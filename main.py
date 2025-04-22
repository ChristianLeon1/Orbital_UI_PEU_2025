#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León 

# Estación terrena para competencia CANSAT PEU 2025 
# Interfaz de usuario para la estación terrena de cansat

import sys 
import os
import pandas as pd 
import folium 
from pathlib import Path
from modules.config_widgets import *
from modules.serial_mod import *
from modules.distancia_coord import *
from PySide6.QtCore import QIODevice, QTimer
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QApplication, QMessageBox
import time

class MainWindow(WidgetsIn): 

    def __init__(self) -> None: 

        super(MainWindow, self).__init__()          
        self.app = app 
        self.tiempo_transcur_cp = [0]
        
        self.cp = pd.DataFrame({'Paquetes':[],
                                'Tiempo de misión':[],
                                'Hora':[], 
                                'Estado de la misión':[],
                                'Servo':[],
                                'Latitud':[],
                                'Longitud':[],
                                'Temperatura':[],
                                'Presión':[],
                                'Altitud':[],
                                'Aceleración en X':[],
                                'Aceleración en Y':[],
                                'Aceleración en Z':[],
                                'Giro X':[],
                                'Giro Y':[],
                                'Giro Z':[],
                                'Ángulo X':[],
                                'Ángulo Y':[],
                                'Ángulo Z':[],
                                'Brujula':[],
                                'Bateria':[],
                                'CO2':[],
                                'Humedad':[]
                                })

        self.graficas = pd.DataFrame({'Tiempo': [],
                                      'CO2': [],
                                      'Presión':[], 
                                      'Temperatura':[]})

        self.names = self.cp.columns 
        self.cp_index = len(self.cp.index) - 1

        #Inicialización de variables 
        self.baud_rate = None
        self.port = None 
        self.sensores_timer = QTimer(self)
        self.gps_timer = QTimer(self)
        self.graficas_timer = QTimer(self)
        self.flag = False
        self.flag_act = True
        self.posicion = [0,0]
        self.graf_x = 15
        self.pos_objetivo = [0,0]
        self.lag_objetivo = False
        self.ajuste_altura = 0
        self.IncluirWidgetsConfig()
        #Configuración serial 
        self.ser = QSerialPort()        
        self.ActualizarSerial() 

        # Señales 
        #Botones 
        self.boton_actualizar.triggered.connect(self.ActualizarSerial)
        self.boton_conec_ser.triggered.connect(self.ConectarPort) 
        self.boton_descon.triggered.connect(self.DescPort)
        #Combobox  
        self.baud_opts.currentTextChanged.connect(self.GuardarBaudRate)
        self.serial_opts.currentTextChanged.connect(self.GuardarSerialPort)
        # Menubar
        self.salir_app.triggered.connect(self.SalirApp) 
        self.guardar_csv.triggered.connect(self.GuardarCSV)
        #Puerto serial
        self.ser.readyRead.connect(self.LeerDatos)
        
        #Monitor serial 
        # self.limpiar_ser_mon.clicked.connect(self.LimpiarSerial)
        # self.datos_a_serial.returnPressed.connect(self.EnviarSerial)
        self.boton_act_servo.triggered.connect(self.ActivarServo)
        self.boton_des_servo.triggered.connect(self.DesactivarServo)

        #Actualización de datos de los sensores
        self.sensores_timer.timeout.connect(self.ActualizarSensores)
        self.gps_timer.timeout.connect(self.ActualizarGPS)        
        self.graficas_timer.timeout.connect(self.ActualizarGraficas)

        #Calibración 
        self.boton_posicion.triggered.connect(self.ObjetivoPos)
        self.boton_calib_altura.triggered.connect(self.CalibAltura)

    def CalibAltura(self): 
        try:
            self.ajuste_altura = float(self.altura.text())
            self.statusBar().showMessage(f'Se guardo correctamente la Calibración de la altura: {self.ajuste_altura}', 8000)
        except: 
            self.statusBar().showMessage(f'No se ingreso un dato válido para calibrar la altura: {self.altura.text()}', 8000)

    def ObjetivoPos(self): 
        try: 
            latitud = float(self.latitud.text())
            longitud = float(self.longitud.text()) 
            self.pos_objetivo = [latitud, longitud]
            self.statusBar().showMessage(f'Se guardo la ubicación del objetivo correctamente: {self.pos_objetivo}', 8000)
            self.maps = folium.Map(location = self.pos_objetivo, zoom_start=16)
            folium.CircleMarker(location=self.pos_objetivo, radius=10, color="#FFE000", fill=True, border=True, opacity=0.7).add_to(self.maps)
            self.gps_w.setHtml(self.maps.get_root().render())
        except: 
            self.statusBar().showMessage(f'No se ingreso correctamente las coordenadas del objetivo. [{self.latitud.text()}, {self.longitud.text()}]', 8000)

    def GuardarBaudRate(self,text):
        self.baud_rate = int(text)
        if self.baud_rate != None and self.serial_opts.currentIndex() != -1: 
            self.boton_conec_ser.setEnabled(True)

    def GuardarSerialPort(self,text): 
        self.port = text 
        if self.baud_rate != None and self.serial_opts.currentIndex() != -1: 
            self.boton_conec_ser.setEnabled(True)

    def ActualizarSerial(self): 
        self.serial_opts.clear()
        self.serial_opts.setEnabled(True)
        if PuertoDisponible() == 0: 
            self.serial_opts.setEnabled(False)
        else: 
            self.serial_opts.addItems(PuertoDisponible())
            self.serial_opts.setCurrentIndex(-1)
        self.port = None
        self.boton_conec_ser.setEnabled(False) 

    def ConectarPort(self):  
        if self.baud_rate != None and self.port != None: 
            self.boton_calib_altura.setEnabled(False)
            self.boton_posicion.setEnabled(False)
            # self.datos_a_serial.setEnabled(True)
            self.boton_des_servo.setEnabled(True)
            self.boton_act_servo.setEnabled(True)
            self.ser.setPortName(self.port)
            self.ser.setBaudRate(self.baud_rate)
            if self.ser.open(QIODevice.ReadWrite): 
                self.statusBar().showMessage(f'Conectado al puerto {self.port}', 10000)
                self.boton_conec_ser.setEnabled(False)
                self.boton_descon.setEnabled(True)
            else: 
                self.statusBar().showMessage(f'No se pudo conectar al puerto{self.port}', 10000)
        else: 
            self.statusBar().showMessage(f'No se pudo conectar al puerto {self.port}', 10000)

    def EnviarSerial(self):
        # texto = self.datos_a_serial.text().encode("utf-8")
        # self.datos_a_serial.setText("")
        # self.ser.write(texto) 
        pass # Falta habilitar el monitor serial 

    def LimpiarSerial(self): 
        # self.serial_monitor.setText("") 
        pass

    def ActivarServo(self): 
        self.ser.write("1".encode("utf-8")) 


    def DesactivarServo(self):
        self.ser.write("0".encode("utf-8")) 

    def ActualizarGPS(self):

        if not (self.posicion[0] == self.cp['Latitud'][self.cp_index] and self.posicion[1] == self.cp['Longitud'][self.cp_index]):
            self.posicion = [self.cp['Latitud'][self.cp_index], self.cp['Longitud'][self.cp_index]]
            self.maps = folium.Map(location=self.posicion, zoom_start=18)
            folium.CircleMarker(location=self.posicion, radius=6, color="red", fill=True, border=True, opacity=0.7).add_to(self.maps)
            self.gps_w.setHtml(self.maps.get_root().render())
        self.gps_timer.start(4007)

    def ActualizarSensores(self): 
        #Identificadores
        self.hora.setText(f"{self.cp['Hora'][self.cp_index]}")
        self.contador_paquetes.setText(f"{self.cp['Paquetes'][self.cp_index]}")
        self.tiempo_vuelo.setText(f"{self.cp['Tiempo de misión'][self.cp_index]}")

        #Mensajes de sensores 
        self.estado.setText(f"{self.cp['Estado de la misión'][self.cp_index]}") 
        self.bateria.setText(f"{self.cp['Bateria'][self.cp_index]}") 
        self.brujula.setText(f"{self.cp['Brujula'][self.cp_index]}")
        self.aceleracion.setText(f"{self.cp['Aceleración en Z'][self.cp_index]}")
        self.sensores_timer.start(500)
        


    def ActualizarGraficas(self):
        if not self.cp['Tiempo de misión'][self.cp_index] < self.graf_x: 
            self.graf_x += 15
            self.temp.setXRange(self.graf_x - 15, self.graf_x)
            self.carbono.setXRange(self.graf_x - 15, self.graf_x)
            self.presion.setXRange(self.graf_x - 15, self.graf_x)  
            self.graficas = pd.DataFrame({'Tiempo': [],
                                          'CO2': [],
                                          'Presión':[], 
                                          'Temperatura':[]})
        new_row = {'Tiempo': self.cp['Tiempo de misión'][self.cp_index],
                  'CO2': self.cp['CO2'][self.cp_index],
                  'Presión': self.cp['Presión'][self.cp_index], 
                  'Temperatura': self.cp['Temperatura'][self.cp_index]
                   }

        self.graficas = pd.concat([self.graficas, pd.DataFrame([new_row])], ignore_index=True)

        self.carbono.data.setData(self.graficas['Tiempo'], self.graficas['CO2'])
        self.temp.data.setData(self.graficas['Tiempo'], self.graficas['Temperatura'])
        self.presion.data.setData(self.graficas['Tiempo'], self.graficas['Presión'])
        self.altura_cp.altura.setText(f"{self.cp['Altitud'][self.cp_index]} m")
        self.acelerometro.updateValue(self.cp['Aceleración en Z'][self.cp_index])
        self.brujula_widget.updateValue(self.cp['Brujula'][self.cp_index])
        if 0 <=  self.cp['Altitud'][self.cp_index] or  self.cp['Altitud'][self.cp_index] <= 500:
            self.altura_cp.bar.setValue(int(self.cp['Altitud'][self.cp_index]))
        else: 
            self.altura_cp.bar.setValue(500) 

        try: 
            if self.cp_index > 20: 
            
                velocidad = round((self.cp['Altitud'][self.cp_index - 20] - self.cp['Altitud'][self.cp_index]) /
                                  (self.cp['Tiempo de misión'][self.cp_index - 20] - self.cp['Tiempo de misión'][self.cp_index]), 2)

                if velocidad == 0: 
                    self.velocidad.setText(f"0.0") 
                    self.velocimetro.value = 0
                else: 
                    self.velocidad.setText(f"{velocidad}") 
                self.velocimetro.updateValue((abs(velocidad)))
            else: 
                self.velocidad.setText(f"0.0") 
        except: 
            pass 

        
        self.graficas_timer.start(79)
        
    def LeerDatos(self): 
        if not self.ser.canReadLine(): 
            return 
        try: 
            new_row = str(self.ser.readLine(),'utf-8')            
            new_row = new_row.strip("\n").split(',')
            if len(new_row) != 23: 
                return 

            if "\\r" in new_row: 
                new_row[22] = new_row[22].rsplit("\\r")

            new_row = {
                'Paquetes': new_row[0],
                'Tiempo de misión': new_row[1],
                'Hora':new_row[2],
                'Estado de la misión': new_row[3],
                'Servo': new_row[4], 
                'Latitud': new_row[5],
                'Longitud': new_row[6],
                'Temperatura': new_row[7],
                'Presión': new_row[8],
                'Altitud': new_row[9],
                'Aceleración en X': new_row[10],
                'Aceleración en Y': new_row[11],
                'Aceleración en Z': new_row[12],
                'Giro X': new_row[13],
                'Giro Y': new_row[14],
                'Giro Z': new_row[15],
                'Ángulo X': new_row[16],
                'Ángulo Y': new_row[17],
                'Ángulo Z': new_row[18],
                'Brujula': new_row[19],
                'Bateria': new_row[20],
                'CO2': new_row[21],
                'Humedad': new_row[22]
            }

            for i in self.cp.columns: 
                if new_row[i].isdigit(): 
                    new_row[i] = int(new_row[i]) 
                else: 
                    try: 
                        new_row[i] = float(new_row[i])
                    except: 
                        pass 
            
            self.cp = pd.concat([self.cp, pd.DataFrame([new_row])], ignore_index=True)
            
            if not self.flag: 
                self.flag = True 
                self.tiempo_inic = time.time() 

            self.cp_index = len(self.cp.index) - 1
            
            if (self.cp_index !=-1) and self.flag_act: 
                self.ActualizarGPS()
                self.ActualizarSensores() 
                self.ActualizarGraficas()
                self.flag_act = False
        except:
            pass

    def DescPort(self): 
        self.boton_conec_ser.setEnabled(True)
        self.boton_descon.setEnabled(False)
        self.boton_posicion.setEnabled(True)
        self.boton_calib_altura.setEnabled(True)
        self.boton_des_servo.setEnabled(False)
        self.boton_des_servo.setEnabled(False)
        if self.ser.isOpen: 
            self.ser.close()
            self.statusBar().showMessage(f'Se desconecto correctamente el puerto {self.port}', 10000)

    def GuardarCSV(self):  
        if len(self.cp.index) > 1: 
            self.cp.to_csv(f"Vuelo_.csv", header =True)
        else: 
            self.statusBar().showMessage(f"No hay ningun archivo por guardar.", 10000)
           
    def SalirApp(self): 
        self.app.quit()

    def closeEvent(self, event):
        flag = self.MensajeSalida()
        if flag == QMessageBox.Yes:
            self.GuardarCSV()
        self.DescPort()

    def MensajeSalida(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Salir")
        msg_box.setText("¿Desea guardar los datos de la misión?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg_box.exec()

if __name__ == "__main__": 
    os.environ["QT3D_RENDER"] = "opengl"
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec()) 
