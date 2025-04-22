#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León




from pathlib import Path
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QVector3D, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DExtras import Qt3DExtras
import sys  # Importación añadida
from ventana_simulacion import Ventana_3d

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar ventana principal
        self.setWindowTitle("Visor 3D")
        self.resize(800, 600)
        
        # Crear instancia del visor 3D
        self.viewer_3d = Ventana_3d()
        
        # Contenedor para integrar la ventana 3D en widgets Qt
        container = QWidget.createWindowContainer(self.viewer_3d)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = MainWindow()
    ventana_principal.show()
    sys.exit(app.exec())
