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
        QtGui.QWidget.__init__(self)

        global choose_container
        global choose_group_cb, choose_semester_cb, choose_subject_cb    # выпадающие списки
        global repeater

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

        # создание рамки для выбора группы/семестра/предмета
        choose_gb = QtGui.QGroupBox('Выберите группу, семестр и предмет', self)
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

        # добавление выпадающего списка о выборе группы в сетку
        choose_container.addWidget(choose_group_cb, 1, 0, 1, 1)

        # вызываю функцию для получения списка групп
        list_of_groups = logic.get()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            choose_group_cb.addItem(str(i))

        choose_group_cb.setEditable(False)

        # ============================================================================

        # создание сообщения о выборе семестра
        choose_semester_l = QtGui.QLabel(u"""Выберите номер семестра:""", choose_gb)
        choose_container.addWidget(choose_semester_l, 2, 0, 1, 1)

        # создание выпадающего списка о выборе семестра
        choose_semester_cb = QtGui.QComboBox(choose_gb)

        choose_semester_cb.setEditable(False)
        choose_semester_cb.setEnabled(False)

        # добавление выпадающего списка о выборе семестра в сетку
        choose_container.addWidget(choose_semester_cb, 3, 0, 1, 1)

        # ============================================================================

        # создание сообщения о выборе группы
        choose_subject_l = QtGui.QLabel(u"""Выберите предмет:""", choose_gb)
        choose_container.addWidget(choose_subject_l, 4, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        choose_subject_cb = QtGui.QComboBox(choose_gb)

        # делает неактивным и неизменяемым
        choose_subject_cb.setEditable(False)
        choose_subject_cb.setEnabled(False)

        # добавление списка в сетку
        choose_container.addWidget(choose_subject_cb, 5, 0, 1, 1)

        print(repeat)
        if repeat is True:
            repeater += 1
            choose_group_cb.setCurrentIndex(choose_group_cb.findText(group_name_re))
            self.choose_semester(group_name_re)

        # при выборе значения из списка вызывает функцию по поиску семестров
        choose_group_cb.currentIndexChanged[str].connect(self.choose_semester)

        # self.setFixedSize(self.sizeHint())

    def choose_semester(self, group_index):
        global choose_container     # главная сетка
        global group_name, semester_name, subject_name  # выбранные значения
        global group_name_re, semester_name_re     # сохраненные значения
        global repeater     # счетчик количества использований
        print('qwertyuiopasdfghjklzxcvbnm,.')
        group_name = group_index
        group_name_re = group_name

        print(repeat, group_name, semester_name, subject_name)

        # семестр обнуляется
        semester_name = None
        subject_name = None

        print(group_name)

        if bool(group_name) is True:
            # делает активным
            choose_semester_cb.setEnabled(True)
            choose_semester_cb.clear()
            # добавляет пустую строку, чтобы изначально группа не была выбрана
            choose_semester_cb.addItem(None)
            """
            Вызываю функцию для получения списка семестров
            Оправляю номер группы
            Должен получить список с семестрами
            """
            list_of_semester = logic.get(group_name)
            # добавляет в выпадающий список семестры
            for i in list_of_semester:
                choose_semester_cb.addItem(str(i))

            if repeat is True:
                repeater += 1
                choose_semester_cb.setCurrentIndex(choose_semester_cb.findText(semester_name_re))
                self.choose_subject(semester_name_re)

            # при выборе значения из списка вызывает функцию по поиску семестров
            choose_semester_cb.currentIndexChanged[str].connect(self.choose_subject)

            semester_name_re = None
        else:
            # делает неактивным
            choose_semester_cb.setEnabled(False)
            choose_semester_cb.setCurrentIndex(0)

    def choose_subject(self, semester_index):
        global choose_container     # главная сетка
        global group_name, semester_name, subject_name  # выбранные значения
        global group_name_re, semester_name_re, subject_name_re     # сохраненные значения
        global repeater     # счетчик количества использований

        semester_name = semester_index
        semester_name_re = semester_name

        print(semester_name)

        # предмет обнуляется
        subject_name = None
        if bool(semester_name) is True:
            # делает активным
            choose_subject_cb.setEnabled(True)
            choose_subject_cb.clear()

            # добавляет пустую строку, чтобы изначально группа не была выбрана
            choose_subject_cb.addItem(None)
            """
            Вызываю функцию для получения списка семестров
            Оправляю номер группы
            Должен получить список с семестрами
            """
            try:
                list_of_subject = logic.get((group_name, semester_name))
                # добавляет в выпадающий список семестры
                print(logic.get((group_name, semester_name)))
                for i in list_of_subject:
                    choose_subject_cb.addItem(str(i))
            except logic.WrongDataError:
                pass

            choose_subject_cb.setEditable(False)

            if repeat is True:
                repeater += 1
                choose_subject_cb.setEnabled(True)
                choose_subject_cb.setCurrentIndex(choose_subject_cb.findText(subject_name_re))
                self.subject(subject_name_re)

            # при выборе значения из списка вызывает функцию по поиску семестров
            choose_subject_cb.currentIndexChanged[str].connect(self.subject)

            subject_name_re = None
        else:
            # делает неактивным
            choose_subject_cb.setEnabled(False)
            choose_subject_cb.setCurrentIndex(0)

    def subject(self, subject_index):
        global subject_name, repeat
        subject_name = subject_index
        print(repeat, group_name, semester_name, subject_name)

        if repeater == 3:
            repeat = False
        print(repeater, repeat)

    def open(self):
        global error_id, attendance, names, base
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
        elif error_id == 3:
            self.setText(u"Права студента не выбраны")
        elif error_id == 4:
            self.setText(u"Введите табельный номер студента")
        elif error_id == 5:
            self.setText(u"Введите имя студента")
        elif error_id == 6:
            self.setText(u"Введите название предмета")
        elif error_id == 7:
            self.setText(u"Семестр не выбран")
        elif error_id == 8:
            self.setText(u"Группа не выбрана")
        elif error_id == 9:
            self.setText(u"Введите номер семестра")
        elif error_id == 10:
            self.setText(u"Группа не выбрана")
        elif error_id == 11:
            self.setText(u"Введите номер группы")
        elif error_id == 12:
            self.setText(u"Сегодня занятий нет")
        elif error_id == 13:
            self.setText(u"Табельный номер должен состоять из цифр")
        elif error_id == 14:
            self.setText(u"Студент с таким табельным номером не найден")
        elif error_id == 15:
            self.setText(u"У вас не хватает прав")

        # настройки окна
        self.setWindowTitle('Ошибка')
        self.setIcon(QtGui.QMessageBox.Warning)
        self.addButton('ОК', QtGui.QMessageBox.AcceptRole)


class CreateWindow(QtGui.QWidget):
    def __init__(self):
        global create_choose_group_cb, create_choose_group_sem_cb, create_choose_semester_cb  # выпадающие списки
        global create_choose_group_le, create_choose_semester_le, create_choose_subject_le  # строки ввода
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Добавить группу, семестр, предмет')

        # создание сетки, в которую помещаются остальные виджеты
        create_container = QtGui.QGridLayout(self)

        # создание кнопки для выхода в стартовое окно
        self.quit_button = QtGui.QPushButton(u"Вернуться")
        self.connect(self.quit_button, QtCore.SIGNAL('clicked()'), self.return_to_menu)
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

        # --------------------------------------------------------------------------------

        # создание сообщения о вводе группы
        create_choose_group_l = QtGui.QLabel(u"""Введите номер группы:""", create_group_gb)
        create_group_container.addWidget(create_choose_group_l, 0, 0, 1, 1)

        # создание строки для ввода номера группы
        create_choose_group_le = QtGui.QLineEdit()
        create_group_container.addWidget(create_choose_group_le, 1, 0, 1, 1)

        # создание кнопки добавления
        self.add_group_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_group_button, QtCore.SIGNAL('clicked()'), self.create_add_group)
        create_group_container.addWidget(self.add_group_button, 2, 0, 1, 1)

        # =================================================================================
        # =================================================================================

        # создание рамки для ввода семестра
        create_semester_gb = QtGui.QGroupBox('Семестр', self)
        # добавление рамки в сетку
        create_container.addWidget(create_semester_gb, 1, 0, 1, 1)

        # создание сетки для рамки "семестр"
        create_semester_container = QtGui.QGridLayout(create_semester_gb)

        # --------------------------------------------------------------------------------

        # создание сообщения о выборе группы
        create_choose_semester_l = QtGui.QLabel(u"""Выберите номер группы:""", create_group_gb)
        create_semester_container.addWidget(create_choose_semester_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        create_choose_group_cb = QtGui.QComboBox(create_group_gb)
        create_choose_group_cb.clear()

        # добавляет пустую строку, чтобы изначально группа не была выбрана
        create_choose_group_cb.addItem(None)

        # вызываю функцию для получения списка групп
        list_of_groups = logic.get()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            create_choose_group_cb.addItem(str(i))

        create_choose_group_cb.setEditable(False)

        create_semester_container.addWidget(create_choose_group_cb, 1, 0, 1, 1)

        # --------------------------------------------------------------------------------

        # создание сообщения о вводе семестра
        create_choose_semester_l = QtGui.QLabel(u"""Введите номер семестра:""", create_group_gb)
        create_semester_container.addWidget(create_choose_semester_l, 2, 0, 1, 1)

        # создание строки для ввода номера семестра
        create_choose_semester_le = QtGui.QLineEdit()
        create_semester_container.addWidget(create_choose_semester_le, 3, 0, 1, 1)

        # создание кнопки добавления
        self.add_semester_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_semester_button, QtCore.SIGNAL('clicked()'), self.create_add_semester)
        create_semester_container.addWidget(self.add_semester_button, 4, 0, 1, 1)

        # =================================================================================
        # =================================================================================

        # создание рамки для ввода предмета
        create_subject_gb = QtGui.QGroupBox('Предмет', self)
        # добавление рамки в сетку
        create_container.addWidget(create_subject_gb, 2, 0, 1, 1)

        # создание сетки для рамки "предмет"
        create_subject_container = QtGui.QGridLayout(create_subject_gb)

        # --------------------------------------------------------------------------------

        # создание сообщения о выборе группы
        create_choose_subject_l = QtGui.QLabel(u"""Выберите номер группы:""", create_group_gb)
        create_subject_container.addWidget(create_choose_subject_l, 0, 0, 1, 1)

        # создание выпадающего списка о выборе группы
        create_choose_group_sem_cb = QtGui.QComboBox(create_group_gb)
        create_choose_group_sem_cb.clear()

        # добавляет пустую строку, чтобы изначально группа не была выбрана
        create_choose_group_sem_cb.addItem(None)

        # добавление выпадающего списка о выборе группы в сетку
        create_subject_container.addWidget(create_choose_group_sem_cb, 1, 0, 1, 1)

        # при выборе значения из списка вызывает функцию по поиску семестров
        create_choose_group_sem_cb.currentIndexChanged[str].connect(self.create_choose_semester)

        # вызываю функцию для получения списка групп
        list_of_groups = logic.get()
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            create_choose_group_sem_cb.addItem(str(i))

        create_choose_group_sem_cb.setEditable(False)

        # --------------------------------------------------------------------------------

        # создание сообщения о выборе семестра
        create_choose_semester_l = QtGui.QLabel(u"""Выберите номер семестра:""", create_group_gb)
        create_subject_container.addWidget(create_choose_semester_l, 2, 0, 1, 1)

        # создание выпадающего списка о выборе семестра
        create_choose_semester_cb = QtGui.QComboBox(create_group_gb)

        create_choose_semester_cb.setEditable(False)
        create_choose_semester_cb.setEnabled(False)

        # добавление выпадающего списка о выборе семестра в сетку
        create_subject_container.addWidget(create_choose_semester_cb, 3, 0, 1, 1)

        # --------------------------------------------------------------------------------

        # создание сообщения о вводе предмета
        create_choose_subject_l = QtGui.QLabel(u"""Введите название предмета:""", create_group_gb)
        create_subject_container.addWidget(create_choose_subject_l, 4, 0, 1, 1)

        # создание строки для ввода предмета
        create_choose_subject_le = QtGui.QLineEdit()
        create_subject_container.addWidget(create_choose_subject_le, 5, 0, 1, 1)

        # --------------------------------------------------------------------------------

        # создание кнопки добавления
        self.add_subject_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_subject_button, QtCore.SIGNAL('clicked()'), self.create_add_subject)
        create_subject_container.addWidget(self.add_subject_button, 6, 0, 1, 1)
    # TODO: Добавить окна с ошибками

    def create_choose_semester(self, create_group_index):
        create_group_name = create_group_index

        if bool(create_group_name) is True:
            # делает активным
            create_choose_semester_cb.setEnabled(True)
            create_choose_semester_cb.clear()
            # добавляет пустую строку, чтобы изначально группа не была выбрана
            create_choose_semester_cb.addItem(None)
            """
            Вызываю функцию для получения списка семестров
            Оправляю номер группы
            Должен получить список с семестрами
            """
            list_of_semester = logic.get(create_group_name)
            # добавляет в выпадающий список семестры
            for i in list_of_semester:
                create_choose_semester_cb.addItem(str(i))
        else:
            # делает неактивным
            create_choose_semester_cb.setEnabled(False)
            create_choose_semester_cb.setCurrentIndex(0)

    def create_add_group(self):
        global error_id
        error_id = None
        create_choose_group_text = create_choose_group_le.text()
        if bool(create_choose_group_text) is True:
            logic.add(create_choose_group_text)
        else:
            error_id = 11

        # обновление списков групп

        # вызываю функцию для получения списка групп
        list_of_groups = logic.get()

        create_choose_group_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        create_choose_group_cb.addItem(None)
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            create_choose_group_cb.addItem(str(i))

        create_choose_group_sem_cb.clear()
        # добавляет пустую строку, чтобы изначально группа не была выбрана
        create_choose_group_sem_cb.addItem(None)
        # добавляет в выпадающий список группы
        for i in list_of_groups:
            create_choose_group_sem_cb.addItem(str(i))

    def create_add_semester(self):
        global error_id
        error_id = None
        create_choose_group_chosen = create_choose_group_cb.currentText()
        create_choose_semester_text = create_choose_semester_le.text()
        if bool(create_choose_group_chosen) is True:
            if bool(create_choose_semester_text) is True:
                logic.add(create_choose_group_chosen,
                          semester=create_choose_semester_text)
            else:
                error_id = 9
        else:
            error_id = 10

    def create_add_subject(self):
        global error_id
        error_id = None
        create_choose_group_chosen = create_choose_group_sem_cb.currentText()
        create_choose_semester_chosen = create_choose_semester_cb.currentText()
        create_choose_subject_text = create_choose_subject_le.text()
        if bool(create_choose_group_chosen) is True:
            if bool(create_choose_semester_chosen) is True:
                if bool(create_choose_subject_text) is True:
                    logic.add(create_choose_group_chosen,
                              semester=create_choose_semester_chosen,
                              subject=create_choose_subject_text)
                else:
                    error_id = 6
            else:
                error_id = 7
        else:
            error_id = 8
        if error_id is not None:
            # если ошибка возникла, окрывается окно с ошибкой
            self.error_window()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()

    def return_to_menu(self):
        global repeat, group_name_re, semester_name_re, subject_name_re, repeater
        repeat = True
        repeater = 0
        group_name_re = group_name
        semester_name_re = semester_name
        subject_name_re = subject_name
        self.rtrn = MainDialog()
        self.rtrn.show()
        self.close()


class TableWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        global table_widget
        global base, attendance, dates_list, names
        global check_self_button, check_button, admin_button

        print(group_name, semester_name, subject_name)

        base = logic.Subject(group_name, semester_name, subject_name)
        attendance = base.get_values_semester()
        print(attendance)
        names = sorted(base.get_names())
        print(names)

        dates_list = sorted(list(attendance.keys()))
        print(dates_list)

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

        # добавление кнопки отметки себя
        check_self_button = QtGui.QAction(u"Отметить себя", self)
        check_self_button.setShortcut('Ctrl+C')
        check_self_button.setStatusTip('Зайти под своим табельным номером и отметить себя')
        self.connect(check_self_button, QtCore.SIGNAL('triggered()'), self.check_login)

        # добавление кнопки отметки всех
        check_button = QtGui.QAction(u"Отметить всех", self)
        check_button.setShortcut('Ctrl+D')
        check_button.setStatusTip('Зайти как староста или преподаватель и отметить группу')
        self.connect(check_button, QtCore.SIGNAL('triggered()'), self.check_login)

        # добавление кнопки админа
        admin_button = QtGui.QAction(u"Зайти в режим редактирования", self)
        admin_button.setShortcut('Ctrl+E')
        admin_button.setStatusTip('Зайти с правами администратора и редактировать таблицу')
        self.connect(admin_button, QtCore.SIGNAL('triggered()'), self.check_login)

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
        file.addAction(check_self_button)
        file.addAction(check_button)
        file.addAction(admin_button)
        file.addAction(change_group_button)
        file.addAction(exit_button)

        table_widget.resize(table_widget.sizeHint())
        
    def sizeHint(self):
        width = 0
        for i in range(table_widget.columnCount()):
            width += table_widget.columnWidth(i)

        width += table_widget.verticalHeader().sizeHint().width()

        width += table_widget.verticalScrollBar().sizeHint().width()
        width += table_widget.frameWidth()*2

        return QtCore.QSize(width,table_widget.height())

    def check_login(self):
        global master_index
        master_index = self.sender()
        self.chlg = CheckLoginWindow()
        self.chlg.show()
        self.close()

    def change_group(self):
        global repeat, group_name_re, semester_name_re, subject_name_re, repeater
        repeat = True
        repeater = 0
        group_name_re = group_name
        semester_name_re = semester_name
        print(semester_name_re)
        subject_name_re = subject_name
        self.chng = MainDialog()
        self.chng.show()
        self.close()


class CheckLoginWindow(QtGui.QWidget):
    def __init__(self):
        global login_le
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Введите свой табельный номер')

        # создание сетки, в которую помещаются остальные виджеты
        login_container = QtGui.QGridLayout(self)

        # ================================================================

        # создание рамки для ввода группы
        login_gb = QtGui.QGroupBox(u"""Введите свой табельный номер:""", self)
        # добавление рамки в сетку
        login_container.addWidget(login_gb, 0, 0, 1, 1)

        # создание сетки для рамки
        login_pass_container = QtGui.QGridLayout(login_gb)

        # создание строки для ввода номера группы
        login_le = QtGui.QLineEdit()
        login_pass_container.addWidget(login_le, 0, 0, 1, 1)

        # создание кнопки добавления
        self.add_group_button = QtGui.QPushButton(u"Принять")
        self.connect(self.add_group_button, QtCore.SIGNAL('clicked()'), self.check)
        login_container.addWidget(self.add_group_button, 1, 0, 1, 1)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        login_container.addWidget(self.exit_button, 2, 0, 1, 1)

    def check(self):
        global error_id
        error_id = None
        print(login_le.text())
        date_today = time.strftime("%d") + '.' + time.strftime("%m") + '.' + time.strftime("%Y")
        print(date_today)
        if date_today not in dates_list:
            error_id = 12
        else:
            if bool(login_le.text()) is True:
                try:
                    student_num = int(login_le.text())
                    if bool(base.get_student_info(pers_number=student_num)) is True:
                        if master_index == check_self_button:
                            base.check_in(date_today, student_num, code=1)
                            self.tb = TableWindow()
                            self.tb.show()
                            self.close()
                            # TODO: Добавить окно с сообщением об успешном завершении операции
                        elif master_index == check_button:
                            if base.get_student_info(pers_number=student_num, right=True) in (1, 2):
                                self.ch = CheckWindow()
                                self.ch.show()
                                self.close()
                            else:
                                error_id = 15
                        elif master_index == admin_button:
                            print(base.get_student_info(pers_number=student_num, right=True))
                            if base.get_student_info(pers_number=student_num, right=True) == 2:
                                self.ch = AdminWindow()
                                self.ch.show()
                                self.close()
                            else:
                                error_id = 15
                    else:
                        error_id = 14
                except ValueError:
                    error_id = 13

        if error_id is not None:
            # если ошибка возникла, окрывается окно с ошибкой
            self.error_window()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()


class CheckWindow(QtGui.QWidget):
    def __init__(self):
        global attendance, dates_list, date_today, item_cb, table_check_widget
        print(group_name, semester_name, subject_name)
        QtGui.QWidget.__init__(self)

        # создание сетки, в которую помещаются остальные виджеты
        table_check_container = QtGui.QGridLayout(self)

        table_check_widget = QtGui.QTableWidget(len(names), 1, self)
        table_check_container.addWidget(table_check_widget, 0, 0, 1, 1)

        ok_exit_button = QtGui.QPushButton(u"Принять")
        self.connect(ok_exit_button, QtCore.SIGNAL('clicked()'), self.ok_exit)
        table_check_container.addWidget(ok_exit_button, 1, 0, 1, 1)

        # self.setCentralWidget(table_check_widget)

        date_today = time.strftime("%d") + '.' + time.strftime("%m") + '.' + time.strftime("%Y")
        date_now = []
        date_now.append(date_today)

        for i in range(len(dates_list)):
            if dates_list[i] == date_now:
                print(i)

        # заполнение шапок
        table_check_widget.setHorizontalHeaderLabels(date_now)
        table_check_widget.setVerticalHeaderLabels(list(names))

        list_of_cb =[]
        print(table_check_widget.rowCount())
        for i in range(table_check_widget.rowCount()):
            item_cb = QtGui.QComboBox(table_check_widget)
            list_of_cb.append(item_cb)
            for j in [0, 1, 2, 3]:
                item_cb.addItem(str(j))
            item_cb.setEditable(False)
            item_cb.currentIndexChanged[str].connect(self.check_in)

            # при выборе значения из списка вызывает функцию замены значения посещения
            table_check_widget.setCellWidget(i, 0, item_cb)
        print(list_of_cb)

        # заполнение ячеек
        print(attendance[date_today])
        for m, cb in enumerate(list_of_cb):
            for n, item in enumerate(names):
                if n == m:
                    check_now_item = attendance[date_today].get(item)
                    cb.setCurrentIndex(cb.findText(check_now_item))

        table_check_widget.resizeColumnsToContents()

    def check_in(self, code):
        index = self.sender()
        index = table_check_widget.indexAt(index.pos())
        row = index.row()
        student_num = base.get_student_info(name=table_check_widget.verticalHeaderItem(int(row)).text())
        base.check_in(date_today, student_num, code)

    def ok_exit(self):
        self.tb = TableWindow()
        self.tb.show()
        self.close()

    def closeEvent(self, event):
        self.tb = TableWindow()
        self.tb.show()
        self.close()


class AdminWindow(QtGui.QWidget):
    def __init__(self):
        global calendar  # добавление даты
        global student_name_le, student_id_le, student_right_cb  # добавление студента
        QtGui.QWidget.__init__(self)

        # название окна
        self.setWindowTitle('Добавить студента или дату')

        # создание сетки, в которую помещаются остальные виджеты
        admin_container = QtGui.QGridLayout(self)

        # создание кнопки для выхода
        self.exit_button = QtGui.QPushButton(u"Выйти")
        self.connect(self.exit_button, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        admin_container.addWidget(self.exit_button, 2, 0, 1, 1)

        # ================================================================

        # создание рамки для ввода группы
        add_student_gb = QtGui.QGroupBox('Студент', self)
        # добавление рамки в сетку
        admin_container.addWidget(add_student_gb, 0, 0, 1, 1)

        # создание сетки для рамки "группа"
        add_student_container = QtGui.QGridLayout(add_student_gb)

        # --------------------------------------------------------------------------------

        # создание сообщения о вводе имени студента
        student_name_l = QtGui.QLabel(u"""Введите имя студента:""", add_student_gb)
        add_student_container.addWidget(student_name_l, 0, 0, 1, 1)

        # создание строки для ввода имени студента
        student_name_le = QtGui.QLineEdit()
        add_student_container.addWidget(student_name_le, 1, 0, 1, 1)

        # создание сообщения о вводе табельного номера
        student_id_l = QtGui.QLabel(u"""Введите табельный номер студента:""", add_student_gb)
        add_student_container.addWidget(student_id_l, 2, 0, 1, 1)

        # создание строки для ввода табельного номера
        student_id_le = QtGui.QLineEdit()
        add_student_container.addWidget(student_id_le, 3, 0, 1, 1)

        # создание сообщения о вводе прав студента
        student_right_l = QtGui.QLabel(u"""Выберите права студента:""", add_student_gb)
        add_student_container.addWidget(student_right_l, 4, 0, 1, 1)

        # создание выпадающего списка для ввода прав студента
        student_right_cb = QtGui.QComboBox(add_student_gb)
        student_right_cb.clear()

        # добавляет пустую строку, чтобы изначально группа не была выбрана
        student_right_cb.addItem(None)

        # добавляет в выпадающий права
        for i in ['Студент', 'Староста', 'Администратор']:
            student_right_cb.addItem(str(i))

        student_right_cb.setEditable(False)

        add_student_container.addWidget(student_right_cb, 5, 0, 1, 1)

        # создание кнопки добавления
        self.add_student_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_student_button, QtCore.SIGNAL('clicked()'), self.add_student)
        add_student_container.addWidget(self.add_student_button, 6, 0, 1, 1)

        # =================================================================================
        # =================================================================================

        # создание рамки для добавления даты
        add_date_gb = QtGui.QGroupBox('Занятие', self)
        # добавление рамки в сетку
        admin_container.addWidget(add_date_gb, 1, 0, 1, 1)

        # создание сетки для рамки "занятие"
        add_date_container = QtGui.QGridLayout(add_date_gb)

        # --------------------------------------------------------------------------------

        # создание сообщения о выборе даты
        student_name_l = QtGui.QLabel(u"""Выберите дату:""", add_date_gb)
        add_date_container.addWidget(student_name_l, 0, 0, 1, 1)

        # создание календаря
        calendar = QtGui.QCalendarWidget(add_date_gb)

        add_date_container.addWidget(calendar, 1, 0, 1, 1)

        # создание кнопки добавления
        self.add_date_button = QtGui.QPushButton(u"Добавить")
        self.connect(self.add_date_button, QtCore.SIGNAL('clicked()'), self.add_date)
        add_date_container.addWidget(self.add_date_button, 2, 0, 1, 1)

    # TODO: Добавить окна с ошибками

    def add_date(self):
        if bool(calendar.selectedDate()) is True:
            date_chosen = calendar.selectedDate()
            day_chosen = str(date_chosen.day())
            month_chosen = str(date_chosen.month())
            year_chosen = str(date_chosen.year())
            if len(day_chosen) == 1:
                day_chosen = '0' + day_chosen
            if len(month_chosen) == 1:
                month_chosen = '0' + month_chosen
            date = day_chosen + '.' + month_chosen + '.' + year_chosen
            dates = []
            dates.append(date)
            print(date, type(date))
            print(dates)
            base.add_lessons(dates)

    def add_student(self):
        global error_id
        if bool(student_name_le.text()) is True:
            student_name_chosen = student_name_le.text()
            if bool(student_id_le.text()) is True:
                student_id_chosen = student_id_le.text()
                if bool(student_right_cb.currentIndex()) is True:
                    student_right_chosen = int(student_right_cb.currentIndex())-1
                    base.add_students(((student_id_chosen, student_name_chosen, student_right_chosen),))
                else:
                    error_id = 3
            else:
                error_id = 4
        else:
            error_id = 5
        if error_id is not None:
            # если ошибка возникла, окрывается окно с ошибкой
            self.error_window()

    def closeEvent(self, event):
        self.tb = TableWindow()
        self.tb.show()
        self.close()

    def error_window(self):
        em = ErrorMessage(error_id)
        em.show()
        em.exec_()


if __name__ == '__main__':
    sip.setdestroyonexit(False)
    app = QtGui.QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
