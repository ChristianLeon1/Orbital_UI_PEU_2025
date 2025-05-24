#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León

# Ventana de monitor serial 

from PySide6.QtCore import QSize, Qt, QUrl
import json
from PySide6.QtWidgets import QComboBox, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit
from PySide6.QtGui import QResizeEvent
from modules.config_widgets import CustomFrame,CustomLabel

class ConfigEjes:
    def __init__(self, filename='config.json'):
        self.filename = filename
        self.default_config = {
            'eje_x': {
                'Eje': 'Ángulo X',
                'Invertir': 1,
                'Calibración': 0
            },
            'eje y': {
                'Eje': 'Ángulo Y', 
                'Invertir': 1,
                'Calibración': 0
            },
            'eje z': {
                'Eje': 'Ángulo Z',
                'Invertir': 1, 
                'Calibración': 0
            }
        }

    def guardar_configuracion(self, config_data):
        with open(self.filename, 'w') as f:
            json.dump(config_data, f, indent=4)

    def cargar_configuracion(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Archivo de configuración no encontrado. Creando uno nuevo con valores por defecto.")
            self.guardar_configuracion(self.default_config)
            return self.default_config
        except json.JSONDecodeError:
            print("Error en el formato del archivo de configuración. Cargando valores por defecto.")
            return self.default_config

class VentanaConfig3D(QWidget):
    def __init__(self, MainWindow):  
        super().__init__()  

        self.main_window = MainWindow

        self.setFixedSize(600,400)
        self.setWindowTitle("Configuración modelo 3D") 

        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424")  

        self.boton_calibrar = QPushButton(self)  
        self.boton_calibrar.setStyleSheet("background-color: #242424")
        self.boton_calibrar.setText("Calibrar modelo 3D")
        self.boton_invertir_x = QPushButton(self) 
        self.boton_calibrar.setStyleSheet("background-color: #242424")
        self.invertir_label = CustomLabel("Invertir Ejes", self, background="black")
        self.boton_invertir_x.setText("Invertir Eje X")
        self.boton_invertir_x.setStyleSheet("background-color: #242424")
        self.boton_invertir_y = QPushButton(self) 
        self.boton_invertir_y.setText("Invertir Eje Y")
        self.boton_invertir_y.setStyleSheet("background-color: #242424")
        self.boton_invertir_z = QPushButton(self) 
        self.boton_invertir_z.setText("Invertir Eje Z")
        self.boton_invertir_z.setStyleSheet("background-color: #242424") 

        self.intercambiar_ejes = CustomLabel("Intercambio de ejes ", parent=self, background="black",) 
        self.eje_x = CustomLabel("Eje X:", parent=self, background="black", align=Qt.AlignLeft)
        self.eje_y = CustomLabel("Eje Y:", parent=self, background="black", align=Qt.AlignLeft)
        self.eje_z = CustomLabel("Eje Z:", parent=self, background="black", align=Qt.AlignLeft) 
        self.selector_eje_x = QComboBox(self) 
        self.selector_eje_x.addItems(['Eje X', 'Eje Y', 'Eje Z'])
        self.selector_eje_x.setCurrentIndex(0)
        self.selector_eje_y = QComboBox(self) 
        self.selector_eje_y.addItems(['Eje X', 'Eje Y', 'Eje Z'])
        self.selector_eje_y.setCurrentIndex(1)
        self.selector_eje_z = QComboBox(self)  
        self.selector_eje_z.addItems(['Eje X', 'Eje Y', 'Eje Z'])
        self.selector_eje_z.setCurrentIndex(2)

        self.boton_aplicar_cambios = QPushButton(self) 
        self.boton_aplicar_cambios.setText("Aplicar Cambios")
        self.boton_aplicar_cambios.setStyleSheet("background-color: #242424") 

        # Acciones

        self.boton_aplicar_cambios.clicked.connect(self.ActualizarDatos)
        self.boton_calibrar.clicked.connect(self.Calibar) 
        self.boton_invertir_x.clicked.connect(self.InvertirEjeX)
        self.boton_invertir_y.clicked.connect(self.InvertirEjeY)
        self.boton_invertir_z.clicked.connect(self.InvertirEjeZ)

    def InvertirEjeX(self): 
        if self.main_window.eje_x['Invertir'] == 1: 
            self.main_window.eje_x['Invertir'] = -1
        else:
            self.main_window.eje_x['Invertir'] = 1 
        
    def InvertirEjeY(self): 
        if self.main_window.eje_x['Invertir'] == 1: 
            self.main_window.eje_x['Invertir'] = -1
        else:
            self.main_window.eje_x['Invertir'] = 1 

    def InvertirEjeZ(self): 
        if self.main_window.eje_x['Invertir'] == 1: 
            self.main_window.eje_x['Invertir'] = -1
        else:
            self.main_window.eje_x['Invertir'] = 1 

    def Calibar(self): 
        self.main_window.eje_x['Calibración'] = self.main_window.eje_x['Invertir'] * self.main_window.cp[self.main_window.eje_x['Eje']][self.main_window.cp_index]
        self.main_window.eje_y['Calibración'] = self.main_window.eje_y['Invertir'] * self.main_window.cp[self.main_window.eje_y['Eje']][self.main_window.cp_index]
        self.main_window.eje_z['Calibración'] = self.main_window.eje_z['Invertir'] * self.main_window.cp[self.main_window.eje_z['Eje']][self.main_window.cp_index]
    
    def ActualizarDatos(self): 

        if self.selector_eje_x.currentIndex == 0: 
            self.main_window.eje_x['Eje'] = 'Ángulo X'
        elif self.selector_eje_x.currentIndex == 1: 
            self.main_window.eje_x['Eje'] = 'Ángulo Y'
        elif self.selector_eje_x.currentIndex == 2: 
            self.main_window.eje_x['Eje'] = 'Ángulo Z'

        if self.selector_eje_y.currentIndex == 0: 
            self.main_window.eje_y['Eje'] = 'Ángulo X'
        elif self.selector_eje_y.currentIndex == 1: 
            self.main_window.eje_y['Eje'] = 'Ángulo Y'
        elif self.selector_eje_y.currentIndex == 2: 
            self.main_window.eje_y['Eje'] = 'Ángulo Z'

        if self.selector_eje_z.currentIndex == 0: 
            self.main_window.eje_z['Eje'] = 'Ángulo X'
        elif self.selector_eje_z.currentIndex == 1: 
            self.main_window.eje_z['Eje'] = 'Ángulo Y'
        elif self.selector_eje_z.currentIndex == 2: 
            self.main_window.eje_z['Eje'] = 'Ángulo Z'


    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.geometry().width()
        height = self.geometry().height() 

        self.invertir_label.setGeometry(int(width*0.1), int(height*0.1), int(width*0.8), 30) 
        self.boton_invertir_x.setGeometry(int(width*0.1), int(height*0.2), int(width*0.233), 30) 
        self.boton_invertir_y.setGeometry(int(width*0.383), int(height*0.2), int(width*0.233), 30) 
        self.boton_invertir_z.setGeometry(int(width*0.666), int(height*0.2), int(width*0.233), 30) 
        
        self.intercambiar_ejes.setGeometry(int(width*0.1), int(height*0.4), int(width*0.8), 30) 
        self.eje_x.setGeometry(int(width*0.1), int(height*0.5), int(width*0.35), 30)
        self.eje_y.setGeometry(int(width*0.1), int(height*0.6), int(width*0.35), 30)
        self.eje_z.setGeometry(int(width*0.1), int(height*0.7), int(width*0.35), 30)
        self.selector_eje_x.setGeometry(int(width*0.5), int(height*0.5), int(width*0.4), 30)
        self.selector_eje_y.setGeometry(int(width*0.5), int(height*0.6), int(width*0.4), 30)
        self.selector_eje_z.setGeometry(int(width*0.5), int(height*0.7), int(width*0.4), 30)
        self.boton_aplicar_cambios.setGeometry(int(width*0.1), int(height*0.8), int(width*0.35), 30)
        self.boton_calibrar.setGeometry(int(width*0.55), int(height*0.8), int(width*0.35), 30)

       
