#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : app
# Author        : Sun YiFan-Movoid
# Time          : 2024/5/24 2:09
# Description   : 
"""
import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QGridLayout, QTabWidget, QWidget, QGroupBox, QListWidget, QTreeWidget, QTextEdit, QLineEdit, QApplication, QMenuBar, QStatusBar


class MainWindow(QMainWindow):
    status_signal = Signal(str, int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.init_menu()
        self.init_status()
        self.init_tab_label()
        self.init_tab_body()
        self.init_tab_now()
        screen_rect = QApplication.primaryScreen().geometry()
        self.setGeometry(int(screen_rect.width() * 0.2), int(screen_rect.height() * 0.2), int(screen_rect.width() * 0.6), int(screen_rect.height() * 0.6))
        main_table = QTabWidget(self)
        self.setCentralWidget(main_table)
        main_table.addTab(self.tab_now, 'now')
        main_table.addTab(self.tab_label, 'label')
        main_table.addTab(self.tab_body, 'body')

        self.show()

    def init_menu(self):
        self.menu = QMenuBar(self)
        self.setMenuBar(self.menu)
        menu_file = self.menu.addMenu('文件')
        menu_file_open = QAction('打开', self)
        menu_file_open.setObjectName('menu_file_open')
        menu_file.addAction(menu_file_open)

    def init_status(self):
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status_signal.connect(self.status_show)

    def init_tab_label(self):
        self.tab_label = QWidget(self)
        grid = QGridLayout(self.tab_label)
        self.tab_label.setLayout(grid)

    def init_tab_body(self):
        self.tab_body = QWidget(self)

    def init_tab_now(self):
        self.tab_now = QWidget(self)
        grid = QGridLayout(self.tab_now)
        grid.setColumnStretch(2, 4)
        self.tab_now.setLayout(grid)
        label_group = QGroupBox('label', self.tab_now)
        body_group = QGroupBox('body', self.tab_now)
        grid.addWidget(label_group, 0, 0)
        grid.addWidget(body_group, 0, 1)
        now_group = QGroupBox('now', self.tab_now)
        grid.addWidget(now_group, 0, 2)

        label_layout = QGridLayout(label_group)
        label_list = QListWidget(label_group)
        label_list.setObjectName('now_label_list')
        label_layout.addWidget(label_list)

        body_layout = QGridLayout(body_group)
        body_list = QListWidget(body_group)
        body_list.setObjectName('now_body_list')
        body_layout.addWidget(body_list)

        now_layout = QGridLayout(now_group)
        now_tree = QTreeWidget(now_group)
        now_tree.setObjectName('now_now_tree')
        now_layout.addWidget(now_tree, 0, 0, 10, 1)
        now_tree.setHeaderLabels(['key', 'value'])

        now_search_input = QLineEdit(now_group)
        now_search_input.setObjectName('now_now_search_input')
        now_layout.addWidget(now_search_input, 0, 1)

        now_search_tree = QTreeWidget(now_group)
        now_search_tree.setObjectName('now_now_search_tree')
        now_layout.addWidget(now_search_tree, 1, 1, 9, 1)
        now_search_tree.setHeaderLabels(['key', 'value'])

    @Slot(str, int)
    def status_show(self, text, timeout=5000):
        self.status.showMessage(text, timeout)
