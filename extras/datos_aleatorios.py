import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class SatelliteDataGenerator:
    def __init__(self):
        self.df = pd.DataFrame({
            'Paquetes': [],
            'Tiempo de misión (s)': [],
            'Hora': [],
            'Estado de la misión': [],
            'Servo': [],
            'Latitud': [],
            'Longitud': [],
            'Temperatura': [],
            'Presión': [],
            'Altitud': [],
            'Aceleración en X': [],
            'Aceleración en Y': [],
            'Aceleración en Z': [],
            'Giro X': [],
            'Giro Y': [],
            'Giro Z': [],
            'Ángulo X': [],
            'Ángulo Y': [],
            'Ángulo Z': [],
            'Brujula': [], 
            'Bateria': [],
            'CO2': [],
            'Humedad': []
        })
        
        self.package_count = 0
        self.mission_time_seconds = 0
        self.start_time = datetime.now()
        self.base_lat = random.uniform(-90, 90)
        self.base_lon = random.uniform(-180, 180)
        self.altitude = 0 
        self.current_compass = 0.0  # Valor inicial de la brújula
        self.compass_direction = 1  # 1 para aumentar, -1 para disminuir
        self.angulo_x = 0 
        self.angulo_y = 0 
        self.angulo_z = 0
        
    def generate_data(self, num_samples=100):
        for _ in range(num_samples):
            self.package_count += 1
            time_increment = 0.033
            self.mission_time_seconds = round(self.mission_time_seconds + time_increment, 3)
            
            # Cálculo de altitud
            gravity = 9.8 
            velocity_elevation = 5 
            velocity_fall = 10

            if self.mission_time_seconds  <= 90: 
                self.altitude += time_increment*velocity_elevation 
            elif 90 < self.mission_time_seconds and self.mission_time_seconds <= 98.456: 
                tiempo = self.mission_time_seconds - 90 
                self.altitude = 450 - (gravity / 2) * tiempo ** 2 
            elif 98.456 < self.mission_time_seconds and self.mission_time_seconds <= 108.4:  
                self.altitude -= velocity_fall*time_increment
            else: 
                self.altitude = 0 
            # Actualización de la brújula con cambio lineal
            compass_increment = 0.20
            self.current_compass += compass_increment
            
            # Cambiar dirección si alcanza los límites
            if self.current_compass >= 360: 
                self.current_compass -= 360
                
            mission_status = 1

            self.angulo_x += 1 
            if self.angulo_x > 360: 
                self.angulo_x = 0
            self.angulo_y += 2 
            if self.angulo_y > 360: 
                self.angulo_y = 0 
            self.angulo_z += 0.25 
            if self.angulo_z > 360: 
                self.angulo_z = 0 
            
            new_row = {
                'Paquetes': np.int64(self.package_count),
                'Tiempo de misión (s)': self.mission_time_seconds,
                'Hora': (self.start_time + timedelta(seconds=self.mission_time_seconds)).strftime("%H:%M:%S"),
                'Estado de la misión': mission_status,
                'Servo': random.choice([0, 1]),
                'Latitud': round(random.uniform(19.502454291471974,19.50264291471974),5),
                'Longitud': -round(random.uniform(99.13312701719184, 99.13332701719184),5),
                'Temperatura': round(random.uniform(-50, 50), 3),
                'Presión': round(random.uniform(800, 1200), 3),
                'Altitud': round(self.altitude, 3),
                'Aceleración en X': round(random.uniform(-2, 2), 3),
                'Aceleración en Y': round(random.uniform(-2, 2), 3),
                'Aceleración en Z': round(random.uniform(0.95, 1.02), 3),
                'Giro X': round(random.uniform(0, 360), 3),
                'Giro Y': round(random.uniform(0, 360), 3),
                'Giro Z': round(random.uniform(0, 360), 3),
                'Ángulo X': self.angulo_x,
                'Ángulo Y': self.angulo_y,
                'Ángulo Z': self.angulo_z,
                'Brujula': round(self.current_compass, 3),  # Valor lineal 0-180°
                'Bateria': round(random.uniform(0, 100), 3),
                'CO2': round(random.uniform(300, 2000), 3),
                'Humedad': round(random.uniform(0, 100), 3)
            }
            
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
    
    def save_to_csv(self, filename='satellite_data.csv'):
        self.df['Estado de la misión'] = np.int64(self.df['Estado de la misión'])
        self.df['Paquetes'] = np.int64(self.df['Paquetes'])
        self.df['Servo'] = np.int64(self.df['Servo'])
        self.df.to_csv(filename, index=False, header=False)
        print(f"Datos guardados exitosamente en {filename}")

# Ejemplo de uso
if __name__ == "__main__":
    generator = SatelliteDataGenerator()
    generator.generate_data(10750)
    generator.save_to_csv('Datos_mis_simul.csv')
