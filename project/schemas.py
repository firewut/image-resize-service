DIRECT_LINK_SCHEMA = {
    "type": "object",
    "properties": {
        "local_file": {
            "type": ["string", "null"],
            "description": "local zip file path"
        }
    }
}

IMAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "original": {
            "type": "file"
        },
        "size": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "custom_size": {
            "type": "file",
            "processors": [
                {
                    "name": "resize",
                    "in": {
                        "original_image": {
                            "property": "original"
                        },
                        "size": {
                            "property": "size"
                        }
                    }
                }
            ]
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