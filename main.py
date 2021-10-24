import sys

from PySide6.QtWidgets import QApplication

import db
import note_window
from menu import menuBar


class Application(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        self.setQuitOnLastWindowClosed(False)
        self.mb = menuBar()

        self.activeNotes = {}

        existing_notes = db.session.query(db.Note).all()
        if len(existing_notes) == 0:
            note_window.noteWindow()
        else:
            for qr in existing_notes:
                note_window.noteWindow(obj=qr)


if __name__ == '__main__':
    app = Application()

    sys.exit(app.exec())

