#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : app
# Author        : Sun YiFan-Movoid
# Time          : 2024/5/26 18:47
# Description   : 
"""
from pathlib import Path

from PySide6.QtCore import Qt
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
        self.main.findChild(QAction, 'menu_file_open').triggered.connect(self.event_read_xml)

    def event_read_xml(self, event):
        file, _ = QFileDialog.getOpenFileName(self.main)
        if file:
            self.read_xml(file)

    def read_xml(self, xml_path):
        path = Path(xml_path)
        if path.is_file():
            self.label.read(str(path))
            self.main.status_signal.emit(f'成功读取{str(path)}', 0)
            self.label.use_labels('__init__')
            self.refresh_label()
            self.refresh_body()
            self.refresh_now()
        else:
            self.main.status_signal.emit(f'{str(path)}不是个有效的xml文件', 0)

    def refresh_label(self):
        body_label_list: QListWidget = self.main.findChild(QListWidget, 'body_label_list')
        body_label_list.clear()
        now_label_list: QListWidget = self.main.findChild(QListWidget, 'now_label_list')
        now_label_list.clear()
        for k, v in self.label.label.items():
            check_state = Qt.CheckState(2 if k in self.label.label_in_use else 0)
            box = QCheckBox(k)
            item = QListWidgetItem()
            body_label_list.addItem(item)
            body_label_list.setItemWidget(item, box)
            box.setCheckState(check_state)
            box.stateChanged.connect(lambda: self.label_list_click(body_label_list))

            box = QCheckBox(k)
            item = QListWidgetItem()
            now_label_list.addItem(item)
            now_label_list.setItemWidget(item, box)
            box.setCheckState(check_state)
            box.stateChanged.connect(lambda: self.label_list_click(now_label_list))
        body_label_list.itemClicked.connect(lambda: self.label_list_click(body_label_list))
        now_label_list.itemClicked.connect(lambda: self.label_list_click(now_label_list))

    def refresh_body(self):
        label_body_list: QListWidget = self.main.findChild(QListWidget, 'label_body_list')
        label_body_list.clear()
        now_body_list: QListWidget = self.main.findChild(QListWidget, 'now_body_list')
        now_body_list.clear()
        for k, v in self.label.body.items():
            check_state = Qt.CheckState(2 if k in self.label.body_in_use else 0)
            box = QCheckBox(k)
            item = QListWidgetItem()
            label_body_list.addItem(item)
            label_body_list.setItemWidget(item, box)
            box.setCheckState(check_state)
            box.stateChanged.connect(lambda: self.body_list_click(label_body_list))

            box = QCheckBox(k)
            item = QListWidgetItem()
            now_body_list.addItem(item)
            now_body_list.setItemWidget(item, box)
            box.setCheckState(check_state)
            box.stateChanged.connect(lambda: self.body_list_click(now_body_list))
        label_body_list.itemClicked.connect(lambda: self.body_list_click(label_body_list))
        now_body_list.itemClicked.connect(lambda: self.body_list_click(now_body_list))

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

    def label_list_click(self, label_list: QListWidget):
        new_labels = []
        for index in range(label_list.count()):
            label_item = label_list.item(index)
            checkbox: QCheckBox = label_list.itemWidget(label_item)
            if checkbox.checkState().value == 2:
                new_labels.append(checkbox.text())
        self.label.use_labels(new_labels, clear_now=True)
        self.refresh_label()
        self.refresh_body()
        self.refresh_now()

    def body_list_click(self, body_list: QListWidget):
        new_bodies = []
        for index in range(body_list.count()):
            body_item = body_list.item(index)
            checkbox: QCheckBox = body_list.itemWidget(body_item)
            if checkbox.checkState().value == 2:
                new_bodies.append(checkbox.text())
        self.label.use_bodies(new_bodies, clear_now=True)
        self.refresh_body()
        self.refresh_now()
