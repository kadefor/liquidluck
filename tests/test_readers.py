#!/usr/bin/env python

import os.path
import datetime
from liquidluck.readers.base import BaseReader, Post
from liquidluck.readers.restructuredtext import RestructuredTextReader

ROOT = os.path.abspath(os.path.dirname(__file__))


class TestPost(object):
    def setUp(self):
        self.meta = {
            'author': 'lepture',
            'date': '2012-12-12',
            'tags': 'life, work',
        }

    def test_author(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert str(post.author) == 'lepture'

    def test_date(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.date == datetime.datetime(2012, 12, 12)

    def test_updated(self):
        path = os.path.join(ROOT, 'source', 'post', 'demo-rst-1.rst')
        post = Post(path, 'content', title='title', meta=self.meta)
        assert isinstance(post.updated, datetime.datetime)

    def test_public(self):
        meta = {'public': 'false'}
        post = Post('filepath', 'content', title='title', meta=meta)
        assert post.public is False

        post = Post('filepath', 'content', title='title', meta={})
        assert post.public is True

        meta = {'public': 'true'}
        post = Post('filepath', 'content', title='title', meta=meta)
        assert post.public is True

    def test_tags(self):
        post = Post('filepath', 'content', title='title', meta=self.meta)
        assert post.tags == ['life', 'work']

    def test_getattr(self):
        meta = {'date': '2012-12-12', 'topic': 'getattr'}
        post = Post('filepath', 'content', title='title', meta=meta)

        assert getattr(getattr(post, 'date'), 'year') == 2012
        assert hasattr(post, 'topic') is True
        assert getattr(post, 'topic') == 'getattr'


class TestRestructuredTextReader(object):
    def setUp(self):
        path = os.path.join(ROOT, 'source/post/demo-rst-1.rst')
        self.reader = RestructuredTextReader(path)
        self.post = self.reader.render()

    def test_title(self):
        assert self.post.title == 'rst'

    def test_tags(self):
        assert self.post.tags == ['tag1', 'tag2']

    def test_public(self):
        assert self.post.public is False

    def test_pygments(self):
        assert 'highlight' in self.post.content
