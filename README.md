# Orbital_UI_PEU_2025 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide](https://img.shields.io/badge/PySide-6.0-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-orange)

Aplicación de estación terrena en Python para recibir y visualizar datos de satélites. Desarrollada con PySide6 para la interfaz gráfica y compatible con Windows y Linux.

## Características principales
- Recepción de datos en tiempo real vía puerto serial/USB.
- Visualización de telemetría (altitud, temperatura, voltaje, etc.).
- Gráficos dinámicos actualizados en tiempo real.
- Almacenamiento de datos en formato `.csv`. 
- Interfaz gráfica intuitiva con PySide6.
- Compatibilidad multiplataforma.

## Requisitos
- Python 3.8 o superior
- Sistema operativo Windows 10+ o Linux (Ubuntu/Debian recomendado)
- Acceso al puerto serial (permisos adecuados en Linux)

## Instalación

### Linux, macOS
#### 1. Clonar el repositorio:
```bash
git clone https://github.com/ChristianLeon1/Orbital_UI_PEU_2025.git 
cd Orbital_UI_PEU_2025 
```

#### 2. Crear entorno virtual y dependencias: 

```bash 
python3 venv -m .venv 
source .venv\bin\activate
pip3 install -r requirements.txt 
```

<!-- ## Dependencias linux  -->
<!---->
<!---->
<!---->
<!-- opengl mesa-utils -->
