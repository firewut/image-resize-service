import zipfile
from zipfile import ZipFile
import os
import tempfile
import string
import random
import re

from flask import Flask, jsonify, request, render_template, send_from_directory, url_for, redirect

import project.settings as settings
import project.schemas as schemas


app = Flask(__name__)

### DEFORM CONNECTION
from pydeform import Client

client = Client(host="deform.io")
token_client = client.auth(  
    'token',
    auth_key=os.getenv("DEFORMIO_TOKEN", "kkXVTMfhjpcqeiUm"),
    project_id=os.getenv("DEFORMIO_PROJECT", "icon-resize"),
)
app.config['token_client'] = token_client
##########################
# Sync schemas
collections = [
    {
        "_id": settings.DIRECT_LINK_SCHEMA_COLLECTION_ID,
        "name": "Link",
        "schema": schemas.DIRECT_LINK_SCHEMA
    },
    {
        "_id": settings.IMAGE_COLLECTION_ID,
        "name": "images",
        "schema": schemas.IMAGE_SCHEMA
    }
]

for collection in collections:
    try:
        token_client.collection.save(
            data=collection,
        )
    except Exception as e:
        print(str(e)) 

@app.route('/resize/', methods=['POST'])
def resize():
    """
        This function make a magic:
          
          * Receives image [ --> 1s ]
          * Creates and emty DIRECT LINK DOCUMENT 
          * Sends the image to deform.io [ --> 0s ]
          * Receives JSON response from deform.io. It will contain a list file IDs [ --> 3s ]
            * Downloads a list of image from JSON response [ --> 5s ]
          * Compress the list of images. Remove unused images [ --> 2s ]

        Whole step takes ~11s in worst case scenario
    """
    if not 'image' in request.files:
        return render_template('error.html', message="The image is required"), 422

    form_image = request.files["image"]
    fp = tempfile.TemporaryFile()
    if len(form_image.mimetype) > 0:    
        fp.write(form_image.read())
        fp.seek(0)

    if len(form_image.mimetype) == 0:
        return render_template('error.html', message="The image is required"), 422
    
    if form_image.mimetype not in settings.ALLOWED_MIMETYPES:
        return render_template('error.html', 
            message="The file should be an image",
            sub_message={
                "header": "Supported mime types",
                "content": ', '.join(settings.ALLOWED_MIMETYPES)
            }
        ), 422

    unique_zipfile_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

    # Step 1
    LINK = {
        '_id': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)),
        'local_file': None
    }

    try:
        # response object is 
        deform_response = token_client.document.create(
            collection=settings.DIRECT_LINK_SCHEMA_COLLECTION_ID,
            data=LINK,
        )
    except Exception as e:
        print(str(e))
        return render_template('error.html', message="An error occured"), 500
    
    size = [300, 300]
    try:
        size[0] = int(request.form['width'])
    except:
        pass
    
    try:
        size[1] = int(request.form['height'])
    except:
        pass

    try:
        IMAGE = {
            "original": fp,
            "size": size
        }
        deform_response = token_client.document.create(
            collection=settings.IMAGE_COLLECTION_ID,
            data=IMAGE,
        )

        images = []
        for key in deform_response.keys():
            if re.match(r'(\d+x\d+)', key) or key == 'original' or key == 'custom_size':
                images.append(
                    {
                        '_id': deform_response[key]['_id'],
                        'filename': deform_response[key]['name'] 
                    }
                )
        
        image_to_zip = []
        for icon in images:
            try:
                image_response = token_client.document.get_file(
                    collection='_files',
                    identity=icon['_id']
                )
                image_to_zip.append(
                    {
                        "_id": icon['_id'],
                        "file": image_response.data
                    }
                )
            except Exception as e:
                print(str(e))
                return render_template('error.html', message="An error occured"), 500
        
        # ZIP array of images
        try:
            ext = None
            zipfile_location = '%s/%s.zip' % (settings.ZIPFILE_DIR, unique_zipfile_name)
            with ZipFile(zipfile_location, 'w', zipfile.ZIP_DEFLATED) as myzip:
                for image_to_zip in image_to_zip:
                    filename = ''
                    for icon in images:
                        if icon["_id"] == image_to_zip["_id"]:
                            filename = icon["filename"] 
                            if filename != 'original' and ext == None and filename != 'custom_size':
                                _, ext = os.path.splitext(filename)
                    
                    if filename == 'original':
                        filename = "%s%s" % (filename, ext) 
                    
                    myzip.writestr(filename, image_to_zip["file"])

            try:
                # response object is 
                deform_response = token_client.document.update(
                    collection=settings.DIRECT_LINK_SCHEMA_COLLECTION_ID,
                    data={
                        'local_file': zipfile_location,       
                    },
                    identity=LINK['_id']
                )
            except Exception as e:
                print(str(e))
                return render_template('error.html', message="An error occured"), 500


        except Exception as e:
            print(str(e))
            return render_template('error.html', message="An error occured"), 500

        return redirect(url_for('get_file_by_link', direct_link_id=LINK['_id']))
    finally:
        fp.close()

    return render_template('error.html', message="An error occured"), 422


@app.route('/link/<direct_link_id>/', methods=['GET'])
def get_file_by_link(direct_link_id):
    try:
        link = token_client.document.get(
            identity=direct_link_id,
            collection=settings.DIRECT_LINK_SCHEMA_COLLECTION_ID,
        )
        return send_from_directory(
            os.path.abspath('.'),
            link['local_file'],
            as_attachment=True)
    except:
        pass
    
    render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(
        debug=settings.DEBUG,
        host="0.0.0.0",
        port=8888
    )
