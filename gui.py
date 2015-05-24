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
        main_container.addWidget(self.exit_button, 3, 0, 1, 1)

        # создание кнопки для ввода данных
        self.create_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.create_button, QtCore.SIGNAL('clicked()'), self.create_window)
        main_container.addWidget(self.create_button, 2, 0, 1, 1)

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

        # вызываю функцию для получения списка групп
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
                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)

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

                    choose_subject_l.deleteLater()
                    choose_subject_l.setParent(None)
                    choose_subject_cb.deleteLater()
                    choose_subject_cb.setParent(None)
                except NameError:
                    pass

                choose_gb.adjustSize()
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
                choose_semester_l.deleteLater()
                choose_semester_l.setParent(None)
                choose_semester_cb.deleteLater()
                choose_semester_cb.setParent(None)

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

            choose_gb.adjustSize()
            self.adjustSize()

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

                choose_gb.adjustSize()
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
        global error_id, attendance, names, dates_list, base
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
            base = logic.Subject(group_name, semester_name, subject_name)
            attendance = base.get_values_semester()
            print(attendance)
            names = sorted(base.get_names())
            print(names)
            dates_list = sorted(list(attendance.keys()))
            print(dates_list)
            self.show_table()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()

    def create_window(self):
        self.cr = CreateWindow()
        self.cr.show()
        self.close()

    def show_table(self):
        global repeat
        repeat = False
        self.tb = TableWindow()
        self.tb.show()
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


class CreateWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Добавить группу, семестр, предмет')

        # создание сетки, в которую помещаются остальные виджеты
        create_container = QtGui.QGridLayout(self)

        # создание кнопки для выхода в стартовое окно
        self.quit_button = QtGui.QPushButton(u"Вернуться")
        self.connect(self.quit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        create_container.addWidget(self.quit_button, 3, 0, 1, 1)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        create_container.addWidget(self.exit_button, 4, 0, 1, 1)

        # ================================================================

        # создание рамки для ввода группы
        create_group_gb = QtGui.QGroupBox('Группа', self)
        # добавление рамки в сетку
        create_container.addWidget(create_group_gb, 0, 0, 1, 1)

        # создание сетки для рамки "группа"
        create_group_container = QtGui.QGridLayout(create_group_gb)

        # создание сообщения о выборе группы
        choose_group_l = QtGui.QLabel(u"""Введите номер группы:""", choose_gb)
        create_group_container.addWidget(choose_group_l, 0, 0, 1, 1)

        # создание строки для ввода номера группы
        choose_group_le = QtGui.QLineEdit()
        create_group_container.addWidget(choose_group_le, 1, 0, 1, 1)

        # создание кнопки добавления
        self.add_group_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_group_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        create_group_container.addWidget(self.add_group_button, 2, 0, 1, 1)

        # ================================================================

        # создание рамки для ввода семестра
        create_semester_gb = QtGui.QGroupBox('Семестр', self)
        # добавление рамки в сетку
        create_container.addWidget(create_semester_gb, 1, 0, 1, 1)

        # создание сетки для рамки "группа"
        create_semester_container = QtGui.QGridLayout(create_semester_gb)

        # создание сообщения о выборе группы
        choose_semester_l = QtGui.QLabel(u"""Введите номер группы:""", choose_gb)
        create_semester_container.addWidget(choose_semester_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_group_cb = QtGui.QComboBox(choose_gb)
        choose_group_cb.clear()

        # добавляет пустую строку, чтобы изначально группа не была выбрана
        choose_group_cb.addItem(None)

        # вызываю функцию для получения списка групп
        list_of_groups = logic.get_groups()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            choose_group_cb.addItem(str(i))
        choose_group_cb.setEditable(False)

        # создание строки для ввода номера семестра
        choose_semester_le = QtGui.QLineEdit()
        create_semester_container.addWidget(choose_semester_le, 1, 0, 1, 1)

        # создание кнопки добавления
        self.add_semester_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_semester_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        create_semester_container.addWidget(self.add_semester_button, 2, 0, 1, 1)

        # ================================================================

        # создание рамки для ввода предмета
        create_subject_gb = QtGui.QGroupBox('Предмет', self)
        # добавление рамки в сетку
        create_container.addWidget(create_subject_gb, 2, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_group_cb = QtGui.QComboBox(choose_gb)
        choose_group_cb.clear()


class TableWindow(QtGui.QMainWindow):
    def __init__(self):
        global table_widget, attendance, dates_list
        print(group_name, semester_name, subject_name)
        QtGui.QMainWindow.__init__(self)

        # настройки окна
        self.setWindowTitle('Контроль посещаемости')

        # отображается меню
        self.menuBar()

        # создание виджета таблицы
        table_widget = QtGui.QTableWidget(len(names), len(attendance.keys()))
        self.setCentralWidget(table_widget)

        # заполнение шапок
        table_widget.setHorizontalHeaderLabels(dates_list)
        table_widget.setVerticalHeaderLabels(list(names))

        # заполнение ячеек
        for m, date in enumerate(dates_list):
            print(attendance[date])
            for n, item in enumerate(names):
                check_item = QtGui.QTableWidgetItem(attendance[date].get(item))
                check_item.setFlags(QtCore.Qt.ItemIsEnabled)
                check_item.setTextAlignment(QtCore.Qt.AlignCenter)
                table_widget.setItem(n, m, check_item)

        table_widget.resizeColumnsToContents()
        table_widget.resizeRowsToContents()

        # создается строка статуса
        self.statusBar()

        # добавление кнопки отметки
        check_button = QtGui.QAction(u"Отметить", self)
        check_button.setShortcut('Ctrl+C')
        check_button.setStatusTip('Зайти под своим табельным номером и отметить себя')
        self.connect(check_button, QtCore.SIGNAL('triggered()'), self.check_login)

        # добавление кнопки преподавателя
        super_button = QtGui.QAction(u"Зайти как препод", self)
        super_button.setShortcut('Ctrl+M')
        super_button.setStatusTip('Зайти как староста или преподаватель')
        self.connect(super_button, QtCore.SIGNAL('triggered()'), self.super)

        # добавление кнопки смены группы
        change_group_button = QtGui.QAction(u"Выбрать другую группу или семестр", self)
        change_group_button.setShortcut('Ctrl+G')
        change_group_button.setStatusTip('Вернуться в меню выбора группы')
        self.connect(change_group_button, QtCore.SIGNAL('triggered()'), self.change_group)

        # добавление кнопки выхода
        exit_button = QtGui.QAction(u"Выйти", self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Выйти из программы')
        self.connect(exit_button, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        # создание панели инструментов
        menu_bar = self.menuBar()

        # создание кнопки файл
        file = menu_bar.addMenu('&Меню')

        # добавление кнопки выхода в меню
        file.addAction(check_button)
        file.addAction(super_button)
        file.addAction(change_group_button)
        file.addAction(exit_button)

    def check_login(self):
        self.chlg = CheckLoginWindow()
        self.chlg.show()

    def super(self):
        pass

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


class CheckLoginWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Введите свой табельный номер')

        # создание сетки, в которую помещаются остальные виджеты
        login_container = QtGui.QGridLayout(self)

        # ================================================================

        # создание рамки для ввода группы
        create_group_gb = QtGui.QGroupBox('Группа', self)
        # добавление рамки в сетку
        login_container.addWidget(create_group_gb, 0, 0, 1, 1)

        # создание сетки для рамки
        login_pass_container = QtGui.QGridLayout(create_group_gb)

        # создание сообщения о вводе логина
        login_l = QtGui.QLabel(u"""Введите свой табельный номер:""", choose_gb)
        login_pass_container.addWidget(login_l, 0, 0, 1, 1)

        # создание строки для ввода номера группы
        login_le = QtGui.QLineEdit()
        login_pass_container.addWidget(login_le, 1, 0, 1, 1)

        # создание кнопки добавления
        self.add_group_button = QtGui.QPushButton(u"Принять")
        self.connect(self.add_group_button, QtCore.SIGNAL('clicked()'), self.check)
        login_container.addWidget(self.add_group_button, 2, 0, 1, 1)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        login_container.addWidget(self.exit_button, 3, 0, 1, 1)

    def check(self):
        self.ch = CheckWindow()
        self.ch.show()
        self.close()

class CheckWindow(QtGui.QTableWidget):
    def __init__(self):
        global attendance, dates_list, date_today, item_cb
        print(group_name, semester_name, subject_name)
        QtGui.QTableWidget.__init__(self, len(names), 1)
        date_today = '1.1'
        date_now = []
        date_now.append(date_today)

        for i in range(len(dates_list)):
            if dates_list[i] == date_now:
                print(i)


        # заполнение шапок
        print(date_now)
        self.setHorizontalHeaderLabels(date_now)
        self.setVerticalHeaderLabels(list(names))

        # # заполнение ячеек
        # for m, name in enumerate(names):
        #     for n, item in enumerate(attendance[name]):
        #         check_item = QtGui.QTableWidgetItem(item)
        #         check_item.setTextAlignment(QtCore.Qt.AlignCenter)
        #         self.setItem(m, n, check_item)
        print(self.rowCount())
        cb_list = QtGui.QListWidget(self)
        for i in range(self.rowCount()):
            item_cb = QtGui.QComboBox(self)
            item_cb.addItem(None)
            for j in [0,1,2,3]:
                item_cb.addItem(str(j))
            item_cb.setEditable(False)
            item_cb.currentIndexChanged[str].connect(self.check_in)
            cb_list.setItemWidget(QtGui.QListWidgetItem, item_cb)
            # при выборе значения из списка вызывает функцию замены значения посещения
            self.setCellWidget(i, 0, item_cb)

        self.resizeColumnsToContents()

    def check_in(self, code):
        print(code)
        index = self.indexAt(item_cb.pos())
        print(index.row(), index.column())
        #student_num = base.get_student_info(name=self.verticalHeaderItem(int(row)).text())
        #print(student_num)
        #base.check_in(date_today, student_num, code)


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
