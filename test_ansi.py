#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SEE: https://github.com/sphinx-doc/sphinx/

from __future__ import absolute_import, print_function
from docutils import nodes
from mock import Mock
from pathlib import Path
import pytest
import sys

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

try:
    from sphinxcontrib import ansi
except ImportError as e:
    print("IMPORT-ERROR: %s" % e)
    for index, p in enumerate(sys.path):
        print("{0:2d}.  {1}".format(index, p))
    raise


RAWSOURCE = '''\
\x1b[1mfoo\x1b[33;1mbar\x1b[1;34mhello\x1b[0mworld\x1b[1m'''


# -----------------------------------------------------------------------------
# FIXTURES:
# -----------------------------------------------------------------------------
@pytest.fixture
def paragraph():
    paragraph = nodes.paragraph()
    paragraph.append(ansi.ansi_literal_block(RAWSOURCE, RAWSOURCE))
    return paragraph


@pytest.fixture
def app():
    return Mock()


@pytest.fixture
def parser():
    return ansi.ANSIColorParser()


# -----------------------------------------------------------------------------
# TEST SUPPORT:
# -----------------------------------------------------------------------------
def _assert_colors(node, *colors):
    assert isinstance(node, nodes.inline)
    for color in colors:
        assert ('ansi-%s' % color) in node['classes']


def _assert_text(node, text):
    assert isinstance(node, nodes.Text)
    assert node.astext() == text



# -----------------------------------------------------------------------------
# TEST SUITE:
# -----------------------------------------------------------------------------
def test_parser_strip_colors(app, parser, paragraph):
    app.builder.name = 'foo'
    parser(app, paragraph, 'foo')
    assert isinstance(paragraph[0], nodes.literal_block)
    _assert_text(paragraph[0][0], 'foobarhelloworld')
    assert not paragraph[0][0].children
    assert paragraph.astext() == 'foobarhelloworld'


def test_parser_colors_parsed(app, parser, paragraph):
    app.builder.name = 'html'
    parser(app, paragraph, 'foo')
    block = paragraph[0]
    assert isinstance(block, nodes.literal_block)
    _assert_colors(block[0], 'bold')
    _assert_text(block[0][0], 'foo')
    _assert_colors(block[1], 'bold', 'yellow')
    _assert_text(block[1][0], 'bar')
    _assert_colors(block[2], 'bold', 'blue')
    _assert_text(block[2][0], 'hello')
    _assert_text(block[3], 'world')
    _assert_colors(block[4], 'bold')
    assert not block[4].children
    assert paragraph.astext() == 'foobarhelloworld'


def test_setup(app):
    ansi.setup(app)
    app.require_sphinx.assert_called_with('1.0')
    app.add_config_value.assert_called_with(
        'html_ansi_stylesheet', None, 'env')
    app.add_directive.assert_called_with(
        'ansi-block', ansi.ANSIBlockDirective)
    assert app.connect.call_args_list[:2] == [
        (('builder-inited', ansi.add_stylesheet),),
        (('build-finished', ansi.copy_stylesheet),)]
    assert app.connect.call_args_list[2][0][0] == 'doctree-resolved'
    assert isinstance(app.connect.call_args_list[2][0][1],
                      ansi.ANSIColorParser)


# -----------------------------------------------------------------------------
# TEST MAIN:
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import pytest
    pytest.main()
