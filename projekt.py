#!/usr/bin/env python3

import sys
import yaml
from PyQt4 import QtGui, QtCore
from PyQt4 import Qt

def import_tagsets(filename):
    with open(filename, 'r') as stream:
        try:
            tagsets = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return tagsets

class Window(QtGui.QMainWindow):
    def __init__(self, tagset):
        super(Window, self).__init__()
        # groupslist = buttonBereich
        self.tagset = tagset
        self.buttonBereich = QtGui.QListWidget()
        self.text1 = QtGui.QTextEdit(self)
        self.text2 = QtGui.QTextEdit(self)
        # unterteilt in obere und untere Editor
        # splitter = mainSplitter
        # editorSplitter = messageSplitter
        self.editorSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.editorSplitter.addWidget(self.text1)
        self.editorSplitter.addWidget(self.text2)
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.buttonBereich)
        self.splitter.addWidget(self.editorSplitter)
        self.setCentralWidget(self.splitter)

        # hoehe und breite fuer die splits
        self.splitter.setStretchFactor(1, 3)
        self.editorSplitter.setStretchFactor(2, 4)

        self.home(self.tagset)

    def make_calluser(self, name):
        # http://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
        def calluser():
            print(name)
            self.text1.insertPlainText(name + " ")
        return calluser

    def home(self, tagset):
        grid = QtGui.QGridLayout()
        self.buttonBereich.setLayout(grid)

        positions = [(i, j) for i in range(18) for j in range(3)]

        for position, name in zip(positions, tagset):
            if name == '':
                continue
            button = QtGui.QPushButton(name, self)
            button.clicked.connect(self.make_calluser(name))
            grid.addWidget(button, *position)


def run():
    mytags = import_tagsets('tagset.yaml')
    app = QtGui.QApplication(sys.argv)
    main = Window(mytags['STTS'])
    main.showMaximized()
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    run()
