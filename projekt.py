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
        self.setWindowTitle("POS")
        self.tagset = tagset
        # groupslist = buttonBereich
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



        # STTS-tagset wird im browser geoffnet
        helpSTTS = QtGui.QAction("STTS Tag Table", self)
        helpSTTS.triggered.connect(self.stts_link)
        # newAction zum saeubern der Editor
        newAction = QtGui.QAction("New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.new)
        # schließt die Anwendung
        quitApp = QtGui.QAction("Quit", self)
        quitApp.setShortcut("Ctrl+Q")
        quitApp.triggered.connect(self.close_application)

        # oeffnet eine datei
        openFile = QtGui.QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.triggered.connect(self.file_open)
        # speichert das was im unteren Editor ist
        save = QtGui.QAction("Save", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.speichern)


        #############EDIT EDITOR 1##############
        #Edit: Cut
        cutAction1 = QtGui.QAction("Cut to clipboard", self)
        cutAction1.setShortcut("Ctrl+X")
        cutAction1.triggered.connect(self.text1.cut)

        #Edit: Copy
        copyAction1 = QtGui.QAction("Copy to clipboard", self)
        copyAction1.setShortcut("Ctrl+C")
        copyAction1.triggered.connect(self.text1.copy)

        # Edit: Paste
        pasteAction1 = QtGui.QAction("Paste from clipboard", self)
        pasteAction1.setShortcut("Ctrl+V")
        pasteAction1.triggered.connect(self.text1.paste)

        # Edit: Undo
        undoAction1 = QtGui.QAction("Undo last action", self)
        undoAction1.setShortcut("Ctrl+Z")
        undoAction1.triggered.connect(self.text1.undo)

        # Edit: Redo
        redoAction1 = QtGui.QAction("Redo last action", self)
        redoAction1.setShortcut("Ctrl+Y")
        redoAction1.triggered.connect(self.text1.redo)
        
        #################EDIT EDITOR 2######################

        #Edit: Cut
        cutAction2 = QtGui.QAction("Cut to clipboard", self)
        cutAction2.setShortcut("Ctrl+X")
        cutAction2.triggered.connect(self.text2.cut)

        #Edit: Copy
        copyAction2 = QtGui.QAction("Copy to clipboard", self)
        copyAction2.setShortcut("Ctrl+C")
        copyAction2.triggered.connect(self.text2.copy)

        #Edit: Paste
        pasteAction2 = QtGui.QAction("Paste from clipboard", self)
        pasteAction2.setShortcut("Ctrl+V")
        pasteAction2.triggered.connect(self.text2.paste)

        #Edit: Undo
        undoAction2 = QtGui.QAction("Undo last action", self)
        undoAction2.setShortcut("Ctrl+Z")
        undoAction2.triggered.connect(self.text2.undo)

        #Edit: Redo
        redoAction2 = QtGui.QAction("Redo last action", self)
        redoAction2.setShortcut("Ctrl+Y")
        redoAction2.triggered.connect(self.text2.redo)
        #################END EDIT EDITOR 2#########
        
        # create menubar
        menuBar = self.menuBar()
        # unterpunkte File, Edit und View , Help werden erstellt
        file = menuBar.addMenu('&File')        
        edit1 = menuBar.addMenu('&Edit Editor 1')
        edit2 = menuBar.addMenu('&Edit Editor 2')
        view = menuBar.addMenu('&View')
        help = menuBar.addMenu('&Help')

        # menuunterpunkt File
        file.addAction(newAction)
        file.addAction(openFile)
        file.addAction(save)
        file.addSeparator()
        file.addAction(quitApp)

        # menuunterpunkt Edit Editor 1
        edit1.addAction(cutAction1)
        edit1.addAction(copyAction1)
        edit1.addAction(pasteAction1)
        edit1.addSeparator()
        edit1.addAction(undoAction1)
        edit1.addAction(redoAction1)

        # menuunterpunkt Edit Editor 2
        edit2.addAction(cutAction2)
        edit2.addAction(copyAction2)
        edit2.addAction(pasteAction2)
        edit2.addSeparator()
        edit2.addAction(undoAction2)
        edit2.addAction(redoAction2)
        
        # menuunterpunkt Help
        help.addAction(helpSTTS)
        
        # create statusbar
        self.statusBar().showMessage("Mustafa Öztürk    |    FAU Erlangen-Nürnberg    |    mustafa.oeztuerk@fau.de")


        # Schriftgröße
        font = QtGui.QFont()
        font.setPointSize(20)
        self.text1.setFont(font)
        self.text2.setFont(font)
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


    def new(self):
        choice = QtGui.QMessageBox.question(self, "Question", "Clear Editors?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            self.text1.clear()
            self.text2.clear()
        else:
            pass
        
    def file_open(self):
        """ oeffnet eine Datei im oberen Editor """
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        """file = open(name, 'r')
        with file:
            text = file.read()
            self.text1.setText(text)
            print(text)
            #test
            words = [word for line in text for word in line.split()]
            print(words)"""
        with open(name, 'r') as file:
            text = file.read()
            self.text1.setText(text)
            # print aktuell geöffneten text
            print(text)
            #words = [word
                     #for line in text
                     #for word in line.split()]
            words = text.split()
        self.read_from_Editor(words)




    def speichern(self):
        """ speichert den Text im unteren Editor"""
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        text = self.text2.toPlainText()
        file.write(text)
        file.close()

    def close_application(self):
        """ schließt die Anwendung"""
        choice = QtGui.QMessageBox.question(self, "Question", "Quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def stts_link(self):
        url = QtCore.QUrl('http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')



    def read_from_Editor(self, words):
        """ reading text from a QTextEdit widget"""
        #doc = self.text1.document()
        #block = doc.begin()
        #lines = [block.text()]
        #for i in range (1, doc.blockCount() ):
            #block = block.next()
            #lines.append(block.text())
        #print(lines)
        self.words = words
        listoflists = []
        for i in range(0, len(words)):
            listoflists.append((words[i], None))
        print(listoflists)

def run():
    mytags = import_tagsets('tagset.yaml')
    app = QtGui.QApplication(sys.argv)
    main = Window(mytags['STTS'])
    main.showMaximized()
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    run()
