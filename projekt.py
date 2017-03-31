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
        self.setWindowTitle("POS-Tagger")
        self.tagset = tagset
        # groupslist = buttonBereich
        self.buttonBereich = QtGui.QListWidget()
        self.text = QtGui.QTextEdit(self)

        # Buttons zwischen den Editoren
        self.widg = QtGui.QWidget()
        self.hbox = QtGui.QHBoxLayout()
        self.startButton = QtGui.QPushButton("START")
        self.skipButton = QtGui.QPushButton("SKIP")
        self.nextButton = QtGui.QPushButton("NEXT")
        self.hbox.addWidget(self.startButton)
        self.hbox.addWidget(self.skipButton)
        self.hbox.addWidget(self.nextButton)
        self.widg.setLayout(self.hbox)

        # wenn der START-Button gedrückt wird soll passieren:
        self.startButton.clicked.connect(self.starting)
        self.nextButton.clicked.connect(self.nextButton_clicked)
        self.skipButton.clicked.connect(self.skipping)
        # unterteilt in obere und untere Editor
        self.editorSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.editorSplitter.addWidget(self.widg)
        self.editorSplitter.addWidget(self.text)
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.buttonBereich)
        self.splitter.addWidget(self.editorSplitter)
        self.setCentralWidget(self.splitter)

        # hoehe und breite fuer die splits
        self.splitter.setStretchFactor(1, 3)
        self.editorSplitter.setStretchFactor(1, 4)



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

        # speichert das Ergebnis als PDF
        pdfAction = QtGui.QAction("Save to PDF", self)
        pdfAction.setShortcut("Ctrl+P")
        pdfAction.triggered.connect(self.SavetoPDF)
        #################EDIT EDITOR ######################

        # Edit: Cut
        cutAction = QtGui.QAction("Cut to clipboard", self)
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.text.cut)

        # Edit: Copy
        copyAction = QtGui.QAction("Copy to clipboard", self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.text.copy)

        # Edit: Paste
        pasteAction = QtGui.QAction("Paste from clipboard", self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.text.paste)

        # Edit: Undo
        undoAction = QtGui.QAction("Undo last action", self)
        undoAction.setShortcut("Ctrl+Z")
        undoAction.triggered.connect(self.text.undo)

        # Edit: Redo
        redoAction = QtGui.QAction("Redo last action", self)
        redoAction.setShortcut("Ctrl+Y")
        redoAction.triggered.connect(self.text.redo)
        #################END EDIT EDITOR #########
        
        # create menubar
        menuBar = self.menuBar()
        # unterpunkte File, Edit und View , Help werden erstellt
        file = menuBar.addMenu('&File')        
        edit = menuBar.addMenu('&Edit')
        pdf = menuBar.addMenu('&PDF')
        help = menuBar.addMenu('&Help')

        # menuunterpunkt File
        file.addAction(newAction)
        file.addAction(openFile)
        file.addAction(save)
        file.addSeparator()
        file.addAction(quitApp)

        # menuunterpunkt Edit
        edit.addAction(cutAction)
        edit.addAction(copyAction)
        edit.addAction(pasteAction)
        edit.addSeparator()
        edit.addAction(undoAction)
        edit.addAction(redoAction)

        # menuunterpunkt PDF
        pdf.addAction(pdfAction)
        # menuunterpunkt Help
        help.addAction(helpSTTS)
        
        # create statusbar
        self.statusBar().showMessage("Mustafa Öztürk      |      FAU Erlangen-Nürnberg      |      mustafa.oeztuerk@fau.de")

        # Schriftgröße
        font = QtGui.QFont()
        font.setPointSize(20)
        self.text.setFont(font)
        self.home(self.tagset)
        
    def make_calluser(self, name):
        # http://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt
        def calluser():
            self.text.insertPlainText("\\\\" + name)
        return calluser

    def home(self, tagset):
        # hier werden die Buttons für die Tags erstellt
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
            self.text.clear()
        else:
            pass
        
    def file_open(self):
        """ oeffnet eine Datei im Editor """
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
            textFile = file.read()
            self.text.setText(textFile)


    def speichern(self):
        """ speichert den Text im unteren Editor"""
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        textF = self.text.toPlainText()
        file.write(textF)
        file.close()

    def close_application(self):
        """ schließt die Anwendung"""
        choice = QtGui.QMessageBox.question(self, "Question", "Quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass


    def SavetoPDF(self):
        """ Speichert das Ergebnis als PDF Datei"""
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save to PDF')
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        if filename:
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            printer.setPageSize(QtGui.QPrinter.A4)
            printer.setColorMode(QtGui.QPrinter.Color)
            printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            self.text.document().print_(printer)

    def stts_link(self):
        url = QtCore.QUrl('http://www.ims.uni-stuttgart.de/forschung/ressourcen/lexika/TagSets/stts-table.html')
        if not QtGui.QDesktopServices.openUrl(url):
            QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')


    def starting(self):
        """Mit dem START-Button wird der Cursor an den Anfang gesetzt, Cursor dient als Marker, um die Wörter einzeln zu Taggen. Und Editor wird gecleart"""
        cursor = self.text.textCursor()
        cursor.movePosition(0, QtGui.QTextCursor.MoveAnchor)
        self.text.setTextCursor(cursor)
        QtCore.QCoreApplication.sendEvent(self.text, QtGui.QKeyEvent(QtCore.QEvent.KeyPress, QtCore.Qt.Key_Up, QtCore.Qt.NoModifier))
        self.text.moveCursor(QtGui.QTextCursor.EndOfWord, QtGui.QTextCursor.MoveAnchor)
        
    
    def nextButton_clicked(self):
        """ Der Cursor wird zum nächsten Wort bewegt, damit der Benutzer sehen kann, welches Wort grad getaggt wird"""
        self.text.moveCursor(QtGui.QTextCursor.NextWord, QtGui.QTextCursor.MoveAnchor)
        self.text.moveCursor(QtGui.QTextCursor.EndOfWord, QtGui.QTextCursor.MoveAnchor)

    def skipping(self):
        """ unbekannte Wörter werden übersprungen"""
        self.text.insertPlainText("!!SKIPPED!!")

def run():
    mytags = import_tagsets('tagset.yaml')
    app = QtGui.QApplication(sys.argv)
    main = Window(mytags['STTS'])
    main.showMaximized()
    sys.exit(app.exec_())

    
if __name__ == '__main__':
    run()
