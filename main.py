import json
import sys
import random
from time import sleep

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QComboBox, QVBoxLayout, QWidget, QPushButton, \
    QMessageBox, QFileDialog, QDialog
from PyQt5.QtCore import Qt

from quizview import QuizView

start_test_id = 1
end_test_id = 11

def get_test_path(test_id):
    return f'tests\\{test_id}\\'

def get_test_data(test_id):
    with open(get_test_path(test_id) + "questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Drive test")
        self.is_all = False

        widget = QWidget()

        combobox = QComboBox(self)
        for i in range(start_test_id, end_test_id + 1):
            combobox.addItem(str(i))

        button = QPushButton("Select")
        button.clicked.connect(lambda: self.onSelect(combobox))

        all_button = QPushButton("Select All")
        all_button.clicked.connect(self.onAll)

        lay = QVBoxLayout()
        lay.addWidget(combobox)
        lay.addWidget(button)
        lay.addWidget(all_button)
        lay.setAlignment(Qt.AlignCenter)
        widget.setLayout(lay)

        self.setCentralWidget(widget)

    def onAll(self):
        self.is_all = True

    def onSelect(self, combobox : QComboBox):
        print(combobox.currentText())

        buttonReply = QMessageBox.question(self, 'PyQt5 message', "Wanna open progress ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        dialog = QuizView(self)
        dialog.test_id = combobox.currentText()
        dialog.test_data = get_test_data(dialog.test_id)

        with open("tests/questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)

        if not self.is_all:
            current_id = int(combobox.currentText())
            dialog.questions = []
            for el in questions:
                if el["test_id"] == current_id:
                    dialog.questions.append(el)
        else:
            dialog.questions = questions

        random.shuffle(dialog.questions)

        if buttonReply == QMessageBox.Yes:
            self.filename = QFileDialog.getOpenFileName(self, 'Open File', ".", "JSON files(*.json)")[0]

            if self.filename:
                with open(self.filename, "r", encoding="utf-8") as f:
                    dialog.progress_data = json.load(f)

                progress_data = []
                for el in dialog.progress_data:
                    if not el["correct"]:
                        progress_data.append(el)

                dialog.progress_data = progress_data

                new_questions = []
                for ids in dialog.progress_data:
                    for el in questions:
                        if el["id"] == ids["id"]:
                            new_questions.append(el)
                dialog.questions = new_questions
        else:
            dialog.progress_data = []

            for el in dialog.questions:
                dialog.progress_data.append({
                    "id" : el["id"],
                    "selected_id" : None,
                    "selected" : None,
                    "correct" : False
                })
        dialog.initUI()
        dialog.show()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
