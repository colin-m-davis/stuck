from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Slot

from sidegrip import CSizeGrip, SideGrip
from note_contents import noteContents
import db


class noteWindow(QtWidgets.QMainWindow):
    def __init__(self, obj=None):
        super().__init__()

        self.resize(360, 360)
        self.setMinimumSize(90, 90)
        self.setWindowOpacity(0.9)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        self.sideGrips = None
        self.cornerGrips = None
        self.setGrips()

        self._prev_pos = None
        self._drag_active = False

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(48, 48, 48))
        self.setPalette(p)

        f = noteContents(parent=self)
        self.setCentralWidget(f)
        self.centralWidget()

        self.show()
        self.raise_()

        if obj:
            self.obj = obj
            self.load()
        else:
            self.obj = db.Note()
            self.save()

    _gripSize = 8

    @property
    def gripSize(self):
        return self._gripSize

    def setGrips(self):
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge),
        ]

        self.cornerGrips = []
        for _ in range(4):
            g = CSizeGrip(self)
            self.cornerGrips.append(g)

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        out_rect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        in_rect = out_rect.adjusted(self.gripSize, self.gripSize, -self.gripSize, -self.gripSize)

        # top left corner
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(out_rect.topLeft(), in_rect.topLeft()))
        # top right corner
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(out_rect.topRight(), in_rect.topRight()).normalized())
        # bottom right corner
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(in_rect.bottomRight(), out_rect.bottomRight()))
        # bottom left corner
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(out_rect.bottomLeft(), in_rect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, in_rect.top(), self.gripSize, in_rect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            in_rect.left(), 0, in_rect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            in_rect.left() + in_rect.width(),
            in_rect.top(), self.gripSize, in_rect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, in_rect.top() + in_rect.height(),
            in_rect.width(), self.gripSize)

    def load(self):
        self.move(self.obj.x, self.obj.y)
        self.resize(self.obj.w, self.obj.h)
        QtWidgets.QApplication.instance().activeNotes[self.obj.id] = self

    def save(self):
        self.obj.x = self.x()
        self.obj.y = self.y()
        self.obj.w = self.width()
        self.obj.h = self.height()
        db.session.add(self.obj)
        db.session.commit()
        print(self.obj)
        QtWidgets.QApplication.instance().activeNotes[self.obj.id] = self

    @Slot()
    def delete(self):
        db.session.delete(self.obj)
        db.session.commit()
        self.close()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def mousePressEvent(self, e):
        self._prev_pos = e.globalPosition().toPoint()
        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, e):
        delta = e.globalPosition().toPoint() - self._prev_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._prev_pos = e.globalPosition().toPoint()

        self._drag_active = True

    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self.save()
            self._prev_pos = None
            self._drag_active = False
            self.setCursor(QtCore.Qt.ArrowCursor)
