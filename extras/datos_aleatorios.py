#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class SatelliteDataGenerator:
    def __init__(self):
        # Inicializar el DataFrame con la estructura especificada
        self.df = pd.DataFrame({
            'Paquetes': [],
            'Tiempo de misión': [],
            'Servo': [],
            'Latitud': [],
            'Longitud': [],
            'Temperatura': [],
            'Presión': [],
            'Altitud': [],
            'Aceleración en X': [],
            'Aceleración en Y': [],
            'Aceleración Z': [],
            'X': [],
            'Y': [],
            'Z': [],
            'Rotación X': [],
            'Rotación Y': [],
            'Rotación Z': [],
            'Brujula': [],
            'Bateria': [],
            'CO2': [],
            'Humedad': []
        })
        
        # Configuración inicial para generación de datos
        self.package_count = np.int64(0)
        self.mission_time = timedelta(seconds=0)
        self.base_lat = random.uniform(-90, 90)
        self.base_lon = random.uniform(-180, 180)
        
    def generate_data(self, num_samples=100):
        for _ in range(num_samples):
            self.package_count += 1
            self.mission_time += timedelta(seconds=random.uniform(0.1, 1.0))
            
            # Generar datos aleatorios para cada columna
            new_row = {
                'Paquetes': self.package_count,
                'Tiempo de misión': str(self.mission_time),
                'Servo': random.choice([0, 1]),
                'Latitud': self.base_lat + random.uniform(-0.01, 0.01),
                'Longitud': self.base_lon + random.uniform(-0.01, 0.01),
                'Temperatura': random.uniform(-50, 50),
                'Presión': random.uniform(800, 1200),
                'Altitud': random.uniform(100, 1000),
                'Aceleración en X': random.uniform(-2, 2),
                'Aceleración en Y': random.uniform(-2, 2),
                'Aceleración Z': random.uniform(-2, 2),
                'X': random.uniform(-1, 1),
                'Y': random.uniform(-1, 1),
                'Z': random.uniform(-1, 1),
                'Rotación X': random.uniform(0, 360),
                'Rotación Y': random.uniform(0, 360),
                'Rotación Z': random.uniform(0, 360),
                'Brujula': random.uniform(0, 360),
                'Bateria': random.uniform(0, 100),
                'CO2': random.uniform(300, 2000),
                'Humedad': random.uniform(0, 100)
            }
            
            # Añadir la nueva fila al DataFrame
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
    
    def save_to_csv(self, filename='satellite_data.csv'):
        self.df.to_csv(filename, index=False, header=False)
        print(f"Datos guardados exitosamente en {filename}")

# Ejemplo de uso
if __name__ == "__main__":
    print("Generando datos de misión satelital...")
    generator = SatelliteDataGenerator()
    generator.generate_data(1000)  # Generar 1000 muestras
    generator.save_to_csv()
    print("¡Datos generados exitosamente!")

