import os

ZIPFILE_DIR = os.getenv('ZIPFILE_DIR', 'zip_files')

DEBUG = os.getenv('IMAGE_RESIZE_SERVICE_MODE', 'test') == 'prod'
PORT = os.getenv('PORT', 8888)


IMAGE_COLLECTION_ID = 'images'
DIRECT_LINK_SCHEMA_COLLECTION_ID = 'link'

ALLOWED_MIMETYPES = (
    "image/bmp",
    "image/cgm",
    # "image/g3fax",
    "image/gif",
    # "image/ief",
    "image/jpeg",
    # "image/ktx",
    "image/png",
    # "image/prs.btif",
    "image/sgi",
    "image/svg+xml",
    "image/tiff",
    # "image/vnd.adobe.photoshop",
    # "image/vnd.dece.graphic",
    # "image/vnd.dvb.subtitle",
    # "image/vnd.djvu",
    # "image/vnd.dwg",
    # "image/vnd.dxf",
    # "image/vnd.fastbidsheet",
    # "image/vnd.fpx",
    # "image/vnd.fst",
    # "image/vnd.fujixerox.edmics-mmr",
    # "image/vnd.fujixerox.edmics-rlc",
    # "image/vnd.ms-modi",
    # "image/vnd.ms-photo",
    # "image/vnd.net-fpx",
    # "image/vnd.wap.wbmp",
    # "image/vnd.xiff",
    "image/webp",
    # "image/x-3ds",
    # "image/x-cmu-raster",
    # "image/x-cmx",
    # "image/x-freehand",
    "image/x-icon",
    # "image/x-mrsid-image",
    # "image/x-pcx",
    # "image/x-pict",
    # "image/x-portable-anymap",
    "image/x-portable-bitmap",
    "image/x-portable-graymap",
    "image/x-portable-pixmap",
    # "image/x-rgb",
    # "image/x-tga",
    "image/x-xbitmap",
    "image/x-xpixmap",
    # "image/x-xwindowdump",
)