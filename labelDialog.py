#
# Copyright (C) 2011 Michael Pitidis, Hussein Abdulwahid.
#
# This file is part of Labelme.
#
# Labelme is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Labelme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Labelme.  If not, see <http://www.gnu.org/licenses/>.
#

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import newIcon, labelValidator

# TODO:
# - Calculate optimal position so as not to go out of screen area.

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="Enter object label", parent=None):
        super(LabelDialog, self).__init__(parent)
        layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setAutoCompletion(True)
        self.combo.setValidator(labelValidator())
        self.labelCandidates = []
        for text in open('label_list.txt', 'r').readlines():
            t = text.strip()
            if t != '':
                self.combo.addItem(t)
                self.labelCandidates.append(t)
        layout.addWidget(self.combo) 
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)
        self.setLayout(layout)

    def validate(self):
        if self.combo.currentText().trimmed():
            self.accept()

    def postProcess(self):
        '''this method was originally added as self.edit.editingFinished.connect(self.postProcess)'''
        self.combo.setCurrentText(self.combo.currentText().trimmed())

    def popUp(self, text='', move=True):
        self.combo.setCurrentIndex(0)
        self.combo.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        status = self.exec_()
        if status:
            labelText = unicode(self.combo.currentText()).strip()
            if labelText not in self.labelCandidates:
                self.labelCandidates.append(labelText)
                self.combo.removeItem(self.combo.count() - 1) # remove the item that may have tailing space
                self.combo.addItem(labelText)
            return labelText
        else:
            return None

