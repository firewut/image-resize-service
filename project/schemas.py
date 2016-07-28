DIRECT_LINK_SCHEMA = {
    "type": "object",
    "properties": {
        "local_file": {
            "type": ["string", "null"],
            "description": "local zip file path"
        }
    }
}

ICONS_SCHEMA = {
    "type": "object",
    "properties": {
        "original": {
            "type": "file"
        },
        "120x120": {
            "type": "file",
            "processors": [
                {
                    "name": "resize",
                    "in": {
                        "original_image": {
                            "property": "original"
                        },
                        "size": {
                            "value": [120, 120]
                        }
                    }
                }
            ]
        },
        "152x152": {
            "type": "file",
            "processors": [
                {
                    "name": "resize",
                    "in": {
                        "original_image": {
                            "property": "original"
                        },
                        "size": {
                            "value": [152, 152]
                        }
                    }
                }
            ]
        },
        "167x167": {
            "type": "file",
            "processors": [
                {
                    "name": "resize",
                    "in": {
                        "original_image": {
                            "property": "original"
                        },
                        "size": {
                            "value": [167, 167]
                        }
                    }
                }
            ]
        },
        "180x180": {
            "type": "file",
            "processors": [
                {
                    "name": "resize",
                    "in": {
                        "original_image": {
                            "property": "original"
                        },
                        "size": {
                            "value": [180, 180]
                        }
                    }
                }
            ]
        }
    }
}