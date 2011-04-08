# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2011 by Wilbert Berendsen
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

"""
Help browser dockwidget.
"""

from __future__ import unicode_literals

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QAction, QKeySequence

import actioncollection
import actioncollectionmanager
import icons
import panels


class HelpBrowser(panels.Panel):
    def __init__(self, mainwindow):
        super(HelpBrowser, self).__init__(mainwindow)
        self.toggleViewAction().setShortcut(QKeySequence("Meta+Alt+H"))
        self.hide()
        mainwindow.addDockWidget(Qt.RightDockWidgetArea, self)
        ac = self.actionCollection = Actions()
        actioncollectionmanager.manager(mainwindow).addActionCollection(ac)

    def translateUI(self):
        self.setWindowTitle(_("Help Browser"))
        self.toggleViewAction().setText(_("&Help Browser"))
        
    def createWidget(self):
        from . import browser
        return browser.Browser(self)


class Actions(actioncollection.ActionCollection):
    name = "helpbrowser"
    
    def title(self):
        return _("Help Browser")
    
    def createActions(self, parent=None):
        self.help_back = QAction(parent)
        self.help_forward = QAction(parent)
        self.help_home = QAction(parent)
        self.help_home_lilypond = QAction(parent)
        
        self.help_back.setIcon(icons.get("go-previous"))
        self.help_forward.setIcon(icons.get("go-next"))
        self.help_home.setIcon(icons.get("go-home"))
        self.help_home_lilypond.setIcon(icons.get("lilypond-run"))
        
    def translateUI(self):
        self.help_back.setText(_("Back"))
        self.help_forward.setText(_("Forward"))
        # L10N: Home page of the Frescobaldi manual
        self.help_home.setText(_("Home"))
        self.help_home_lilypond.setText(_("LilyPond"))




