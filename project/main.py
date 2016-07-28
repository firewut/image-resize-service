from flask import Flask, jsonify, request, render_template, send_from_directory, url_for

import zipfile
from zipfile import ZipFile

import os
import tempfile
import pdb
import settings
import string
import schemas
import random
import re

app = Flask(__name__)

### DEFORM CONNECTION
from pydeform import Client

client = Client(host="deform.io")
token_client = client.auth(  
    'token',
    auth_key=os.getenv("DEFORMIO_TOKEN", "kkXVTMfhjpcqeiUm"),
    project_id=os.getenv("DEFORMIO_PROJECT", "icon-resize"),
)
##########################
# Sync schemas
collections = [
    {
        "_id": settings.DIRECT_LINK_SCHEMA_COLLECTION_ID,
        "name": "Link",
        "schema": schemas.DIRECT_LINK_SCHEMA
    },
    {
        "_id": settings.ICONS_COLLECTION_ID,
        "name": "Icons",
        "schema": schemas.ICONS_SCHEMA
    }
]

# for collection in collections:
#     try:
#         token_client.collection.save(
#             data=collection,
#         )
#     except Exception as e:
#         pdb.set_trace() 

@app.route('/resize/', methods=['POST'])
def resize():
    """
        This function make a magic:
          
          * + Receives image [ --> 1s ]
          * + Creates and emty DIRECT LINK DOCUMENT 
          * + Sends the image to deform.io [ --> 0s ]
          * + Receives JSON response from deform.io. It will contain a list file IDs [ --> 3s ]
            * + Downloads a list of image from JSON response [ --> 5s ]
          * + Compress the list of images. Remove unused images [ --> 2s ]

        Whole step takes ~11s in worst case scenario
    """
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
        pdb.set_trace()


    form_icon = request.files["icon"]
    fp = tempfile.TemporaryFile()
    
    if len(form_icon.mimetype) > 0:    
        fp.write(form_icon.read())
        fp.seek(0)
    try:
        ICON = {
            "original": fp
        }
        deform_response = token_client.document.create(
            collection=settings.ICONS_COLLECTION_ID,
            data=ICON,
        )

        icons = []
        for key in deform_response.keys():
            if re.match(r'(\d+x\d+)', key) or key == 'original':
                icons.append(
                    {
                        '_id': deform_response[key]['_id'],
                        'filename': deform_response[key]['name'] 
                    }
                )
        
        icon_to_zip = []
        for icon in icons:
            try:
                icon_response = token_client.document.get_file(
                    collection='_files',
                    identity=icon['_id']
                )
                icon_to_zip.append(
                    {
                        "_id": icon['_id'],
                        "file": icon_response.data
                    }
                )
            except Exception as e:
                print(str(e))
                pdb.set_trace()
        
        # ZIP array of icons
        try:
            ext = None
            zipfile_location = '%s/%s.zip' % (settings.ZIPFILE_DIR, unique_zipfile_name)
            with ZipFile(zipfile_location, 'w', zipfile.ZIP_DEFLATED) as myzip:
                for icon_to_zip in icon_to_zip:
                    # pdb.set_trace()
                    filename = ''
                    for icon in icons:
                        if icon["_id"] == icon_to_zip["_id"]:
                            filename = icon["filename"] 
                            if filename != 'original' and ext == None:
                                _, ext = os.path.splitext(filename)
                    
                    if filename == 'original':
                        filename = "%s%s" % (filename, ext) 

                    myzip.writestr(filename, icon_to_zip["file"])

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
                pdb.set_trace()


        except Exception as e:
            print(str(e))
            pdb.set_trace()

        response = jsonify({
            "link_for_results":  url_for('get_file_by_link', direct_link_id=LINK['_id'])
        })
        return response, 202
    finally:
        fp.close()

    return jsonify({
        "message": "error occured"
    }), 422


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
    
    return jsonify({
        "message": "the link does not exists"
    }), 404

@app.route('/')
def index_page():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8888
    )
