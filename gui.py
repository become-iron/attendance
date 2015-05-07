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
        global choose_container, main_widget, choose_gb
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
        choose_gb = QtGui.QGroupBox('Выберите группу и семестр')
        choose_gb.setAlignment(QtCore.Qt.AlignCenter)

        # добавление рамки в сетку
        main_container.addWidget(choose_gb, 0, 0, 1, 1)

        # создание сетки, в которую помещаются выпадающие списки
        choose_container = QtGui.QGridLayout()

        # добавление сетки в рамку
        choose_gb.setLayout(choose_container)

        # создание сообщения о выборе группы
        choose_group_l = QtGui.QLabel(u"""Выберите номер группы:""")
        choose_container.addWidget(choose_group_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_group_cb = QtGui.QComboBox()
        choose_group_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_group_cb.addItem(None)

        """
        Вызываю функцию для получения списка групп
        """
        list_of_groups = logic.group_get()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            choose_group_cb.addItem(str(i))
        choose_group_cb.setEditable(True)

        # добавление списка в сетку
        choose_container.addWidget(choose_group_cb, 1, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_group_cb.currentIndexChanged[str].connect(self.choose_semester)

    def choose_semester(self, group_index):
        global choose_container, choose_semester_cb, choose_semester_l
        print(group_index)
        try:
            choose_semester_l.deleteLater()
            choose_semester_l.setParent(None)
            choose_semester_cb.deleteLater()
            choose_semester_cb.setParent(None)
        except NameError:
            pass
        except RuntimeError:
            pass

        # создание сообщения о выборе группы
        choose_semester_l = QtGui.QLabel(u"""Выберите номер семестра:""")
        choose_container.addWidget(choose_semester_l, 3, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_semester_cb = QtGui.QComboBox()
        choose_semester_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_semester_cb.addItem(None)

        """
        Вызываю функцию для получения списка семестров
        Оправляю номер группы
        Должен получить список с семестрами
        """
        try:
            list_of_semester = logic.semester_get(group_index)
            # добавляет в выпадающий список семестры
            for i in list_of_semester:
                choose_semester_cb.addItem(str(i))
        except logic.WrongDataError:
            print('kek')
            try:
                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)
            except NameError:
                pass

            choose_gb.resize(choose_gb.sizeHint())
            self.resize(choose_gb.sizeHint())
            MainWindow.adjustSize(self)

        choose_semester_cb.setEditable(True)

        # добавление списка в сетку
        choose_container.addWidget(choose_semester_cb, 4, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_semester_cb.currentIndexChanged[str].connect(self.semester)

    def semester(self, semester_index):
        print(semester_index)

if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
