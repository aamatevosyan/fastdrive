import json
import os
import textwrap
from typing import List
import time


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def get_test_path(test_id: int):
    return f'tests\\{test_id}\\'

class QuizView(QMainWindow):

    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle("Manage tags")

        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        self.setMinimumHeight(600)
        self.setMinimumWidth(900)
        self.choices = []


    def initUI(self):

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        for el in self.questions:
            widget = QWidget()
            lay = QVBoxLayout()
            lay.setAlignment(Qt.AlignCenter)
            lay.setSpacing(5)

            if el["img"] != "undefined":
                pic = QLabel()
                pixmap = QPixmap("tests\\img\\" + el["img"])
                pixmap4 = pixmap.scaled(800, 800, Qt.KeepAspectRatio)
                pic.setAlignment(Qt.AlignCenter)
                pic.setPixmap(pixmap4)
                lay.addWidget(pic)

            question_label = QTextEdit(el["question"])
            question_label.setAlignment(Qt.AlignCenter)
            question_label.setMaximumWidth(800)
            question_label.setMinimumHeight(80)
            font = QFont()
            font.setPointSize(14)
            question_label.setFont(font)
            question_label.setReadOnly(True)
            lay.addWidget(question_label)
            btngroup = QButtonGroup()
            ind = 0

            buttons = []
            for choice in el["choices"]:
                tmp = textwrap.fill(choice["text"], width=80)
                button = QRadioButton(tmp)

                font = QFont()
                font.setFamily("Sylafean")
                font.setPointSize(14)
                font.setWeight(QFont.StyleItalic)
                button.setFont(font)

                button.correct = choice["correct"]
                button.id = el["id"]
                print(button.id)
                button.ind = ind
                button.clicked.connect(lambda state, x=button: self.onChoice(x))
                #button.setMinimumHeight(100)
                button.setMaximumWidth(800)
                btngroup.addButton(button)
                lay.addWidget(button)
                ind += 1

                buttons.append(button)

            self.choices.append(buttons)

            widget.setLayout(lay)
            widget.setStyleSheet("background-color: #eeeeee; border-style: outset; border-width: 1px; border-radius: 5px; border-color: #e3dfc8; padding: 2px;")
            layout.addWidget(widget)

        self.setLayout(layout)

        self.widget.setLayout(layout)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(self.scroll)

        saveAct = QAction(QIcon('save.png'), 'Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.triggered.connect(self.onSave)

        checkAct = QAction(QIcon('find.png'), 'Check', self)
        checkAct.setShortcut('Ctrl+F')
        checkAct.triggered.connect(self.onCheck)

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(checkAct)
        self.toolbar.addAction(saveAct)

        print(len(self.questions))

    def onChoice(self, button):
        for el in self.progress_data:
            if el["id"] == button.id:
                el["selected_id"] = button.ind
                el["correct"] = button.correct

    def onCheck(self):
        for buttons in self.choices:
            for button in buttons:
                if button.isChecked():
                    button.setStyleSheet("background-color: red")
                if button.correct:
                    button.setStyleSheet("background-color: lightgreen")

        correct_count = 0
        for el in self.progress_data:
            if el["correct"]:
                correct_count += 1

        self.setWindowTitle(f"Result: {correct_count} / {len(self.progress_data)}")

    def onSave(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        fileName = QFileDialog.getSaveFileName(self, 'Save progress', timestr + ".json", '*.json')
        if fileName:
            with open(timestr, "w", encoding="utf-8") as f:
                json.dump(self.progress_data, f, ensure_ascii=False, indent=4)