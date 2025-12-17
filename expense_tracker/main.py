"""
Application entry point for Finly.

Run: python -m expense_tracker.main

Creator: Maloth Harsha
"""
import sys
from PySide6 import QtWidgets
from .controllers import Controller


def main():
    app = QtWidgets.QApplication(sys.argv)
    ctrl = Controller(app)
    ctrl.run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
