
# output.py - utility functions for webcheck
#
# Copyright (C) 1998, 1999 Albert Hopkins (marduk)
# Copyright (C) 2002 Mike W. Meyer
# Copyright (C) 2005, 2006, 2007, 2008, 2010, 2011, 2013 Arthur de Jong
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# The files produced as output from the software do not automatically fall
# under the copyright of the software, unless explicitly stated otherwise.

"""Utility functions for generating the report."""

import codecs
import logging
import os
import shutil
import sys
import time
import urllib
import urlparse

import jinja2

from webcheck import config
from webcheck.db import Link
import webcheck


logger = logging.getLogger(__name__)


def open_file(filename, is_text=True, makebackup=False):
    """This returns an open file object which can be used for writing. This
    file is created in the output directory. The output directory (stored in
    config.OUTPUT_DIR is created if it does not yet exist. If the second
    parameter is True (default) the file is opened as an UTF-8 text file."""
    # check if output directory exists and create it if needed
    if not os.path.isdir(config.OUTPUT_DIR):
        os.mkdir(config.OUTPUT_DIR)
    # build the output file name
    fname = os.path.join(config.OUTPUT_DIR, filename)
    # check if file exists
    if os.path.exists(fname):
        if makebackup:
            # create backup of original (overwriting previous backup)
            os.rename(fname, fname + '~')
        elif not config.OVERWRITE_FILES:
            # ask to overwrite
            try:
                res = raw_input('webcheck: overwrite %s? [y]es, [a]ll, [q]uit: ' % fname)
            except EOFError:
                # bail out in case raw_input() failed
                logger.exception('error reading response')
                res = 'q'
            res = res.lower() + ' '
            if res[0] == 'a':
                config.OVERWRITE_FILES = True
            elif res[0] != 'y':
                raise SystemExit('Aborted.')
    # open the file for writing
    if is_text:
        return codecs.open(fname, encoding='utf-8', mode='w')
    else:
        return open(fname, 'wb')


def install_file(source, is_text=False):
    """Install the given file in the output directory.
    If the is_text flag is set to true it is assumed the file is text,
    translating line endings."""
    # figure out mode to open the file with
    mode = 'r'
    if is_text:
        mode += 'U'
    # check with what kind of argument we are called
    scheme = urlparse.urlsplit(source)[0]
    if scheme == 'file':
        # this is a file:/// url, translate to normal path and open
        source = urllib.url2pathname(urlparse.urlsplit(source)[2])
    elif scheme == '' and os.path.isabs(source):
        # this is an absolute path, just open it as is
        pass
    elif scheme == '':
        # this is a relavite path, try to fetch it from the python path
        for directory in sys.path:
            tst = os.path.join(directory, source)
            if os.path.isfile(tst):
                source = tst
                break
    # TODO: support more schemes here
    # figure out the destination name
    target = os.path.join(config.OUTPUT_DIR, os.path.basename(source))
    # test if source and target are the same
    source = os.path.realpath(source)
    if source == os.path.realpath(target):
        logger.warn('attempt to overwrite %s with itself', source)
        return
    # open the input file
    sfp = open(source, mode)
    # create file in output directory (with overwrite question)
    tfp = open_file(os.path.basename(source), is_text=is_text)
    # copy contents
    shutil.copyfileobj(sfp, tfp)
    # close files
    tfp.close()
    sfp.close()


env = jinja2.Environment(
    loader=jinja2.PackageLoader('webcheck'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
    trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)


def render(output_file, **kwargs):
    """Render the output file with the specified context variables."""
    kwargs.setdefault('webcheck', webcheck)
    kwargs.setdefault('output_file', output_file)
    kwargs.setdefault('time', time.ctime(time.time()))
    crawler = kwargs.get('crawler', None)
    if crawler:
        kwargs.setdefault('sitename', crawler.bases[0].title or crawler.bases[0].url)
    kwargs.setdefault('Link', Link)
    kwargs.setdefault('config', config)
    template = env.get_template(output_file)
    fp = open_file(output_file)
    fp.write(template.render(**kwargs))
    fp.close()
