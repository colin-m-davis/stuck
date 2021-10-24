from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Slot

from note_window import noteWindow


class menuBar(QtWidgets.QMenuBar):
    def __init__(self):
        super(menuBar, self).__init__(parent=None)

        menu_file = menuFile(parent=self)
        self.addMenu(menu_file)


class menuFile(QtWidgets.QMenu):
    def __init__(self, parent=None):
        super().__init__(parent=parent, title='File')

        self.new_note = QtGui.QAction('New Note')
        self.new_note.setShortcut(QtGui.QKeySequence.New)
        self.new_note.triggered.connect(self._newNoteSlot)
        self.addAction(self.new_note)

    @Slot()
    def _newNoteSlot(self):
        noteWindow()
