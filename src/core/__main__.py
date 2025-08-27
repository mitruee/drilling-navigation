import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from src.core.gui.menu import Menu


def main():
    app = QApplication(sys.argv)
    default_font = QFont()
    default_font.setPointSize(12)
    app.setFont(default_font)

    win = Menu()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
