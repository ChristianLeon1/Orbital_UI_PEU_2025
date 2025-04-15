#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2023 CREADOR: Christian Yael Ramírez León

import sys 
from PySide6.QtSerialPort import QSerialPortInfo  # Módulo nativo de Qt para puertos seriales

def PuertoDisponible(): 
    names = []
    ports = QSerialPortInfo.availablePorts()
    if not ports: 
        return 0 
    for port in ports: 
        names.append(port.portName())
    return names
