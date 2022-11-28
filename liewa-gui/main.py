import sys
import subprocess
import platform
import yaml
from PyQt5 import QtGui, QtCore, QtWidgets
from designer_main import Ui_MainWindow
from planet_dialog import PlanetDialog
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QDialogButtonBox, QStyle
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QSize

from scheduler import Systemd, Launchd, Schtasks

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #########################Image Cmposition#########################
        self.parsed_config = {'settings': {'width': 1920, 'height': 1080, 'bg-color': '#000000'}, 'planets': {}}
        
        self.planet_list_model = QtGui.QStandardItemModel(self.planet_list_table)
        self.planet_list_table.setModel(self.planet_list_model)

        self.dialog_buttons.clicked.connect(self.handle_dialog_btn_click)
        self.save_yml_btn.clicked.connect(self.save_yml)
        self.choose_color_btn.clicked.connect(self.open_colorpicker)
        self.browse_bg_file_btn.clicked.connect(self.get_bg_img_file)
        self.browse_config_btn.clicked.connect(self.get_config_file)
        self.add_planet_btn.clicked.connect(self.add_planet)
        self.edit_planet_btn.clicked.connect(self.edit_planet)
        self.delete_planet_btn.clicked.connect(self.delete_planet)
        self.size_dropdown.currentIndexChanged.connect(self.canvas_size_change)
        self.x_value_input.textChanged.connect(self.canvas_size_change)
        self.y_value_input.textChanged.connect(self.canvas_size_change)
        self.custom_config_checkbox.toggled.connect(self.toggel_custom_config_mode)

        pixmapi = QStyle.SP_DialogSaveButton
        icon = self.style().standardIcon(pixmapi)
        self.save_yml_btn.setIcon(icon)
        
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
        self.selected_bg_color = QtGui.QColor(QtCore.Qt.black)

        self.preview_scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.preview_scene)

        self.size_error_label.setVisible(False)
        self.choosen_color_label.setStyleSheet(f"background-color: {self.selected_bg_color.name()};\n"f"color: {self.selected_bg_color.name()};")
    
        self.add_drop_down_options()
        self.size_dropdown.setCurrentIndex(6)

        self.update_planet_list()
        self.update_preview()
        #########################Scheduler###########################
        system = platform.system()
        if system == "Windows":
            self.scheduler = Schtasks()
        elif system == "Darwin":
            self.scheduler = Launchd()
        elif system == "Linux":
            self.scheduler = Systemd()
        else:
            print("Your OS-system is not supported!")
            sys.exit(1)

        self.status = False

        pixmapi = QStyle.SP_BrowserReload
        icon = self.style().standardIcon(pixmapi)
        self.reload_status_btn.setIcon(icon)

        self.reload_status_btn.clicked.connect(self.update_status)
        self.create_schedueler_btn.clicked.connect(self.create_new_scheduler)
        self.delete_scheduler_btn.clicked.connect(self.delete_scheduler)
        self.reload_scheduler_btn.clicked.connect(self.reload_scheduler)
        self.test_now_btn.clicked.connect(self.test_now)



        self.update_status()

        self.show()

    #########################Image Cmposition#########################
    def open_colorpicker(self):
            color = QColorDialog.getColor()
            if color.isValid():
                self.selected_bg_color = color
                self.choosen_color_label.setStyleSheet(f"background-color: {self.selected_bg_color.name()};\n"f"color: {self.selected_bg_color.name()};")
                self.update_preview()

    def handle_dialog_btn_click(self, button):
        role = self.dialog_buttons.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            with open('../liewa/recources/gui_config.yml', 'w') as file:
                yaml.dump(self.parsed_config, file)
            self.close()
            
        elif role == QDialogButtonBox.RejectRole:
            self.close()   

    def get_config_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file',"", "YAML files (*.yml)")[0]
            with open(fname, "r") as ymlfile:
                cfg = yaml.load(ymlfile,Loader=yaml.Loader)
            self.parsed_config = cfg
            self.planet_list_model.clear()
            self.update_planet_list()
            self.update_preview()
        except FileNotFoundError:
            pass

    def toggel_custom_config_mode(self,state):
        if not state:
            self.custom_size_checkbox.setChecked(False)
            self.background_img_checkbox.setChecked(False)
            self.x_value_input.setEnabled(False)
            self.x_label.setEnabled(False)
            self.y_value_input.setEnabled(False)
            self.y_label.setEnabled(False)
            self.browse_bg_file_btn.setEnabled(False)
        if state:
            self.planet_list_selection.clear()
            self.planet_list_model.clear()
            self.parsed_config["planets"] = {}
            self.update_planet_list()
            self.update_preview()
        
    def get_bg_img_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',"","Background files (*.png *.jpg)")
        print(fname)
        return fname

    def save_yml(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Open file',"my_config.yml", "YAML files (*.yml)")[0]
            with open(fname, 'w') as file:
                yaml.dump(self.parsed_config, file)
        except FileNotFoundError:
            pass
    
    def add_drop_down_options(self):
        for i,el in enumerate(self.drop_down_options):
            self.size_dropdown.addItem(el)
            self.size_dropdown.setItemText(i,el)

    def canvas_size_change(self):
        if self.x_value_input.isEnabled():
            self.selected_size = (int(self.x_value_input.text()),int(self.y_value_input.text()))
        else:
            self.selected_size = self.drop_down_options[self.size_dropdown.currentText()]
        try:
            self.size_error_label.setVisible(False)
            self.update_preview()
        except ZeroDivisionError:
            self.size_error_label.setVisible(True)
        
    def update_preview(self):
        self.preview_scene.clear()
        self.preview_scene.setBackgroundBrush(self.selected_bg_color)

        self.preview_scene.setSceneRect(0,0,int(200/self.selected_size[1]*self.selected_size[0]),200)
        preview_width = int(200/self.selected_size[1]*self.selected_size[0])
        preview_height = 200
        self.graphicsView.setFixedWidth(preview_width)
        self.graphicsView.setFixedHeight(preview_height)

        for index in range(self.planet_list_model.rowCount()):  #iterate through every planet in the list
            item = self.planet_list_model.item(index)
            if item.text() not in ["sentinel","apod"]:
                if item.text() in ["goes-16","goes-17","goes-18","himawari","meteosat-9","meteosat-11"]:
                    color = QtGui.QColor(QtCore.Qt.blue)
                elif item.text() == "sdo":
                    color = QtGui.QColor(QtCore.Qt.yellow)

                x = self.parsed_config["planets"][item.text()]["x"]
                y = self.parsed_config["planets"][item.text()]["y"]
                size = self.parsed_config["planets"][item.text()]["size"]
                
                scaled_x,scaled_y,scaled_width,scaled_height = self.scale_size_to_preview(x,y,size,size,preview_width,preview_height)

                self.preview_scene.addEllipse(scaled_x,scaled_y,scaled_width,scaled_height, brush=QBrush(color,Qt.SolidPattern))
            elif item.text() == "sentinel":
                color = QtGui.QColor('#707070')

                x = self.parsed_config["planets"][item.text()]["x"]
                y = self.parsed_config["planets"][item.text()]["y"]
                width = self.parsed_config["planets"][item.text()]["width"]
                height = self.parsed_config["planets"][item.text()]["height"]

                scaled_x,scaled_y,scaled_width,scaled_height = self.scale_size_to_preview(x,y,width,height,preview_width,preview_height)
                self.preview_scene.addRect(scaled_x,scaled_y,scaled_width,scaled_height, brush=QBrush(color,Qt.SolidPattern))
            elif item.text() == "apod":
                color = QtGui.QColor('#707070')

                x = self.parsed_config["planets"][item.text()]["x"]
                y = self.parsed_config["planets"][item.text()]["y"]
                size = self.parsed_config["planets"][item.text()]["size"]

                scaled_x,scaled_y,scaled_width,scaled_height = self.scale_size_to_preview(x,y,size,size,preview_width,preview_height)
                self.preview_scene.addRect(scaled_x,scaled_y,scaled_width,scaled_height, brush=QBrush(color,Qt.SolidPattern))

    def scale_size_to_preview(self,old_x,old_y,width,height,preview_width,preview_height):
        old_x = old_x-(width/2)
        old_y = old_y-(height/2)

        scale_factor = self.selected_size[1]/(preview_height)

        scaled_x = old_x/scale_factor
        scaled_y = old_y/scale_factor
        scaled_width = width/scale_factor
        scaled_height = height/scale_factor

        return scaled_x, scaled_y, scaled_width, scaled_height

    def update_planet_list(self):
        self.planet_list_model.clear()
        for planet in self.parsed_config['planets'].keys():
            item = QtGui.QStandardItem(planet)
            item.setEditable(False)
            self.planet_list_model.appendRow(item)

        self.planet_list_selection = self.planet_list_table.selectionModel()
        self.planet_list_selection.select(self.planet_list_model.index(0,0), QtCore.QItemSelectionModel.Select)
        
    def add_planet(self):
        planet_dialog = PlanetDialog("goes-16",{},self.parsed_config["settings"])
        if planet_dialog.settings:
            self.parsed_config["planets"][planet_dialog.planet] = planet_dialog.settings
            item = QtGui.QStandardItem(planet_dialog.planet)
            item.setEditable(False)
            self.planet_list_model.appendRow(item)
            self.update_planet_list()
            self.update_preview()

    def edit_planet(self):
        selected_item = self.planet_list_selection.selectedIndexes()
        if selected_item:
            selected_planet = self.planet_list_model.data(selected_item[0])
            planet_dialog = PlanetDialog(selected_planet,self.parsed_config["planets"][selected_planet],self.parsed_config["settings"])
            if planet_dialog.settings:
                self.parsed_config["planets"][planet_dialog.planet] = planet_dialog.settings
                self.update_planet_list()
                self.update_preview()

    def delete_planet(self):
        selected_index = self.planet_list_selection.selectedRows()
        if selected_index:
            item = self.planet_list_model.item(selected_index[0].row())
            self.parsed_config["planets"].pop(item.text(), None)
            self.planet_list_model.removeRow(selected_index[0].row())
            self.update_planet_list()
            self.update_preview()

    ##############################Scheduler###########################################

    def update_status(self):
        output, self.status = self.scheduler.update()

        if self.status:
            icon = self.style().standardIcon(QStyle.SP_DialogYesButton).pixmap(20,20)
            self.status_label_text.setText("Running")
        else:
            icon = self.style().standardIcon(QStyle.SP_DialogNoButton).pixmap(20,20)
            self.status_label_text.setText("Not running")
        self.status_label_color.setPixmap(icon)
        self.status_output.setPlainText(output)

    def create_new_scheduler(self):
        self.scheduler.create_scheduler()
        self.update_status()

    def delete_scheduler(self):
        self.scheduler.delete_scheduler()
        self.update_status()
    
    def reload_scheduler(self):
        self.scheduler.reload_scheduler()
        self.update_status()

    def test_now(self):
        liewa_path = subprocess.check_output(['which','liewa']).decode('utf-8').strip()
        subprocess.check_output(liewa_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec()
