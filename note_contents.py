"""
Fuck yeah!
"""
from PySide6 import QtCore, QtGui, QtWidgets


class noteContents(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.arrange()

    def arrange(self):
        title = QtWidgets.QPushButton(parent=self)
        title.setGeometry(20, 20, 30, 30)
        title.clicked.connect(self._deleteNote)
        pix = QtGui.QPixmap('pic.png')
        title.setIcon(pix)
        title.setIconSize(self.size())
        self.setStyleSheet('background-color: green')
        self.setStyleSheet('background: transparent')

    def _deleteNote(self):
        self.parentWidget().delete()
