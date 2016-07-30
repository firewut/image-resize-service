# -*- coding: utf-8 -*-
import os
import unittest

import nose
import re
from urllib.parse import urlparse
from flask import Flask, url_for
from nose.tools import *


from project.main import app
import project.settings as settings

image_file = "project/test_data/icon.png"
text_file = "project/test_data/text.txt"


class FlaskTestClientProxy(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.local_http_client = self.app.test_client()
    
    def tearDown(self):
        app.config['token_client'].documents.remove(
            collection='_files'
        )
        app.config['token_client'].documents.remove(
            collection=settings.DIRECT_LINK_SCHEMA_COLLECTION_ID
        )
        app.config['token_client'].documents.remove(
            collection=settings.IMAGE_COLLECTION_ID
        )
    
    def test_no_image(self):
        data = {
        }
        r_view = self.local_http_client.post(
            '/resize/',
            data={},
            content_type='multipart/form-data'
        )
        assert_equals(r_view.status_code, 422)
        assert b'The image is required' in r_view.data
    
    def test_invalid_image(self):
        r_view = self.local_http_client.post(
            '/resize/',
            data={
                'image': (open(text_file, 'rb'), 'world.txt'),
            },
            content_type='multipart/form-data'
        )
        assert_equals(r_view.status_code, 422)
        assert b'The file should be an image' in r_view.data
    
    def test_valid_image_redirect(self):
        r_view = self.local_http_client.post(
            '/resize/',
            data={
                'image': (open(image_file, 'rb'), 'icon.png'),
            },
            content_type='multipart/form-data',
        )
        assert_equals(r_view.status_code, 302)

    def test_valid_image_zipfile(self):
        r_view = self.local_http_client.post(
            '/resize/',
            data={
                'image': (open(image_file, 'rb'), 'icon.png'),
            },
            content_type='multipart/form-data',
            follow_redirects=True
        )
        assert_equals(r_view.status_code, 200)
        assert_equals(r_view.content_type, "application/zip")


        # o = urlparse(r_view.headers.get('Location'))
        # match = re.match(r'^/\w+/(\w+)/$', o.path) # /link/4H3PY6DSRDOUU7F2THQ4/
        # assert(match != None)
        # groups = match.groups()
        # link_id = groups[0]
    
    # def test_valid_image_with_size(self):
    #     r_view = self.local_http_client.post(
    #         '/resize/',
    #         data={
    #             'width': str(10),
    #             'height': str(10),
    #             'image': (open(image_file, 'rb'), 'icon.png'),
    #         },
    #         content_type='multipart/form-data'
    #     )
    #     assert_equals(r_view.status_code, 302)
    #     # Delete a link and associated file
    
if __name__ == '__main__':
    nose.run(argv=[__file__, '--with-doctest', '-v', '-s'])
