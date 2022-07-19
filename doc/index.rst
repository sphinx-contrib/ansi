.. highlight:: rest
.. default-domain:: rst

:py:mod:`sphinxcontrib.ansi` -- Parse ANSI control sequences
============================================================

.. py:module:: sphinxcontrib.ansi
   :synopsis:  Parse and interpret ANSI control sequences

This extension for Sphinx_ 1.0 converts ANSI colour sequences to colored
HTML output.  Use this extension to correctly include the output of command
line tools, which use these control sequences to color their output (like
``sphinx-build``, for instance).

The extension is available under the terms of the BSD license, 
see LICENSE for more information.


Installation
------------

This extension can be installed from the Python Package Index::

   pip install sphinxcontrib-ansi

Alternatively, you can clone the `sphinx-contrib/ansi`_ repository,
and install the extension directly from the repository::

   git clone https://github.com/sphinx-contrib/ansi sphinxcontrib-ansi
   cd sphinxcontrib-ansi
   python setup.py install


Usage
-----

To interpret ANSI colour codes, use the following directive:

.. directive:: ansi-block

   This directive interprets its content as literal block containing ANSI
   control sequences for coloured output for HTML output.  If the document
   is build with any other builder than ``html``, color sequences are
   stripped from output.

   If the option ``string_escape`` is specified, the content of the
   directive is decoded using the ``string_escape`` codec.  Thus you can
   include Python escape sequences, and therefore use ``\x1b`` instead of
   the real escape character.


Appearance
^^^^^^^^^^

The appearance is controlled by :confval:`html_ansi_stylesheet`:

.. confval:: html_ansi_stylesheet

   The builtin stylesheet to use for ANSI color sequences.  As of now, the
   following builtin stylesheets are provided:

   - ``black-on-white.css``: Use dark colors on a white background.

If you do not like the builtin stylesheets, set
:confval:`html_ansi_stylesheet` to ``None`` and create your own stylesheet.
This stylesheet must provide styles for the following CSS classes:

- ``ansi-bold``: Bold text
- ``ansi-dark``: Dark text
- ``ansi-underscore``: Underlined text
- ``ansi-black``: Black colour
- ``ansi-red``: Red colour
- ``ansi-green``: Green colour
- ``ansi-yellow``: Yellow colour
- ``ansi-blue``: Blue colour
- ``ansi-magenta``: Magenta colour
- ``ansi-cyan``: Cyan colour
- ``ansi-white``: White colour

These classes can appear in different combinations, especially a colour
combined with a text format.  You can therefore use a different colour, if
the colour class is combined with a text format class.  See
`black-on-white.css`_ for an example.

Put this stylesheet somewhere in your :confval:`html_static_path` and make
it known to sphinx by including the following code snippet in your
``conf.py``:

.. code-block:: python

   def setup(app):
       # -- NOTE: RemovedInSphinx40Warning:
       # The app.add_stylesheet() is deprecated. Please use app.add_css_file() instead.
       app.add_css_file('my_ansi_theme.css')

       # OLDER-SOLUTION: sphinx <= 2.0
       # app.add_stylesheet('my_ansi_theme.css')


Contribution
------------

Please contact the author or create an issue in the `issue tracker`_ of the
`sphinx-contrib/ansi`_ repository, if you have found any bugs or miss some
functionality (e.g. support for more attributes).  Patches are welcome!


.. toctree::
   :maxdepth: 2
   :hidden:

   changes.rst


.. _`Sphinx`: https://www.sphinx-doc.org/
.. _`sphinx-contrib/ansi`: https://github.com/sphinx-contrib/ansi
.. _`issue tracker`:       https://github.com/sphinx-contrib/ansi/issues
.. _`black-on-white.css`:  https://github.com/sphinx-contrib/ansi/blob/master/sphinxcontrib/black-on-white.css

.. hidden:

   BROKEN: Missing on Github.
   .. _LICENSE: https://bitbucket.org/birkenfeld/sphinx-contrib/src/tip/LICENSE

