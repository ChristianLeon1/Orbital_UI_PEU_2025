#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 Autor: Christian Yael Ramírez León
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QFrame, QLabel, QProgressBar
import pyqtgraph as pg 

class CustomLabel(QLabel):
    def __init__(self, text="", parent=None, fsize=16, background="#2A2A2A", align=Qt.AlignCenter):
        super().__init__(text, parent)

        # Establecer las características iniciales
        self.setStyleSheet(
            f"background: {background};"
            "color: white;"
            f"font-size: {fsize}px;"
            "font-weight: bold;")
        
        self.setAlignment(align)
        self.setGeometry(3,3,198,27)

class CustomFrame(QFrame): 
    def __init__(self, parent=None, background="#000000"):
        super().__init__(parent)
        self.setStyleSheet(f"background: {background};"
                           "border: 1px;"
                           "border-radius: 5px;") 

class CustomGraph(pg.PlotWidget):
    def __init__(self, name="", units="",  pen=pg.mkPen("#0BBB10"), brush=(52,131,54,50), parent=None):
        super().__init__(parent)
        self.showGrid(x=True, y=True) 
        self.setLabel('left', name, units=units)
        self.setLabel('bottom', 'Tiempo', units='s')
        self.setXRange(0,15)
        self.data = self.plot(pen=pen,fillLevel=0, brush=brush)

class AltitudeWidget(QFrame): 
    def __init__(self, parent=None, label="ALTITUD"):
        self.frame = CustomFrame(parent=parent, background="#151515")
        self.bar = QProgressBar(self.frame)
        self.bar.setOrientation(Qt.Vertical)
        self.bar .setStyleSheet("QProgressBar{border: 2px solid white;"
                                    "border-radius: 1px;"
                                    "text-align: center;}"
                                    "QProgressBar::chunk {background-color: red;}")     
        self.bar.setTextVisible(False)
        self.bar.setRange(0,500) 
        self.frame_name = CustomFrame(self.frame, "#00BDFF")
        self.label_name = CustomLabel(label,self.frame_name) 
        self.altura = CustomLabel(parent=self.frame) 
        self.piso_marca = CustomFrame(self.frame, "white")
        self.autogiro_marca = CustomFrame(self.frame, "white")
        self.drone_marca = CustomFrame(self.frame, "white")
        self.max_marca = CustomFrame(self.frame, "white")
        self.piso_label = CustomLabel("0 m", self.frame, 12, "#151515",Qt.AlignLeft) 
        self.autogiro_label = CustomLabel("200 m", self.frame, 12, "#151515", Qt.AlignLeft)
        self.drone_label = CustomLabel("450 m", self.frame, 12, "#151515", Qt.AlignLeft)
        self.max_label = CustomLabel("500 m", self.frame, 12, "#151515", Qt.AlignLeft)

    def Resize(self):
        width_f, height_f = self.frame.geometry().width(), self.frame.geometry().height()
        self.bar.setGeometry(int(width_f*0.3),int(height_f*0.05),int(width_f*0.1), int(height_f*0.73))
        self.frame_name.setGeometry(int(width_f*0.1), int(height_f*0.82), int(width_f*0.8), 30)
        self.label_name.setGeometry(3,3,self.frame_name.geometry().width() - 3, 28)
        self.altura.setGeometry(int(width_f*0.1), int(height_f*0.9), int(width_f*0.8), 30)
        self.piso_marca.setGeometry(int(width_f*0.3), int(height_f*0.78) - 2, int(width_f*0.25), 2)
        self.autogiro_marca.setGeometry(int(width_f*0.3), int(height_f*0.05) + int(self.bar.geometry().height()*0.6) - 3, int(width_f*0.25), 2)
        self.drone_marca.setGeometry(int(width_f*0.3), int(height_f*0.05) + int(self.bar.geometry().height()*0.1) - 3, int(width_f*0.25), 2)
        self.max_marca.setGeometry(int(width_f*0.3), int(height_f*0.05), int(width_f*0.25), 2)
        self.piso_label.setGeometry(int(width_f*0.565), int(height_f*0.78) - 9, int(width_f*0.24), int(16))
        self.autogiro_label.setGeometry(int(width_f*0.565), int(height_f*0.05) + int(self.bar.geometry().height()*0.6) - 10, int(width_f*0.24), int(16))
        self.drone_label.setGeometry(int(width_f*0.565),  int(height_f*0.05) + int(self.bar.geometry().height()*0.1)  - 9, int(width_f*0.24), int(16))
        self.max_label.setGeometry(int(width_f*0.565), int(height_f*0.05) - 8, int(width_f*0.239), int(16))
