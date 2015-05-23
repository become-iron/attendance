# -*- coding: utf-8 -*-

import random
import sys
import time
from PyQt4 import QtGui
from PyQt4 import QtCore
import sip

import logic

error_id = None
semester_name = None
group_name = None
subject_name = None

repeat = False  # индикатор повторного вызова стартового диалога
repeater = 0  # счетчик количества использований

class MainDialog(QtGui.QWidget):
    def __init__(self):
        global choose_container, choose_gb, repeater
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Контроль посещаемости')

        # создание сетки, в которую помещаются остальные виджеты
        main_container = QtGui.QGridLayout(self)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        main_container.addWidget(self.exit_button, 2, 0, 1, 1)

        # создание кнопки для ввода данных
        self.open_button = QtGui.QPushButton(u"Открыть")
        self.connect(self.open_button, QtCore.SIGNAL('clicked()'), self.open)
        main_container.addWidget(self.open_button, 1, 0, 1, 1)

        # создание рамки для ввода id
        choose_gb = QtGui.QGroupBox('Выберите группу и семестр', self)
        choose_gb.setAlignment(QtCore.Qt.AlignCenter)

        # добавление рамки в сетку
        main_container.addWidget(choose_gb, 0, 0, 1, 1)

        # создание сетки, в которую помещаются выпадающие списки
        choose_container = QtGui.QGridLayout(choose_gb)

        # создание сообщения о выборе группы
        choose_group_l = QtGui.QLabel(u"""Выберите номер группы:""", choose_gb)
        choose_container.addWidget(choose_group_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_group_cb = QtGui.QComboBox(choose_gb)
        choose_group_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_group_cb.addItem(None)

        """
        Вызываю функцию для получения списка групп
        """
        list_of_groups = logic.get_groups()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            choose_group_cb.addItem(str(i))
        choose_group_cb.setEditable(False)

        if repeat is True:
            repeater += 1
            choose_group_cb.setCurrentIndex(choose_group_cb.findText(group_name_re))
            self.choose_semester(group_name_re)

        # добавление списка в сетку
        choose_container.addWidget(choose_group_cb, 1, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_group_cb.currentIndexChanged[str].connect(self.choose_semester)

    def choose_semester(self, group_index):
        global choose_container, choose_semester_cb, choose_semester_l, group_name, semester_name, group_name_re, semester_name_re, subject_name, repeater
        group_name = group_index
        group_name_re = group_name

        print(repeat, group_name, semester_name, subject_name)

        # семестр обнуляется
        semester_name = None
        subject_name = None

        print(group_name)

        if bool(group_name) is True:
            try:
                choose_subject_l.deleteLater()
                choose_subject_l.setParent(None)
                choose_subject_cb.deleteLater()
                choose_subject_cb.setParent(None)

                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)
            except NameError:
                pass
            except RuntimeError:
                pass

            choose_gb.adjustSize()
            self.adjustSize()

            # создание сообщения о выборе группы
            choose_semester_l = QtGui.QLabel(u"""Выберите номер семестра:""", choose_gb)
            choose_container.addWidget(choose_semester_l, 3, 0, 1, 1)

            # создание выпадающего списка о выборе группы
            choose_semester_cb = QtGui.QComboBox(choose_gb)
            choose_semester_cb.clear()
            # добавляет пустую строку, чтобы изначально группа не была выбрана
            choose_semester_cb.addItem(None)

            """
            Вызываю функцию для получения списка семестров
            Оправляю номер группы
            Должен получить список с семестрами
            """
            try:
                list_of_semester = logic.get_semesters(group_name)
                # добавляет в выпадающий список семестры
                for i in list_of_semester:
                    choose_semester_cb.addItem(str(i))
            except logic.WrongDataError:
                try:
                    choose_semester_l.deleteLater()
                    choose_semester_l.setParent(None)
                    choose_semester_cb.deleteLater()
                    choose_semester_cb.setParent(None)
                except NameError:
                    pass

                choose_gb.resize(choose_gb.sizeHint())
                self.adjustSize()

            choose_semester_cb.setEditable(False)

            if repeat is True:
                repeater += 1
                choose_semester_cb.setCurrentIndex(choose_semester_cb.findText(semester_name_re))
                self.choose_subject(semester_name_re)

            semester_name_re = None

            # добавление списка в сетку
            choose_container.addWidget(choose_semester_cb, 4, 0, 1, 1)

            # при выборе значения из списка вызывает функцию по поиску семестров
            choose_semester_cb.currentIndexChanged[str].connect(self.choose_subject)

        else:
            try:
                choose_subject_l.deleteLater()
                choose_subject_l.setParent(None)
                choose_subject_cb.deleteLater()
                choose_subject_cb.setParent(None)

                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)
            except NameError:
                pass
            except RuntimeError:
                pass

            choose_gb.adjustSize()
            self.adjustSize()

    def choose_subject(self, semester_index):
        global semester_name, choose_container, choose_subject_cb, choose_subject_l, group_name, subject_name, group_name_re, subject_name_re, semester_name_re, repeater

        semester_name = semester_index
        semester_name_re = semester_name

        print(semester_name)

        # предмет обнуляется
        subject_name = None
        if bool(semester_name) is True:
            try:
                choose_subject_l.deleteLater()
                choose_subject_l.setParent(None)
                choose_subject_cb.deleteLater()
                choose_subject_cb.setParent(None)
            except NameError:
                pass
            except RuntimeError:
                pass

            # создание сообщения о выборе группы
            choose_subject_l = QtGui.QLabel(u"""Выберите предмет:""", choose_gb)
            choose_container.addWidget(choose_subject_l, 5, 0, 1, 1)

            # создание выпадающего списка о выборе группы
            choose_subject_cb = QtGui.QComboBox(choose_gb)
            choose_subject_cb.clear()
            # добавляет пустую строку, чтобы изначально группа не была выбрана
            choose_subject_cb.addItem(None)

            """
            Вызываю функцию для получения списка семестров
            Оправляю номер группы
            Должен получить список с семестрами
            """
            try:
                list_of_subject = logic.get_subjects(group_name, semester_name)
                # добавляет в выпадающий список семестры
                print(logic.get_subjects(group_name, semester_name))
                for i in list_of_subject:
                    choose_subject_cb.addItem(str(i))
            except logic.WrongDataError:
                try:
                    choose_subject_l.deleteLater()
                    choose_subject_l.setParent(None)
                    choose_subject_cb.deleteLater()
                    choose_subject_cb.setParent(None)
                except NameError:
                    pass

                choose_gb.resize(choose_gb.sizeHint())
                self.adjustSize()

            choose_subject_cb.setEditable(False)

            if repeat is True:
                repeater += 1
                choose_subject_cb.setCurrentIndex(choose_subject_cb.findText(subject_name_re))
                self.subject(subject_name_re)

            subject_name_re = None

            # добавление списка в сетку
            choose_container.addWidget(choose_subject_cb, 6, 0, 1, 1)

            # при выборе значения из списка вызывает функцию по поиску семестров
            choose_subject_cb.currentIndexChanged[str].connect(self.subject)

        else:
            try:
                choose_subject_l.deleteLater()
                choose_subject_l.setParent(None)
                choose_subject_cb.deleteLater()
                choose_subject_cb.setParent(None)
            except NameError:
                pass
            except RuntimeError:
                pass

            choose_gb.adjustSize()
            self.adjustSize()

    def subject(self, subject_index):
        global subject_name, repeat
        subject_name = subject_index
        print(repeat, group_name, semester_name, subject_name)

        if repeater == 3:
            repeat = False
        print(repeater, repeat)


    def open(self):
        global error_id, attendance, dates_list
        # код ошибки обнуляется
        error_id = None

        print(repeat, group_name, semester_name, subject_name)

        if bool(subject_name) is False:
            error_id = 2
            if bool(semester_name) is False:
                error_id = 1
                if bool(group_name) is False:
                    error_id = 0
        if error_id is not None:
            # если ошибка возникла, окрывается окно с ошибкой
            self.error_window()
        else:
            dates_list = logic.get_lessons(group_name, semester_name)
            attendance = logic.get_values_semester(group_name, semester_name)
            attendance = dict(sorted(attendance.items(), key=lambda x: x[1]))
            self.show_table()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()

    def show_table(self):
        global repeat
        repeat = False
        self.table = TableWindow()
        self.table.show()
        self.close()


class ErrorMessage(QtGui.QMessageBox):
    def __init__(self, error_id):
        QtGui.QMessageBox.__init__(self)

        # в зависимости от кода надпись меняется
        if error_id == 0:
            self.setText(u"Группа не выбрана")
        elif error_id == 1:
            self.setText(u"Семестр не выбран")
        elif error_id == 2:
            self.setText(u"Предмет не выбран")

        # настройки окна
        self.setWindowTitle('Ошибка')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.addButton('ОК', QtGui.QMessageBox.AcceptRole)


class TableWindow(QtGui.QWidget):
    def __init__(self):
        global table_widget, attendance, dates_list
        print(group_name, semester_name, subject_name)
        QtGui.QWidget.__init__(self)

        # настройки окна
        self.setWindowTitle('Контроль посещаемости')

        # создание сетки, в которую помещаются остальные виджеты
        table_main_container = QtGui.QGridLayout(self)

        # добавление кнопки отметки
        self.check_button = QtGui.QPushButton(u"Отметить")
        table_main_container.addWidget(self.check_button, 0, 0, 1, 1)

        # добавление кнопки преподавателя
        self.super_button = QtGui.QPushButton(u"Зайти как препод")
        table_main_container.addWidget(self.super_button, 1, 0, 1, 1)

        # добавление кнопки смены группы
        self.change_group_button = QtGui.QPushButton(u"Выбрать другую группу или семестр")
        self.connect(self.change_group_button, QtCore.SIGNAL('clicked()'), self.change_group)
        table_main_container.addWidget(self.change_group_button, 2, 0, 1, 1)

        # добавление кнопки выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        table_main_container.addWidget(self.exit_button, 3, 0, 1, 1)

        # создание виджета таблицы
        table_widget = QtGui.QTableWidget(len(attendance.keys()), len(dates_list))
        table_main_container.addWidget(table_widget, 0, 1, 4, 1)

        # заполнение шапок
        table_widget.setHorizontalHeaderLabels(dates_list)
        table_widget.setVerticalHeaderLabels(list(sorted(attendance.keys())))

        # заполнение ячеек
        for m, name in enumerate(sorted(attendance.keys())):
            for n, item in enumerate(attendance[name]):
                check_item = QtGui.QTableWidgetItem(item)
                check_item.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(m, n, check_item)

    def change_group(self):
        global repeat, group_name_re, semester_name_re, subject_name_re, repeater
        repeat = True
        repeater = 0
        group_name_re = group_name
        semester_name_re = semester_name
        subject_name_re = subject_name
        self.change = MainDialog()
        self.change.show()
        self.close()


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
