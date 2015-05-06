# -*- coding: utf-8 -*-

import random
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

import logic


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        global input_text
        QtGui.QMainWindow.__init__(self)

        # создание главного виджета
        main_widget = QtGui.QWidget()
        self.setCentralWidget(main_widget)

        # создание сетки, в которую помещаются остальные виджеты
        main_container = QtGui.QGridLayout()
        main_widget.setLayout(main_container)

        # название окна
        self.setWindowTitle('Контроль посещаемости')

        # создание кнопки для выхода
        exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        main_container.addWidget(exit_button, 1, 0, 1, 1)

        # создание рамки для ввода id
        input_gb = QtGui.QGroupBox('Введите id')
        input_gb.setAlignment(QtCore.Qt.AlignCenter)

        # добавление рамки в сетку
        main_container.addWidget(input_gb, 0, 0, 1, 1)

        # создание сетки, в которую помещаются остальные виджеты
        input_container = QtGui.QGridLayout()

        # создание поля ввода сообщения
        input_text = QtGui.QLineEdit()
        input_text.setFixedHeight(25)
        input_text.setMinimumWidth(200)
        input_container.addWidget(input_text, 0, 0, 1, 1)

        # создание поля ввода сообщения
        input_button = QtGui.QPushButton('Send')
        input_button.setFixedSize(75, 25)
        input_container.addWidget(input_button, 0, 1, 1, 1)

        # отправляет id
        input_button.clicked.connect(self.input)

        # добавление сетки в рамку
        input_gb.setLayout(input_container)

    def input(self):
        global input_text
        # вызов функции по поиску введенного id
        gotten_id = input_text.text()
        print(gotten_id)

        prava = logic.search(gotten_id)
        """
        отправляет в функцию введенный id и получает его права
        Получает:
            0 - введен id преподавателя
            1 - введен id старосты
            2 - введен id студента
            3 - id не найден
            4 - id введен неверно
        """

        if prava == 0:
            # вызывет таблицу с правами преподавателя
            self.sensei()
        elif prava == 1:
            # вызывет таблицу с правами старосты
            self.sempai()
        elif prava == 2:
            # просто ставит отметку о присутствии
            self.kohai()
        elif prava == 3:
            # выводит окно об ошибке
            self.not_found()
        elif prava == 4:
            # выводит окно об ошибке
            self.input_error()

    def sensei(self):
        pass

    def sempai(self):
        pass

    def kohai(self):
        pass

    def not_found(self):
        pass
    
    def input_error(self):
        pass

if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
