#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León

# Ventana de monitor serial 

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit
from PySide6.QtGui import QResizeEvent
from modules.config_widgets import CustomFrame,CustomLabel
# from main import MainWindow

class VentanaMonitorSerial(QWidget): 
    def __init__(self, MainWindow): 
        super().__init__() 

        self.mainwindow = MainWindow

        self.setFixedSize(1000,750)
        self.setWindowTitle("Monitor Serial") 

        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424") 

        self.texto_monitor_serial = QTextEdit(self)
        self.limpiar_ser_mon = QPushButton(self)
        self.limpiar_ser_mon.setText("Limpiar")
        self.datos_a_serial = QLineEdit(self)
        self.datos_a_serial.setPlaceholderText("Mensaje (Enter para enviar el mensaje)")
        self.datos_a_serial.setEnabled(False)
        self.texto_monitor_serial.setReadOnly(True)
        self.texto_monitor_serial.setText("Puerto serial desconectado.")
        self.texto_monitor_serial.setStyleSheet("background: #050505;"
                                          "border: 1px solid #5A5C5F;"
                                          "border-radius: 5px;"
                                          )
        self.limpiar_ser_mon.setStyleSheet("background: #111111;"
                                          "border: 1px solid #5A5C5F;"
                                          "border-radius: 5px;"
                                           )
        self.datos_a_serial.setStyleSheet("background: #1D1D1D;"
                                        "border: 1px solid #5A5C5F;"
                                        "border-radius: 5px;"
                                        ) 

        self.limpiar_ser_mon.clicked.connect(self.LimpiarSerial)
        self.datos_a_serial.returnPressed.connect(self.EnviarSerial)

    def EnviarSerial(self):
        texto = self.datos_a_serial.text().encode("utf-8")
        self.datos_a_serial.setText("")
        self.mainwindow.ser.write(texto) 

    def LimpiarSerial(self): 
        self.texto_monitor_serial.setText("") 
        pass


    def resizeEvent(self, event: QResizeEvent) -> None:
        self.texto_monitor_serial.setGeometry(int(self.geometry().width()*0.01), int(self.geometry().height()*0.05), int(self.geometry().width()*0.98), int(self.geometry().height()*0.85))
        self.limpiar_ser_mon.setGeometry(int(self.geometry().width()*0.92), int(self.geometry().height()*0.92), int(self.geometry().width()*0.07), int(self.geometry().height()*0.06))
        self.datos_a_serial.setGeometry(int(self.geometry().width()*0.01), int(self.geometry().height()*0.92), int(self.geometry().width()*0.90), int(self.geometry().height()*0.06))

