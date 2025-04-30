from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QVector3D, QColor, QQuaternion
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DExtras import Qt3DExtras

class Ventana_3d(Qt3DExtras.Qt3DWindow): 
    def __init__(self): 
        super().__init__() 
        
        self.defaultFrameGraph().setClearColor(QColor(21, 21, 21))

        self.root_entity = Qt3DCore.QEntity() 
        self.camara = self.camera() 
        self.camara.setPosition(QVector3D(0, 0, 200))
        self.camara.setViewCenter(QVector3D(0,0,0))
        self.camara.setUpVector(QVector3D(0, 1, 0))
        self.camara.setFieldOfView(100)  
        self.camera_transform = Qt3DCore.QTransform()
        self.camera_entity = Qt3DCore.QEntity(self.root_entity)

        self.setup_lights()
        self.load_3d_model()
        self.setRootEntity(self.root_entity) 

        cam_controller = Qt3DExtras.QOrbitCameraController(self.root_entity)
        cam_controller.setLinearSpeed(50)
        cam_controller.setLookSpeed(180)
        cam_controller.setCamera(self.camara)
   
    def setup_lights(self): 

        self.spotlight_entity = Qt3DCore.QEntity(self.root_entity)
        
        self.spotlight = Qt3DRender.QSpotLight(self.spotlight_entity)
        self.spotlight.setColor(QColor(255, 255, 255))
        self.spotlight.setIntensity(1.5)
        self.spotlight.setCutOffAngle(150)
        self.spotlight.setConstantAttenuation(1.0)
        self.spotlight.setLinearAttenuation(0.0)
        self.spotlight.setQuadraticAttenuation(0.0)
        
        self.spotlight_transform = Qt3DCore.QTransform()
        self.spotlight_entity.addComponent(self.spotlight_transform)
        self.spotlight_entity.addComponent(self.spotlight)
        self.spotlight_transform.setTranslation(QVector3D(0,0,200))

    def load_3d_model(self):

        materials = self.load_mtl_materials("CANSAT.mtl")
        
        model_entity = Qt3DCore.QEntity(self.root_entity)
        
        mesh = Qt3DRender.QMesh(model_entity)
        self.model_path = Path(__file__).parent.parent / "models" / "CANSAT.obj" 
        mesh.setSource(QUrl.fromLocalFile(str(self.model_path)))
        
        material_name = "material96"  
        if material_name in materials:
            material = Qt3DExtras.QPhongMaterial(model_entity)
            material.setDiffuse(QColor(47, 68, 124))
            material.setSpecular(QColor(30, 30, 30))  
            material.setShininess(100) 
        
        self.model_transform = Qt3DCore.QTransform()
        self.model_transform.setScale(1) 

        model_entity.addComponent(mesh)
        model_entity.addComponent(material)
        model_entity.addComponent(self.model_transform) 

    def load_mtl_materials(self, mtl_path):
        mtl_file = Path(__file__).parent.parent / "models" / mtl_path
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

    def set_rotation(self, pitch, yaw, roll):
        # Orden de aplicación: roll (Z), pitch (X), yaw (Y)
        euler_rotation = QVector3D(roll, pitch, yaw)
        self.model_transform.setRotation(QQuaternion.fromEulerAngles(euler_rotation))
