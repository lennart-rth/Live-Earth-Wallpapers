from PyQt5.QtWidgets import QDialog, QSpinBox, QComboBox, QLabel, QDoubleSpinBox
from liewa.liewa_gui.designer_planet import Ui_Dialog
from PyQt5.QtWidgets import QDialogButtonBox


class PlanetDialog(QDialog, Ui_Dialog):
    def __init__(self,planet,planet_config, view_config):
        super(PlanetDialog, self).__init__()
        self.setupUi(self)
        
        self.planet = planet
        self.settings = planet_config

        if planet != "sentinel":
            self.size_input.setValue(int(view_config["width"]/3))       #set size to 1/3 of image width

        self.filter = {"geostationary":["x","y","size","color"],"sdo":["x","y","size","bandwidth"],"apod":["x","y","size","fit"],"sentinel":["x","y","width","height","scale","latitude","longitude"]}

        self.dialog_buttons.clicked.connect(self.handle_dialog_btn_click)
        self.satellite_selector.currentTextChanged.connect(self.filter_dialog)

        self.satellite_selector.setCurrentText(self.planet)

        self.filter_dialog()
        self.parse_values_in_dialog()

        self.exec_()

    def handle_dialog_btn_click(self, button):
        role = self.dialog_buttons.buttonRole(button)
        if role == QDialogButtonBox.ApplyRole:
            self.get_values()
            self.parse_values_in_dialog()
            self.close()
            
        elif role == QDialogButtonBox.RejectRole:
            self.settings = None
            self.close()

    def get_values(self):
        planet_group = "geostationary" if self.satellite_selector.currentText() in ["goes-16","goes-18","himawari","gk2a","meteosat-9","meteosat-0deg"] else self.satellite_selector.currentText()
        all_values = {}
        for widget in self.children():
            if isinstance(widget, QSpinBox) or isinstance(widget,QDoubleSpinBox):
                all_values[widget.objectName().split("_")[0]] = widget.value()
            elif isinstance(widget, QComboBox):
                if widget.objectName() != "satellite_selector":
                    all_values[widget.objectName().split("_")[0]] = widget.currentText()
       
        self.settings = {par:all_values[par] for par in self.filter[planet_group]}

    def filter_dialog(self):
        planet_group = "geostationary" if self.satellite_selector.currentText() in ["goes-16","goes-18","himawari","gk2a","meteosat-9","meteosat-0deg"] else self.satellite_selector.currentText()
        parameter_list = []
        for par in self.filter[planet_group]:
            parameter_list.append(par+"_label")
            parameter_list.append(par+"_input")

        for widget in self.children():
            if isinstance(widget, QSpinBox) or isinstance(widget,QComboBox) or isinstance(widget,QLabel) or isinstance(widget, QDoubleSpinBox):
                if widget.objectName() in parameter_list:
                    widget.setVisible(True)
                else:
                    widget.setVisible(False)
        
        self.satellite_label.setVisible(True)
        self.satellite_selector.setVisible(True)                

        self.adjustSize()

    def parse_values_in_dialog(self):
        self.planet = self.satellite_selector.currentText()

        planet_group = "geostationary" if self.satellite_selector.currentText() in ["goes-16","goes-18","himawari","gk2a","meteosat-9","meteosat-0deg"] else self.satellite_selector.currentText()
        
        for widget in self.children():
            if isinstance(widget, QSpinBox):
                name = widget.objectName().split("_")[0]
                if name in self.settings:
                    value = self.settings[name]
                    widget.setValue(value)
            elif isinstance(widget, QComboBox):
                if widget.objectName() != "satellite_selector":
                    name = widget.objectName().split("_")[0]
                    if name in self.settings:
                        value = self.settings[name]
                        widget.setCurrentText(value)

        

    

        
