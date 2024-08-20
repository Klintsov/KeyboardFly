import sys
from PySide6.QtWidgets import (QApplication,
                               QWidget,
                               QMainWindow,
                               QPushButton,
                               QVBoxLayout,
                               QHBoxLayout)
from PySide6.QtCore import QSize, QRect
from PySide6 import QtWidgets


class PopupKeyboard(QMainWindow):
    """  Виртуальная клавиатура.
        :attach: родительский виджет, куда будет записана строка ввода.
        :xpos: горизонтальная координата верхнего левого угла виджета PopupKeyboard.
        :ypos: вертикальная координата верхнего левого угла виджета PopupKeyboard.
        :win_bg_color: цвет фона основного окна PopupKeyboard.
        :btn_bg_color: цвет фона кнопок PopupKeyboard.
        :btn_brd_hover_color: цвет рамки кнопки при наведении на неё стрелки мыши.
        :btn_text_color: цвет текста кнопки.
    """
    def __init__(self,
                 attach,
                 xpos=None,
                 ypos=None,
                 win_bg_color=None,
                 btn_bg_color=None,
                 btn_text_color=None,
                 btn_border_hover_color=None):
        super().__init__()
        self.setWindowTitle("Виртуальная клавиатура:")
        self.win_bg_color = '#5AAAA5' if win_bg_color is None else win_bg_color
        self.btn_bg_color = '#89abcd' if btn_bg_color is None else btn_bg_color
        self.btn_text_color = '#000000' if btn_text_color is None else btn_text_color
        self.btn_border_hover_color = '#3337ff' if btn_border_hover_color is None else btn_border_hover_color
        self.x = xpos
        self.y = ypos
        self.btn = []
        self.up = False
        self.en = True
        self.inp = ''
        self.attach = attach
        self.attach.setPlaceholderText("Enter your text")
        self.x_pos = self.attach.x() if self.x is None else self.x
        self.y_pos = self.attach.y() + self.attach.height() + 5 if self.y is None else self.y
        self.setGeometry(QRect(self.x_pos, self.y_pos, 590, 185))
        self.setMaximumSize(QSize(590, 185))

        self.keys_en_low = [['ESC', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BkSp'],
                            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[ ', ']', 'Enter'],
                            ['▲', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '\\'],
                            ['RU', 'z', 'x', 'c', 'v', 'space', 'b', 'n', 'm', ',', '.', '/']]

        self.keys_en_upp = [['ESC', '~', '!', '@', '#', '$', '%', '^', '&&', '*', '(', ')', 'BkSp'],
                            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', 'Enter'],
                            ['▼', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', '|'],
                            ['RU', 'Z', 'X', 'C', 'V', 'space', 'B', 'N', 'M', '<', '>', '?']]

        self.keys_ru_low = [['ESC', 'ё', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BkSp'],
                            ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х ', 'ъ', 'Enter'],
                            ['▲', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', '\\'],
                            ['EN', 'я', 'ч', 'с', 'м', 'space', 'и', 'т', 'ь', 'б', 'ю', '.']]

        self.keys_ru_upp = [['ESC', 'Ё', '!', '"', '№', ';', '%', ':', '?', '*', '(', ')', 'BkSp'],
                            ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х ', 'Х', 'Enter'],
                            ['▼', 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', '/'],
                            ['EN', 'Я', 'Ч', 'С', 'М', 'space', 'М', 'Т', 'Ь', 'Б', 'Б', ',']]
        self.setStyleSheet("QWidget {\n"
                           f"background-color: {self.win_bg_color};\n"
                           "}\n"
                           "QPushButton {\n"
                           f"background-color: {self.btn_bg_color};\n"
                           f"color: {self.btn_text_color};\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           f"border: 3px solid {self.btn_border_hover_color};\n"
                           "}")
        self.__initial(self.keys_en_low)
        self.attach.mouseDoubleClickEvent = self.__doble_click

    def __doble_click(self, event):
        """ Показ скрытой клавиатуры."""
        self.showNormal()

    def __initial(self, key) -> None:
        """
        Функция построения виджета виртуальной клавитуры.
        :param key: список строк клавиатуры.
        :type key: list[list[str]]
        :return: widget
        :rtype: None
        """
        widget = QWidget(self)
        widget.setGeometry(0, 0, 590, 185)
        layout_vertical = QVBoxLayout()
        layout_vertical.setContentsMargins(5, 5, 5, 5)
        layout_vertical.setSpacing(5)
        for s in range(0, len(key)):
            str_btn = []
            layout_horizontal = QHBoxLayout()
            for p in range(0, len(key[s])):
                b = QPushButton(parent=widget, text=key[s][p])
                if key[s][p] == 'space':
                    b.setMinimumSize(QSize(85, 40))
                else:
                    b.setMinimumSize(QSize(40, 40))
                b.pressed.connect(lambda v=key[s][p]: self.__button_pressed(v))
                str_btn.append(b)
                layout_horizontal.addWidget(str_btn[p])
            self.btn.append(str_btn)
            layout_vertical.addLayout(layout_horizontal)
        widget.setLayout(layout_vertical)
        self.setCentralWidget(widget)

    def __button_pressed(self, n) -> None:
        """
        Функция обработки нажатий клавиш экранной клавиатуры.
        :param n: строка из названия нажатой клавиши.
        :type n: str()
        :return: None
        :rtype: None
        """
        match n:
            case 'ESC':
                self.inp = None
                self.destroy()
            case '&&':
                self.inp += '&'
            case '▲':
                self.up = True
            case '▼':
                self.up = False
            case 'space':
                self.inp += ' '
            case 'BkSp':
                self.inp = self.inp[:-1]
            case 'RU':
                self.en = False
            case "EN":
                self.en = True
            case 'Enter':
                self.hide()
            case _:
                self.inp += n

        if self.en:
            if self.up:
                self.__initial(self.keys_en_upp)
            else:
                self.__initial(self.keys_en_low)
        if not self.en:
            if self.up:
                self.__initial(self.keys_ru_upp)
            else:
                self.__initial(self.keys_ru_low)
        self.attach.setText(self.inp)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = QMainWindow()
    win.setGeometry(400, 400, 300, 200)
    win.setWindowTitle("CodersLegacy")

    line = QtWidgets.QLineEdit(win)
    line.setFixedWidth(140)
    line.move(80, 80)

    win.show()

    x = win.x() + line.x()
    y = win.y() + line.y() + line.height() + 67

    rbd = PopupKeyboard(attach=line, xpos=x, ypos=y)
    rbd.show()

    sys.exit(app.exec())
