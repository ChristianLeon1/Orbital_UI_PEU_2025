#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2023 CREADOR: Christian Yael Ramírez León

import subprocess 

def PuertoDisponible(): 
    port = subprocess.run(['python3', '-m', 'serial.tools.list_ports'], capture_output=True) 
    port = str(port.stdout, 'utf-8')
    if len(port) == 0: 
        return 0 
    port = port.split('\n')
    port.remove('')
    for i in range(0,len(port)): 
        port[i] = port[i].strip()
    return port 
