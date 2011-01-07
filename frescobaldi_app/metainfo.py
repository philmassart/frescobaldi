# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008, 2009, 2010 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

from __future__ import unicode_literals

"""
Store meta information about documents.
"""

import time
import weakref

from PyQt4.QtCore import QSettings, QUrl

import app


__all__ = ["info", "add"]


# This dictionary stores the MetaInfo objects per document
_metainfo = weakref.WeakKeyDictionary()

# This dictionary store the default values: "name": [default, readfunc]
_defaults = {}


def info(document):
    """Returns a MetaInfo object for the Document."""
    try:
        return _metainfo[document]
    except KeyError:
        minfo = _metainfo[document] = MetaInfo(document)
    return minfo


def add(name, default, readfunc=None):
    """Define a value to be stored in the metainfo.
    
    Should be defined before it is requested or set.
    If readfunc is not given it defaults to a suitable function for bool or int types.
    
    """
    if readfunc is None:
        if isinstance(default, bool):
            if default:
                readfunc = lambda v: v not in ('false', False)
            else:
                readfunc = lambda v: v not in ('true', True)
        elif isinstance(default, int):
            readfunc = int
        else:
            readfunc = lambda v: v
    _defaults[name] = [default, readfunc]
    
    # read this value for already loaded metainfo items
    for minfo in _metainfo.items():
        minfo.loadValue(name)


class MetaInfo(object):
    def __init__(self, document):
        self.document = weakref.ref(document)
        self.load()
        document.loaded.connect(self.load)
        
    def settingsGroup(self):
        url = self.document().url()
        if not url.isEmpty():
            s = app.settings('metainfo')
            s.beginGroup(url.toString().replace('\\', '_').replace('/', '_'))
            return s
        
    def load(self):
        s = self.settingsGroup()
        for name in _defaults:
            self.loadValue(name, s)
        
    def loadValue(self, name, settings=None):
        s = settings or self.settingsGroup()
        default, readfunc = _defaults[name]
        if s and QSettings().value("metainfo", True) not in (False, 'false'):
            self.__dict__[name] = readfunc(s.value(name, default))
        else:
            self.__dict__[name] = default

    def save(self):
        s = self.settingsGroup()
        if s:
            s.setValue("time", time.time())
            for name in _defaults:
                value = self.__dict__[name]
                s.remove(name) if value == _defaults[name][0] else s.setValue(name, value)
            

@app.documentClosed.connect
def save(document):
    info(document).save()
    

@app.qApp.aboutToQuit.connect
def prune():
    """Prune old info."""
    s = app.settings('metainfo')
    month_ago = time.time() - 31 * 24 * 3600
    for key in s.childGroups():
        if float(s.value(key + "/time", 0.0)) < month_ago:
            s.remove(key)

