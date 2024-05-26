#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : app
# Author        : Sun YiFan-Movoid
# Time          : 2024/5/26 18:47
# Description   : 
"""
from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QFileDialog, QListWidget, QCheckBox, QListWidgetItem, QTreeWidget, QTreeWidgetItem
from movoid_xml_data import LabelData

from ..ui import MainWindow


class MainApp:
    def __init__(self):
        self.app = QApplication()
        self.main = MainWindow()
        self.label = LabelData()
        self.init()

    def exec(self):
        return self.app.exec()

    def init(self):
        self.main.findChild(QAction, 'menu_file_open').triggered.connect(self.read_xml)

    def read_xml(self, event):
        file, _ = QFileDialog.getOpenFileName(self.main)
        if file:
            path = Path(file)
            if path.is_file():
                self.label.read(str(path))
                self.main.status_signal.emit(f'成功读取{str(path)}', 5000)
                self.label.use_labels('__init__')
                self.refresh_label()
                self.refresh_body()
                self.refresh_now()

    def refresh_label(self):
        now_label_list: QListWidget = self.main.findChild(QListWidget, 'now_label_list')
        now_label_list.clear()
        for k, v in self.label.label.items():
            box = QCheckBox(k)
            item = QListWidgetItem()
            now_label_list.addItem(item)
            now_label_list.setItemWidget(item, box)

    def refresh_body(self):
        now_body_list: QListWidget = self.main.findChild(QListWidget, 'now_body_list')
        now_body_list.clear()
        for k, v in self.label.body.items():
            box = QCheckBox(k)
            item = QListWidgetItem()
            now_body_list.addItem(item)
            now_body_list.setItemWidget(item, box)

    def refresh_now(self):
        now_now_tree: QTreeWidget = self.main.findChild(QTreeWidget, 'now_now_tree')
        now_now_tree.clear()
        for k, v in self.label.now.items():
            item = QTreeWidgetItem()
            item.setText(0, k)
            if not v.has_son():
                item.setText(1, str(v.value))
            else:
                self.refresh_tree_loop(item, v)
            now_now_tree.addTopLevelItem(item)

    def refresh_tree_loop(self, parent, tree_items):
        for k, v in tree_items.items():
            item = QTreeWidgetItem()
            item.setText(0, k)
            if not v.has_son():
                item.setText(1, str(v.value))
            else:
                self.refresh_tree_loop(item, v)
            parent.addChild(item)
