from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from .gui_horizontal import Horizontal_Well
from .gui_inclined import Inclined_Well
import os

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выберите")
        button_inclined = QPushButton("Рассчет наклонного профиля")
        button_inclined_res = QPushButton("Просмотр результатов")
        button_horiz = QPushButton("Расчет горизонтального профиля")
        button_horiz_res = QPushButton("Просмотр результатов ")

        lay = QVBoxLayout()
        
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        row1.addWidget(button_inclined)
        row1.addWidget(button_inclined_res)

        row2.addWidget(button_horiz)
        row2.addWidget(button_horiz_res)
        lay.addLayout(row1)
        lay.addLayout(row2)

        self.setLayout(lay)

        button_inclined.clicked.connect(self.open_inclined)
        button_horiz.clicked.connect(self.open_horizontal)
        button_horiz_res.clicked.connect(self.open_excel_horiz)
        self._directional_win = None
        self._horizontal_win  = None

    def open_inclined(self):
        # сохраняем в атрибут, чтобы объект не был сборщиком уничтожен
        self._directional_win = Directional_Well()
        self._directional_win.show()

    def open_excel_horiz(self):
        _excel_path = "results.xlsx"
        try:
            from PyQt6.QtWidgets import QMessageBox
            if os.name == 'nt':
                os.startfile(_excel_path)
            elif sys.platform == 'darwin':
                os.system(f'open "{_excel_path}"')
            else:
                os.system(f'xdg-open "{_excel_path}"')
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл:\n{e}")

    def open_horizontal(self):
        self._horizontal_win = Horizontal_Well()
        self._horizontal_win.show()
        
    

