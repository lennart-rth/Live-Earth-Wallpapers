import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from designer import Ui_MainWindow
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QDialogButtonBox, QGraphicsRectItem

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.dialog_buttons.clicked.connect(self.handle_dialog_btn_click)

        self.choose_color_btn.clicked.connect(self.open_colorpicker)
        self.browse_bg_file_btn.clicked.connect(self.get_bg_img_file)
        self.browse_config_btn.clicked.connect(self.get_config_file)

        self.size_dropdown.currentIndexChanged.connect(self.size_change)
        self.x_value_input.textChanged.connect(self.size_change)
        self.y_value_input.textChanged.connect(self.size_change)


        scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(scene)
        scene.setSceneRect(0,0,0,0)
        pen = QtGui.QPen(QtCore.Qt.black)

        

        
        self.drop_down_options = {
            "320x320": (320,320),
            "640x480": (640,480),
            "800x600": (800,600),
            "900x600": (900,600),
            "1024x768": (1024,768),
            "1440x900": (1440,900),
            "1920x1080": (1920,1080),
            "3840x2160": (3840,2160),
            "7680x4320": (7680,4320),}

        self.selected_size = (1920, 1080)
        self.selected_bg_color = "#000000"



        self.add_drop_down_options()
        self.size_dropdown.setCurrentIndex(6)
        self.show()

    def open_colorpicker(self):
            color = QColorDialog.getColor()
            if color.isValid():
                self.selected_bg_color = color.name()
                self.choosen_color_label.setStyleSheet(f"background-color: {self.selected_bg_color};\n"f"color: {self.selected_bg_color};")


    def handle_dialog_btn_click(self, button):
        role = self.dialog_buttons.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            self.close()
            
        elif role == QDialogButtonBox.RejectRole:
            self.close()   

    def get_config_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',"YAML files (*.yml)", "YAML files (*.yml)")
        print(fname)
        return fname

    def get_bg_img_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',"Background files (*.png *.jpg)","Background files (*.png *.jpg)")
        print(fname)
        return fname
    
    def add_drop_down_options(self):
        for i,el in enumerate(self.drop_down_options):
            self.size_dropdown.addItem(el)
            self.size_dropdown.setItemText(i,el)

    def size_change(self):
        if self.x_value_input.isEnabled():
            self.selected_size = (int(self.x_value_input.text()),int(self.y_value_input.text()))
        else:
            self.selected_size = self.drop_down_options[self.size_dropdown.currentText()]


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec()
