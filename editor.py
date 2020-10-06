import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QPlainTextEdit, QFrame, QLabel, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

import io

from omniaUI import OmniaUI

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'OmniaUI Editor'
        self.left = 10
        self.top = 10
        self.width = 1200
        self.height = 800
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(20, 40)
        self.textbox.resize(800,700)
        
        # Create a button in the window
        self.draw_btn = QPushButton('Draw', self)
        self.draw_btn.move(840,360)
        self.rotate_btn = QPushButton('Rotate', self)
        self.rotate_btn.move(950,360)
        self.save_btn = QPushButton('Save', self)
        self.save_btn.move(950,400)
        self.open_btn = QPushButton('Open', self)
        self.open_btn.move(840,400)

        # Create filename label
        self.file_label = QLabel(self)
        self.file_label.setText("")
        self.file_label.move(20,10)
        self.file_label.resize(800, 30)

        # Create image
        self.ui_width = 320
        self.ui_height = 240

        self.img_label = QLabel(self)
        self.img_label.text = "hello"
        self.img_label.resize(320,240)
        self.img_label.move(840,20)
        self.img_label.setFrameShape(QFrame.Panel)        

        self.omniaui = OmniaUI((self.ui_width, self.ui_height))

        self.image = QPixmap()

        self.draw()

        self.img_label.setPixmap(self.image)

        # connect button to function on_click
        self.draw_btn.clicked.connect(self.draw_ui)
        self.rotate_btn.clicked.connect(self.rotate_ui)
        self.save_btn.clicked.connect(self.save_ui)
        self.open_btn.clicked.connect(self.open_ui)
        self.show()
    
    def draw(self, xml_string=''):
        if xml_string != '':
            self.omniaui.loadFromXML(xml_string)
        
        img = self.omniaui.get_image()
        w,h = img.size
        #print(w,h)
        self.img_label.resize(w,h)
        
        f = io.BytesIO()
        img.save(f, "png")
        buf = f.getbuffer()
        self.image.loadFromData(buf)
        del buf
        f.close()

        self.img_label.setPixmap(self.image)

    @pyqtSlot()
    def rotate_ui(self):
        self.omniaui.changeOrientation()

        orientation = self.omniaui.getOrientation()

        self.draw()

        text = self.textbox.toPlainText()

        or_index = text.find("orientation=")

        if or_index == -1:
            #print(text.find("ui"))
            start = text.find("<ui") + 3
            end = text.find(">", start)
            ui_attrib = text[ start : end ].strip()
            ui_attrib += " orientation='"+orientation+"'"

            text = text[:start] +" "+ ui_attrib + text[end:]
            
        else:
            start = or_index + 13   # skip "orientation='"
            end = text.find("'",start)
            text = text[:start] + orientation + text[end:]
        
        self.textbox.setPlainText(text)     

    @pyqtSlot()
    def draw_ui(self):
        textboxValue = self.textbox.toPlainText()
        self.draw(textboxValue)
    
    @pyqtSlot()
    def save_ui(self):
        text = self.textbox.toPlainText()
        name = QFileDialog.getSaveFileName(self, "Save File", '.', '.xml')[0]
        if name != '':
            self.file_label.setText(name + ".xml")
        

        with open(name + ".xml", "w") as f:
            #_ = f.read()
            f.seek(0,0)
            f.write(text)
    
    @pyqtSlot()
    def open_ui(self):
        fileFullName, _ = QFileDialog.getOpenFileName(self,"Open UI file", ".","XML files (*.xml)")
        
        self.file_label.setText(fileFullName)
        with open(fileFullName, "r") as f:
            content = f.read()
            self.textbox.setPlainText(content)
            self.draw(content)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())