#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QAction, QKeySequence, QPixmap, QResizeEvent, Qt, QVector3D, QColor
from PySide6.QtWidgets import QMainWindow, QToolBar, QComboBox, QLabel, QStatusBar, QFrame, QTabWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView 
from PySide6.Qt3DCore import Qt3DCore 
from PySide6.Qt3DRender import Qt3DRender 
from PySide6.Qt3DExtras import Qt3DExtras 
from modules.tab_style import ColorTab 
from modules.custom_widgets import *
from modules.gaugemeter import AnalogGaugeWidget
from modules.compass import Compass
from modules.ventana_simulacion import *
import folium 
class WidgetsIn(QMainWindow):  
    def __init__(self): 
        super().__init__() 

    def IncluirWidgetsConfig(self): 

        #Ajustes app 
        self.logo = QPixmap("images/Logo.png")
        self.setWindowIcon(self.logo)
        self.setWindowTitle("Estación Terrena ORBITAL")
        self.setObjectName("Estación Terrena ORBITAL")
        self.setStyleSheet("background-color: black;"
                        "color: white;"
                        "selection-color: #DFDFDF;"
                        "selection-background-color: #242424")
        self.setFixedSize(int(1920*0.9), int(1080*0.9))

        #Menubar 
        self.menubar = self.menuBar()
        self.archivo_menu = self.menubar.addMenu("Archivo") 
        self.guardar_csv = self.archivo_menu.addAction("Guardar CSV")
        self.guardar_csv.setShortcut(QKeySequence("Ctrl+s"))
        self.salir_app = self.archivo_menu.addAction("Salir")
        self.salir_app.setShortcut(QKeySequence("Ctrl+q"))
        self.ventanas_menu = self.menubar.addMenu("Herramientas") 
        self.abrir_serial_monitor = self.ventanas_menu.addAction("Monitor Serial")

        #Toolbar 
        self.toolbar = QToolBar("Herramientas") 
        self.toolbar.setIconSize(QSize(16,16))
        self.addToolBar(self.toolbar) 
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        #Combo box configuración serial. 
        label_baud = QLabel("Baudrate: ")
        self.baud_opts = QComboBox()
        self.baud_opts.addItems(['9600', '19200', '31250', '38400', '57600', '74880', '115200', '230400', '250000', '460800', '500000', '921600', '1000000', '2000000'])
        self.baud_opts.setCurrentIndex(-1)
        self.serial_opts = QComboBox() 
        label_serial = QLabel("Puertos Disponibles: ")
        
        #Agregar ubicación del objetivo
        label_pos = QLabel("Ubicación del objetivo: ")
        self.latitud = QLineEdit()
        self.longitud = QLineEdit()
        self.altura = QLineEdit()
        self.latitud.setFixedWidth(60)
        self.longitud.setFixedWidth(60)
        self.altura.setFixedWidth(60)
        self.latitud.setStyleSheet("background: #212121")
        self.longitud.setStyleSheet("background: #212121")
        self.altura.setStyleSheet("background: #212121")
        # Botones 
        self.boton_actualizar = QAction("Actualizar Puertos")
        self.boton_conec_ser = QAction("Conectar")
        self.boton_descon = QAction("Desconectar")
        self.boton_posicion = QAction("Actualizar")
        self.boton_calib_altura = QAction("Calibrar Altura")
        self.boton_act_servo = QAction("Activar Servo")
        self.boton_des_servo = QAction("Desactivar Servo")
        self.boton_conec_ser.setEnabled(False)
        self.boton_descon.setEnabled(False)
        
        #Widgets en el toolbar 
        self.toolbar.addWidget(label_baud)
        self.toolbar.addWidget(self.baud_opts)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_serial) 
        self.toolbar.addWidget(self.serial_opts)
        self.toolbar.addAction(self.boton_actualizar)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_conec_ser) 
        self.toolbar.addAction(self.boton_descon) 
        self.toolbar.addSeparator()
        self.toolbar.addWidget(label_pos)
        self.toolbar.addWidget(self.latitud)
        self.toolbar.addWidget(self.longitud)
        self.toolbar.addAction(self.boton_posicion)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.altura)
        self.toolbar.addAction(self.boton_calib_altura)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.boton_act_servo)
        self.toolbar.addAction(self.boton_des_servo)

        # Status Bar 
        self.setStatusBar(QStatusBar(self))
        
        #Sensores 
        self.frame_sensores = CustomFrame(parent=self, background="#151515")
        self.tiempo_vuelo_label = CustomLabel("T V:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.contador_paquetes_label = CustomLabel("C P:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.hora_label = CustomLabel("HORA:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.bateria_label = CustomLabel("BATERIA:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)
        self.estado_label = CustomLabel("ESTADO:", self.frame_sensores, 20, "#151515", Qt.AlignLeft)

        self.tiempo_vuelo = CustomLabel(parent=self.frame_sensores)
        self.contador_paquetes = CustomLabel(parent=self.frame_sensores)
        self.hora = CustomLabel(parent=self.frame_sensores)
        self.bateria = CustomLabel(parent=self.frame_sensores)
        self.estado = CustomLabel(parent=self.frame_sensores)

        self.altura_cp = AltitudeWidget(parent=self, label="ALTITUD")

        self.frame_medidores = CustomFrame(parent=self, background="#151515")
        self.velocidad_label = CustomLabel("VELOCIDAD", self.frame_medidores, 20, "#151515")
        self.aceleracion_label = CustomLabel("ACELERACIÓN", self.frame_medidores, 20, "#151515") 
        self.brujula_label = CustomLabel("BRÚJULA", self.frame_medidores, 20, "#151515") 
        self.velocidad =CustomLabel("", self.frame_medidores) 
        self.aceleracion = CustomLabel("", self.frame_medidores)
        self.brujula = CustomLabel("", self.frame_medidores)

        self.velocimetro = AnalogGaugeWidget(self.frame_medidores) 
        self.velocimetro.maxValue = 120  
        self.velocimetro.enable_value_text = False 
        self.velocimetro.setGaugeTheme(2)
        self.acelerometro = AnalogGaugeWidget(self.frame_medidores) 
        self.acelerometro.maxValue = 20
        self.acelerometro.enable_value_text = False 
        self.acelerometro.setGaugeTheme(2)
        self.brujula_widget = Compass(self.frame_medidores) 
        self.brujula_widget.enable_value_text = False 

        # Graficas 
        self.temp_frame = CustomFrame(parent=self, background="#151515") 
        self.carbono_frame = CustomFrame(parent=self, background="#151515") 
        self.presion_frame = CustomFrame(parent=self, background="#151515")
        self.carbono_container = QVBoxLayout(self.carbono_frame)
        self.temp_container = QVBoxLayout(self.temp_frame)
        self.presion_container = QVBoxLayout(self.presion_frame)

        self.carbono = CustomGraph("CO2", "ppm")
        self.temp = CustomGraph("Temperatura", "°C")
        self.presion = CustomGraph("Presión", "Pa")
        self.carbono_container.addWidget(self.carbono)
        self.temp_container.addWidget(self.temp)
        self.presion_container.addWidget(self.presion)
        self.carbono.setYRange(0,5)
        self.temp.setYRange(0,40)
        self.presion.setYRange(75000,80000)

        # GPS
        self.gps_frame = CustomFrame(self,"#151515")
        self.gps_w = QWebEngineView(self.gps_frame)
        # self.maps = folium.Map(location = [19.4284, -99.1276], zoom_start=4)

        self.maps = folium.Map(
            location=[19.4284, -99.1276],
            zoom_start=4, 
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", 
            attr='Esri World Imagery'
        )
        self.gps_w.setHtml(self.maps.get_root().render())

        # Simulación 3D 
        self.simulacion_frame = CustomFrame(self, "#151515")
        self.simulacion_container = QVBoxLayout(self.simulacion_frame) 
        self.ventana_3d = Ventana_3d() 
        # self.ventana_3d.setup_lights() 
        # self.ventana_3d.load_3d_model()  

        self.ventana_container = QWidget.createWindowContainer(self.ventana_3d)
        self.simulacion_container.addWidget(self.ventana_container)

        # #Tab monitor serial
        # self.tab_serial_monitor.setStyleSheet("border-radius: 5px;")
        # self.serial_mon_frame = CustomFrame(self.tab_serial_monitor,"#151515")
        # self.serial_monitor = QTextEdit(self.serial_mon_frame)
        # self.limpiar_ser_mon = QPushButton(self.serial_mon_frame)
        # self.limpiar_ser_mon.setText("Limpiar")
        # self.datos_a_serial = QLineEdit(self.serial_mon_frame)
        # self.datos_a_serial.setPlaceholderText("Mensaje (Enter para enviar el mensaje)")
        # self.datos_a_serial.setEnabled(False)
        # self.serial_monitor.setReadOnly(True)
        # self.serial_monitor.setStyleSheet("background: #050505;"
        #                                   "border: 1px solid #5A5C5F;"
        #                                   "border-radius: 5px;"
        #                                   )
        # self.limpiar_ser_mon.setStyleSheet("background: #111111;"
        #                                   "border: 1px solid #5A5C5F;"
        #                                   "border-radius: 5px;"
        #                                   )
        # self.datos_a_serial.setStyleSheet("background: #1D1D1D;"
        #                                 "border: 1px solid #5A5C5F;"
        #                                 "border-radius: 5px;"
        #                                 )


    def resizeEvent(self, event: QResizeEvent) -> None:
        width = self.geometry().width()
        height = self.geometry().height()

        # #GPS 
        self.gps_frame.setGeometry(int(0.005*width), int(0.59*height), int(0.41*width), int(0.36*height))
        self.gps_w.setGeometry(int(0.02*self.gps_frame.geometry().width()), int(0.03*self.gps_frame.geometry().height()), int(0.96*self.gps_frame.geometry().width()), int(0.94*self.gps_frame.geometry().height()))
        
        # #Monitor Serial
        # self.serial_mon_frame.setGeometry(int(0.01*width_f), int(0.05*height_f), int(0.95*width_f), int(0.9*height_f) - 31)
        # self.serial_monitor.setGeometry(int(self.serial_mon_frame.geometry().width()*0.01), int(self.serial_mon_frame.geometry().height()*0.05), int(self.serial_mon_frame.geometry().width()*0.98), int(self.serial_mon_frame.geometry().height()*0.85))
        # self.limpiar_ser_mon.setGeometry(int(self.serial_mon_frame.geometry().width()*0.92), int(self.serial_mon_frame.geometry().height()*0.92), int(self.serial_mon_frame.geometry().width()*0.07), int(self.serial_mon_frame.geometry().height()*0.06))
        # self.datos_a_serial.setGeometry(int(self.serial_mon_frame.geometry().width()*0.01), int(self.serial_mon_frame.geometry().height()*0.92), int(self.serial_mon_frame.geometry().width()*0.90), int(self.serial_mon_frame.geometry().height()*0.06))

        # # Gráficas 
        self.presion_frame.setGeometry(int(width*0.42), int(height*0.08), int(width*(0.24)), int(height*0.28))  
        self.temp_frame.setGeometry(int(width*0.42), int(height*(0.08 + 0.295)), int(width*(0.24)), int(height*0.28)) 
        self.carbono_frame.setGeometry(int(width*0.42), int(height*(0.08 + 2*0.295)), int(width*(0.24)), int(height*0.28))
 
        # Datos de los sensores:  
        self.frame_sensores.setGeometry(int(width*0.762), int(height*0.4), int(width*0.22), int(height*0.55)) 
 
        width_f, height_f = self.frame_sensores.geometry().width(), self.frame_sensores.geometry().height() 
        self.tiempo_vuelo_label.setGeometry(int(width_f*0.08), int(height_f/6) - 15, int(width_f*0.38), 30)
        self.contador_paquetes_label.setGeometry(int(width_f*0.08), 2*int(height_f/6) - 15, int(width_f*0.37), 30)        
        self.hora_label.setGeometry(int(width_f*0.08), 3*int(height_f/6) - 15, int(width_f*0.37), 30)
        self.bateria_label.setGeometry(int(width_f*0.08), 4*int(height_f/6) - 15, int(width_f*0.37), 30)
        self.estado_label.setGeometry(int(width_f*0.08), 5*int(height_f/6) - 15, int(width_f*0.37), 30)

        self.tiempo_vuelo.setGeometry(int(width_f*0.55), 1*int(height_f/6) - 15, int(width_f*0.35), 30)
        self.contador_paquetes.setGeometry(int(width_f*0.55), 2*int(height_f/6) - 15, int(width_f*0.35), 30)
        self.hora.setGeometry(int(width_f*0.55), 3*int(height_f/6) - 15, int(width_f*0.35), 30)
        self.bateria.setGeometry(int(width_f*0.55), 4*int(height_f/6) - 15, int(width_f*0.35), 30)
        self.estado.setGeometry(int(width_f*0.55), 5*int(height_f/6) - 15, int(width_f*0.35), 30)

        #Altitud 
        self.altura_cp.frame.setGeometry(int(width*0.67), int(height*0.4), int(width*0.085), int(height*0.55))
        self.altura_cp.Resize()

        # Espacio para los medidores  

        self.frame_medidores.setGeometry(int(width*0.67), int(height*0.08), int(width*0.312), int(height*0.3)) 
        width_f, height_f = self.frame_medidores.geometry().width(), self.frame_medidores.geometry().height() 
        self.velocimetro.setGeometry(int(width_f*0.03), int(height_f*0.08), int(width_f*0.30), int(height_f*0.6)) 
        self.velocidad_label.setGeometry(int(width_f*0.03), int(height_f*0.65), int(width_f*0.30), int(30)) 
        self.velocidad.setGeometry(int(width_f*0.03), int(height_f*0.65) + 35, int(width_f*0.30), int(30)) 
        self.acelerometro.setGeometry(int(width_f*0.35), int(height_f*0.08), int(width_f*0.30), int(height_f*0.6)) 
        self.aceleracion_label.setGeometry(int(width_f*0.35), int(height_f*0.65), int(width_f*0.30), int(30)) 
        self.aceleracion.setGeometry(int(width_f*0.35), int(height_f*0.65) + 35, int(width_f*0.30), int(30)) 
        self.brujula_widget.setGeometry(int(width_f*0.67), int(height_f*0.08), int(width_f*0.30), int(height_f*0.6)) 
        self.brujula_label.setGeometry(int(width_f*0.67), int(height_f*0.65), int(width_f*0.30), int(30)) 
        self.brujula.setGeometry(int(width_f*0.67), int(height_f*0.65) + 35, int(width_f*0.30), int(30)) 


        # Simulación 3d 

        self.simulacion_frame.setGeometry(int(0.005*width), int(0.08*height), int(0.41*width), int(0.5*height))
        # width_f, height_f = self.simulacion_frame.geometry().width(), self.simulacion_frame.geometry().height() 
        # self.ventana_3d.setGeometry(int(0.05*width_f), int(0.05*height_f), int(0.9*width_f), int(0.9*height_f))
