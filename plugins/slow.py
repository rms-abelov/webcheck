# Copyright (C) 1998,1999  marduk <marduk@python.net>
# Copyright (C) 2002 Mike Meyer <mwm@mired.org>
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

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""Pages that are slow to download"""

__version__ = '1.0'
__author__ = 'mwm@mired.org'

import webcheck
from httpcodes import HTTP_STATUS_CODES
from rptlib import *

Link = webcheck.Link
linkList = Link.linkList
config = webcheck.config

title = "What's Slow"

def generate():
    import time
    print '<div class="table">'
    print '<table border=0 cellpadding=2 cellspacing=2 width="75%">'
    print '\t<tr><th rowspan=2>Link</th>',
    print '<th rowspan=2>Size <br>(Kb)</th>',
    print '<th colspan=3>Time (HH:MM:SS)</th></tr>'
    print '\t<tr><th>28.8</th><th>ISDN</th><th>T1</th></tr>'

    urls = linkList.keys()
    urls.sort(sort_by_size)
    for url in urls:
        link = linkList[url]
        if not link.html: continue
        sizeK = link.totalSize / 1024
        sizek = link.totalSize * 8 / 1000
        if sizeK < config.REPORT_SLOW_URL_SIZE:
            break
        print '\t<tr><td>%s</td>' % make_link(url, get_title(url)),
        print '<td>%s</td><td class="time">%s</td>' \
              % (sizeK, time.strftime('%H:%M:%S',time.gmtime(int(sizek/28.8)))),
        print '<td class="time">%s</td>' \
              % time.strftime('%H:%M:%S',time.gmtime(int(sizek/56))),
        print '<td class="time">%s</td>' \
              % time.strftime('%H:%M:%S',time.gmtime(int(sizek/1500))),
        print '</tr>'
        add_problem('Slow Link: %sK' % sizeK, link) 
    print '</table>'
    print '</div>'
