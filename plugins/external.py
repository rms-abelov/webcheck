
# external.py - plugin to list external links
#
# Copyright (C) 1998, 1999 Albert Hopkins (marduk) <marduk@python.net>
# Copyright (C) 2002 Mike Meyer <mwm@mired.org>
# Copyright (C) 2005 Arthur de Jong <arthur@tiefighter.et.tudelft.nl>
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
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""External links"""

__version__ = '1.0'
__author__ = 'mwm@mired.org'


import webcheck
from rptlib import *

title = 'External Links'

def generate(fp):
    fp.write('<ol>\n')
    for url in Link.linkMap.keys():
        link=Link.linkMap[url]
        if link.external:
            fp.write('  <li>%s</li>\n' % make_link(url,get_title(url)))
    fp.write('</ol>\n')
