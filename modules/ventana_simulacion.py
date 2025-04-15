from pathlib import Path
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QVector3D, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DExtras import Qt3DExtras

class Ventana_3d(Qt3DExtras.Qt3DWindow): 
    def __init__(self): 
        super().__init__() 

        # Entidad raiz 
        self.root_entity = Qt3DCore.QEntity() 
        
        # Configurar camaras 

        self.camara = self.camera() 

        self.camara.setPosition(QVector3D(-10, 0, 200))
        self.camara.setViewCenter(QVector3D(-10, 0, 0))
        self.camara.setUpVector(QVector3D(0, 1, 0))
        self.camara.setFieldOfView(100) 
       # Configurar luces
        self.setup_lights()
        # Cargar modelo 3D
        self.load_3d_model()
        
        # Configurar control de cámara
        cam_controller = Qt3DExtras.QOrbitCameraController(self.root_entity)
        cam_controller.setLinearSpeed(50)
        cam_controller.setLookSpeed(180)
        cam_controller.setCamera(self.camara)

        self.setRootEntity(self.root_entity)
   
    def setup_lights(self):
    # Luz puntual 1
        light_entity = Qt3DCore.QEntity(self.root_entity)
        light = Qt3DRender.QPointLight(light_entity)
        light.setColor(QColor(255, 255, 255))
        light.setIntensity(1.0)
        light_entity.addComponent(light)
        
        light_transform = Qt3DCore.QTransform()
        light_transform.setTranslation(QVector3D(-10, 0, 200))  # Posición ajustada
        light_entity.addComponent(light_transform)

        # Luz puntual 2
        light_entity2 = Qt3DCore.QEntity(self.root_entity)
        light2 = Qt3DRender.QPointLight(light_entity2)
        light2.setColor(QColor(255, 255, 255))
        light2.setIntensity(1.0)
        light_entity2.addComponent(light2)

        light_transform2 = Qt3DCore.QTransform()
        light_transform2.setTranslation(QVector3D(10, 10, 0))  # Posición diferente
        light_entity2.addComponent(light_transform2)

        # Luz direccional (en lugar de luz ambiental)
        directional_light_entity = Qt3DCore.QEntity(self.root_entity)
        directional_light = Qt3DRender.QDirectionalLight(directional_light_entity)
        directional_light.setColor(QColor(200, 200, 200))  # Color de la luz
        directional_light.setIntensity(1.0)  # Intensidad de la luz
        directional_light_entity.addComponent(directional_light)

        # Configurar la dirección de la luz
        light_direction = QVector3D(-1, -1, -1)  # Dirección de la luz
        light_direction.normalize()  # Normalizar el vector
        directional_light.setWorldDirection(light_direction)

    def load_3d_model(self):
    # Cargar materiales desde el .mtl
        materials = self.load_mtl_materials("CANSAT.mtl")
        
        # Crear una entidad principal para el modelo
        model_entity = Qt3DCore.QEntity(self.root_entity)
        
        # Cargar malla
        mesh = Qt3DRender.QMesh(model_entity)
        model_path = Path(__file__).parent / "CANSAT.obj"
        mesh.setSource(QUrl.fromLocalFile(str(model_path)))
        
        # Asignar el primer material (ejemplo básico)
        # Nota: Esto aplicará solo un material. Para múltiples materiales, necesitas subentidades.
        material_name = "material96"  # Cambia esto según tu modelo
        if material_name in materials:
            mtl_data = materials[material_name]
            material = Qt3DExtras.QPhongMaterial(model_entity)
            material.setDiffuse(QColor(
                int(mtl_data['Kd'][0] * 255),
                int(mtl_data['Kd'][1] * 255),
                int(mtl_data['Kd'][2] * 255)
            ))
            material.setSpecular(QColor(
                int(mtl_data['Ks'][0] * 255),
                int(mtl_data['Ks'][1] * 255),
                int(mtl_data['Ks'][2] * 255)
            ))
        
        # Configurar transformación
        transform = Qt3DCore.QTransform()
        transform.setScale(0.5)
        
        # Ensamblar componentes
        model_entity.addComponent(mesh)
        model_entity.addComponent(material)
        model_entity.addComponent(transform)

    def load_mtl_materials(self, mtl_path):
        mtl_file = Path(__file__).parent / mtl_path
        materials = {}
        current_mtl = None

        with open(mtl_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                if parts[0] == 'newmtl':
                    current_mtl = parts[1]
                    materials[current_mtl] = {
                        'Ka': (1.0, 1.0, 1.0),  # Por defecto
                        'Kd': (0.8, 0.8, 0.8),  # Por defecto
                        'Ks': (0.0, 0.0, 0.0),  # Por defecto
                    }
                elif current_mtl:
                    if parts[0] == 'Ka':
                        materials[current_mtl]['Ka'] = (float(parts[1]), float(parts[2]), float(parts[3]))
                    elif parts[0] == 'Kd':
                        materials[current_mtl]['Kd'] = (float(parts[1]), float(parts[2]), float(parts[3]))
                    elif parts[0] == 'Ks':
                        materials[current_mtl]['Ks'] = (float(parts[1]), float(parts[2]), float(parts[3]))

        return materials

