#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2024 CREADOR: Christian Yael Ramírez León

import numpy as np

def Distancia(pos_1: list[float], pos_2: list[float]) -> float: 
    r = 6371000
    pos_1 = [pos_1[0]*2*np.pi/180, pos_1[1]*np.pi/180]
    pos_2 = [pos_2[0]*2*np.pi/180, pos_2[1]*np.pi/180]
    distancia = 2*r*np.arcsin(np.sqrt(np.sin((pos_2[1] - pos_1[1])/2)**2 + np.cos(pos_2[1])*np.cos(pos_1[1])*np.sin((pos_2[0] - pos_1[0])/2)**2))
    return round(distancia,2)


def Cambio_ID(ID: int): 
    if ID == 1: 
        return "ORB_CP" 
    elif ID == 2: 
        return "ORB_CS"

def LatitudGPS(latitud: str): 
    if "N" in latitud: 
        return float(latitud.rstrip("N"))
    elif "S" in latitud:
        return -float(latitud.rstrip("S"))

def LongitudGPS(longitud: str): 
    if "E" in longitud: 
        return float(longitud.rstrip("E"))
    elif "W" in longitud:
        return -float(longitud.rstrip("W"))

def EstadoSoftware(ES: int): 
    if ES == 0: 
        return "ACOPLADO" 
    elif ES == 2: 
        return "DESACOPLADO"
