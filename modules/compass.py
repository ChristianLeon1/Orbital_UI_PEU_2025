#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AÑO: 2025 CREADOR: Christian Yael Ramírez León


########################################################################
## IMPORTS
########################################################################

import os
import math

########################################################################
## MODULE UPDATED TO USE QTPY
########################################################################
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont, QPainter, QFontMetrics, QConicalGradient, QRadialGradient, QFontDatabase
from qtpy.QtCore import Qt, QTimer, QPoint, QPointF, QRect, QSize, QObject, Signal

from modules.log import *



################################################################################################
# AnalogGaugeWidget CLASS
################################################################################################
class Compass(QWidget):
    """Fetches rows from a Bigtable.
    Args: 
        none
    
    """
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(Compass, self).__init__(parent)

        ################################################################################################
        # DEFAULT TIMER VALUE
        ################################################################################################
        self.use_timer_event = False # Revisar para que el timer 

        ################################################################################################
        # DEFAULT NEEDLE COLOR
        ################################################################################################
        self.setNeedleColor(180, 0, 0, 255)

        ################################################################################################
        # DEFAULT NEEDLE WHEN RELEASED
        ################################################################################################
        self.NeedleColorReleased = self.NeedleColor

        ################################################################################################
        # DEFAULT NEEDLE COLOR ON DRAG
        ################################################################################################
        # self.NeedleColorDrag = QColor(255, 0, 00, 255)
        self.setNeedleColorOnDrag(255, 0, 00, 255)

        ################################################################################################
        # DEFAULT SCALE TEXT COLOR
        ################################################################################################
        self.setScaleValueColor(0, 0, 0, 255)

        ################################################################################################
        # DEFAULT VALUE COLOR
        ################################################################################################
        self.setDisplayValueColor(0, 0, 0, 255)

        ################################################################################################
        # DEFAULT CENTER POINTER COLOR
        ################################################################################################
        # self.CenterPointColor = QColor(50, 50, 50, 255)
        self.set_CenterPointColor(0, 0, 0, 255)

        ################################################################################################
        # DEFAULT NEEDLE COUNT
        ################################################################################################
        self.value_needle_count = 1

        self.value_needle = QObject

        ################################################################################################
        # DEFAULT MINIMUM AND MAXIMUM VALUE
        ################################################################################################
        self.minValue = 0
        self.maxValue = 360
        ################################################################################################
        # DEFAULT START VALUE
        ################################################################################################
        self.value = self.minValue

        ################################################################################################
        # DEFAULT OFFSET
        ################################################################################################
        self.value_offset = 0

        self.valueNeedleSnapzone = 0.05
        self.last_value = 0

        # self.value2 = 0
        # self.value2Color = QColor(0, 0, 0, 255)

        ################################################################################################
        # DEFAULT RADIUS
        ################################################################################################
        self.gauge_color_outer_radius_factor = 1
        self.gauge_color_inner_radius_factor = 0.9

        self.center_horizontal_value = 0
        self.center_vertical_value = 0

        ################################################################################################
        # DEFAULT SCALE VALUE
        ################################################################################################
        self.scale_angle_start_value = 270
        self.scale_angle_size = 360

        self.angle_offset = 0

        self.setScalaCount(8)   # Divisiones grandes
        self.scala_subdiv_count = 9 #Divisiones pequeñas 

        self.pen = QPen(QColor(0, 0, 0)) #Color de las divisiones 

        ################################################################################################
        # LOAD CUSTOM FONT
        ################################################################################################     
        # QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), 'fonts/Orbitron/Orbitron-VariableFont_wght.ttf') ) #Borrar 

        ################################################################################################
        # DEFAULT POLYGON COLOR
        ################################################################################################
        self.scale_polygon_colors = []

        ################################################################################################
        # BIG SCALE COLOR
        ################################################################################################
        self.bigScaleMarker = Qt.black

        ################################################################################################
        # FINE SCALE COLOR
        ################################################################################################
        self.fineScaleColor = Qt.black

        ################################################################################################
        # DEFAULT SCALE TEXT STATUS
        ################################################################################################
        self.setEnableScaleText(True)
        self.scale_fontname = "Orbitron"
        self.initial_scale_fontsize = 14
        self.scale_fontsize = self.initial_scale_fontsize

        ################################################################################################
        # DEFAULT VALUE TEXT STATUS
        ################################################################################################
        self.enable_value_text = True
        self.value_fontname = "Orbitron"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize
        self.text_radius_factor = 0.5

        ################################################################################################
        # ENABLE BAR GRAPH BY DEFAULT
        ################################################################################################
        self.setEnableBarGraph(True) # Habilita radio exterior
        ################################################################################################
        # FILL POLYGON COLOR BY DEFAULT
        ################################################################################################
        self.setEnableScalePolygon(True) # Tambien radio exterior
        ################################################################################################
        # ENABLE CENTER POINTER BY DEFAULT
        ################################################################################################
        self.enable_CenterPoint = True #Habilita el circulo del centro
        ################################################################################################
        # ENABLE FINE SCALE BY DEFAULT
        ################################################################################################
        self.enable_fine_scaled_marker = True # Habilita las divisiones pequeñas 
        ################################################################################################
        # ENABLE BIG SCALE BY DEFAULT
        ################################################################################################
        self.enable_big_scaled_marker = True # Habilita las divisiones grandes 

        ################################################################################################
        # NEEDLE SCALE FACTOR/LENGTH
        ################################################################################################
        self.needle_scale_factor = 0.8 #Tamaño de la aguja 
        ################################################################################################
        # ENABLE NEEDLE POLYGON BY DEFAULT
        ################################################################################################
        self.enable_Needle_Polygon = True # Habilita la aguja 

        ################################################################################################
        # ENABLE NEEDLE MOUSE TRACKING BY DEFAULT
        ################################################################################################
        # self.setMouseTracking(True)

        ################################################################################################
        # SET GAUGE UNITS
        ################################################################################################
        self.units = ""

        # QTimer sorgt für neu Darstellung alle X ms
        # evtl performance hier verbessern mit self.update() und self.use_timer_event = False
        # todo: self.update als default ohne ueberpruefung, ob self.use_timer_event gesetzt ist oder nicht
        # Timer startet alle 10ms das event paintEvent
        if self.use_timer_event:
            timer = QTimer(self)
            timer.timeout.connect(self.update)
            timer.start(10)
        else:
            self.update()

        ################################################################################################
        # SET DEFAULT THEME
        ################################################################################################
        self.setGaugeTheme(1)

        ################################################################################################
        # RESIZE GAUGE
        ################################################################################################
        self.rescale_method()

    ################################################################################################
    # SET SCALE FONT FAMILY
    ################################################################################################
    def setScaleFontFamily(self, font):
        self.scale_fontname = str(font)

    ################################################################################################
    # SET VALUE FONT FAMILY
    ################################################################################################
    def setValueFontFamily(self, font):
        self.value_fontname = str(font)

    ################################################################################################
    # SET BIG SCALE COLOR
    ################################################################################################
    def setBigScaleColor(self, color):
        self.bigScaleMarker = QColor(color)      

    ################################################################################################
    # SET FINE SCALE COLOR
    ################################################################################################
    def setFineScaleColor(self, color):
        self.fineScaleColor = QColor(color)    

    ################################################################################################
    # GAUGE THEMES
    ################################################################################################
    def setGaugeTheme(self, Theme = 1):
        if Theme == 1:


            self.set_scale_polygon_colors([[.75, QColor(110,110,110,255)]])

            self.needle_center_bg = [
                                    [0, Qt.white], 
                                    ]

            self.bigScaleMarker = Qt.black
            self.fineScaleColor = Qt.black

            self.needle_center_bg = [
                                    [0, QColor(35, 40, 3, 255)], 
                                    [0.16, QColor(30, 36, 45, 255)], 
                                    [0.225, QColor(36, 42, 54, 255)], 
                                    [0.423963, QColor(19, 23, 29, 255)], 
                                    [0.580645, QColor(45, 53, 68, 255)], 
                                    [0.792627, QColor(59, 70, 88, 255)], 
                                    [0.935, QColor(30, 35, 45, 255)], 
                                    [1, QColor(35, 40, 3, 255)]
                                    ]

            self.outer_circle_bg =  [
                                    [0.0645161, QColor(255, 255, 255, 255)], 
                                    [0.37788, QColor(200, 200, 200, 255)], 
                                    [1, QColor(130, 130, 130, 255)]
                                    ]

        
    ################################################################################################
    # SET CUSTOM GAUGE THEME
    ################################################################################################
    def setCustomGaugeTheme(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                            [.5, QColor(str(colors['color2']))],
                                            [.75, QColor(str(colors['color3']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))], 
                                            [0.322581, QColor(str(colors['color1']))], 
                                            [0.571429, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                                            ]

                    self.outer_circle_bg =  [
                                            [0.0645161, QColor(str(colors['color3']))], 
                                            [0.36, QColor(str(colors['color1']))], 
                                            [1, QColor(str(colors['color2']))]
                                            ]

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                             [1, QColor(str(colors['color2']))]])

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))], 
                                            [1, QColor(str(colors['color1']))]
                                            ]

                    self.outer_circle_bg =  [
                                            [0, QColor(str(colors['color2']))], 
                                            [1, QColor(str(colors['color2']))]
                                            ]

            else:

                self.set_scale_polygon_colors([[1, QColor(str(colors['color1']))]])

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                                        ]

                self.outer_circle_bg =  [
                                        [1, QColor(str(colors['color1']))]
                                        ]

        else:
            self.setGaugeTheme(0)
            logInfo(self, "Custom Gauge Theme: color1 is not defined")

    ################################################################################################
    # SET SCALE POLYGON COLOR
    ################################################################################################
    def setScalePolygonColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.set_scale_polygon_colors([[.25, QColor(str(colors['color1']))],
                                            [.5, QColor(str(colors['color2']))],
                                            [.75, QColor(str(colors['color3']))]])

                else:

                    self.set_scale_polygon_colors([[.5, QColor(str(colors['color1']))],
                                             [1, QColor(str(colors['color2']))]])

            else:

                self.set_scale_polygon_colors([[1, QColor(str(colors['color1']))]])

        else:
            logInfo(self, "Custom Gauge Theme: color1 is not defined")

    ################################################################################################
    # SET NEEDLE CENTER COLOR
    ################################################################################################
    def setNeedleCenterColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color3']))], 
                                            [0.322581, QColor(str(colors['color1']))], 
                                            [0.571429, QColor(str(colors['color2']))],
                                            [1, QColor(str(colors['color3']))]
                                            ]

                else:

                    self.needle_center_bg = [
                                            [0, QColor(str(colors['color2']))], 
                                            [1, QColor(str(colors['color1']))]
                                            ]

            else:

                self.needle_center_bg = [
                                        [1, QColor(str(colors['color1']))]
                                        ]
        else:
            logInfo(self, "Custom Gauge Theme: color1 is not defined")

    ################################################################################################
    # SET OUTER CIRCLE COLOR
    ################################################################################################
    def setOuterCircleColor(self, **colors):
        if "color1" in colors and len(str(colors['color1'])) > 0:
            if "color2" in colors and len(str(colors['color2'])) > 0:
                if "color3" in colors and len(str(colors['color3'])) > 0:

                    self.outer_circle_bg =  [
                                            [0.0645161, QColor(str(colors['color3']))], 
                                            [0.37788, QColor(str(colors['color1']))], 
                                            [1, QColor(str(colors['color2']))]
                                            ]

                else:

                    self.outer_circle_bg =  [
                                            [0, QColor(str(colors['color2']))], 
                                            [1, QColor(str(colors['color2']))]
                                            ]

            else:

                self.outer_circle_bg =  [
                                        [1, QColor(str(colors['color1']))]
                                        ]

        else:
            logInfo(self, "Custom Gauge Theme: color1 is not defined")


    ################################################################################################
    # RESCALE
    ################################################################################################
    def rescale_method(self):
        ################################################################################################
        # SET WIDTH AND HEIGHT
        ################################################################################################
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        ################################################################################################
        # SET NEEDLE SIZE
        ################################################################################################
        self.change_value_needle_style([QPolygon([
            QPoint(4, 0),
            QPoint(-4, 0),
            QPoint(-2, - self.widget_diameter / 2 * self.needle_scale_factor),
            QPoint(0, - self.widget_diameter / 2 * self.needle_scale_factor - 6),
            QPoint(2, - self.widget_diameter / 2 * self.needle_scale_factor)
        ])
                                        ,
        QPolygon([
            QPoint(4, 0),
            QPoint(-4, 0),
            QPoint(-2, - self.widget_diameter / 2 * self.needle_scale_factor),
            QPoint(0, - self.widget_diameter / 2 * self.needle_scale_factor - 6),
            QPoint(2, - self.widget_diameter / 2 * self.needle_scale_factor)
        ])
                                        ])

        ################################################################################################
        # SET FONT SIZE
        ################################################################################################
        self.scale_fontsize = self.initial_scale_fontsize * self.widget_diameter / 300
        self.value_fontsize = self.initial_value_fontsize * self.widget_diameter / 300


    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)
        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # UPDATE VALUE
    ################################################################################################
    def updateValue(self, value, mouse_controlled = False):
        # if not mouse_controlled:
        #     self.value = value
        #
        # if mouse_controlled:
        #     self.valueChanged.emit(int(value))

        if value <= self.minValue:
            self.value = self.minValue
        elif value >= self.maxValue:
            self.value = self.maxValue
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def updateAngleOffset(self, offset):
        self.angle_offset = offset
        if not self.use_timer_event:
            self.update()

    def center_horizontal(self, value):
        self.center_horizontal_value = value

    def center_vertical(self, value):
        self.center_vertical_value = value

    ################################################################################################
    # SET NEEDLE COLOR
    ################################################################################################
    def setNeedleColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()
    ################################################################################################
    # SET NEEDLE COLOR ON DRAG
    ################################################################################################
    def setNeedleColorOnDrag(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE VALUE COLOR
    ################################################################################################
    def setScaleValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.ScaleValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET DISPLAY VALUE COLOR
    ################################################################################################
    def setDisplayValueColor(self, R=50, G=50, B=50, Transparency=255):
        # Red: R = 0 - 255
        # Green: G = 0 - 255
        # Blue: B = 0 - 255
        # Transparency = 0 - 255
        self.DisplayValueColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET CENTER POINTER COLOR
    ################################################################################################
    def set_CenterPointColor(self, R=50, G=50, B=50, Transparency=255):
        self.CenterPointColor = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE NEEDLE POLYGON
    ################################################################################################
    def setEnableNeedlePolygon(self, enable = True):
        self.enable_Needle_Polygon = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE SCALE TEXT
    ################################################################################################
    def setEnableScaleText(self, enable = True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE BAR GRAPH
    ################################################################################################
    def setEnableBarGraph(self, enable = True):
        self.enableBarGraph = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE VALUE TEXT
    ################################################################################################
    def setEnableValueText(self, enable = True):
        self.enable_value_text = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE CENTER POINTER
    ################################################################################################
    def setEnableCenterPoint(self, enable = True):
        self.enable_CenterPoint = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE FILLED POLYGON
    ################################################################################################
    def setEnableScalePolygon(self, enable = True):
        self.enable_filled_Polygon = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE BIG SCALE
    ################################################################################################
    def setEnableBigScaleGrid(self, enable = True):
        self.enable_big_scaled_marker = enable

        if not self.use_timer_event:
            self.update()


    ################################################################################################
    # SHOW HIDE FINE SCALE
    ################################################################################################
    def setEnableFineScaleGrid(self, enable = True):
        self.enable_fine_scaled_marker = enable

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SHOW HIDE SCALA MAIN CONT
    ################################################################################################
    def setScalaCount(self, count):
        if count < 1:
            count = 1
        self.scalaCount = count

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET MINIMUM VALUE
    ################################################################################################
    def setMinValue(self, min):
        if self.value < min:
            self.value = min
        if min >= self.maxValue:
            self.minValue = self.maxValue - 1
        else:
            self.minValue = min

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET MAXIMUM VALUE
    ################################################################################################
    def setMaxValue(self, max):
        if self.value > max:
            self.value = max
        if max <= self.minValue:
            self.maxValue = self.minValue + 1
        else:
            self.maxValue = max

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE ANGLE
    ################################################################################################
    def setScaleStartAngle(self, value):
        # Value range in DEG: 0 - 360
        self.scale_angle_start_value = value

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE SIZE
    ################################################################################################
    def setTotalScaleAngleSize(self, value):
        self.scale_angle_size = value

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET GAUGE COLOR OUTER RADIUS
    ################################################################################################
    def setGaugeColorOuterRadiusFactor(self, value):
        self.gauge_color_outer_radius_factor = float(value) / 1000

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET GAUGE COLOR INNER RADIUS
    ################################################################################################
    def setGaugeColorInnerRadiusFactor(self, value):
        self.gauge_color_inner_radius_factor = float(value) / 1000

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # SET SCALE POLYGON COLOR
    ################################################################################################
    def set_scale_polygon_colors(self, color_array):
        if 'list' in str(type(color_array)):
            self.scale_polygon_colors = color_array
        elif color_array == None:
            self.scale_polygon_colors = [[.0, Qt.transparent]]
        else:
            self.scale_polygon_colors = [[.0, Qt.transparent]]

        if not self.use_timer_event:
            self.update()

    ################################################################################################
    # GET MAXIMUM VALUE
    ################################################################################################
    def get_value_max(self):
        return self.maxValue

    ###############################################################################################
    # SCALE PAINTER
    ###############################################################################################

    ################################################################################################
    # CREATE PIE
    ################################################################################################
    def create_polygon_pie(self, outer_radius, inner_raduis, start, lenght, bar_graph = True):
        polygon_pie = QPolygonF()
        # start = self.scale_angle_start_value
        # start = 0
        # lenght = self.scale_angle_size
        # lenght = 180
        # inner_raduis = self.width()/4
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        # todo enable/disable bar graf here
        if not self.enableBarGraph and bar_graph:
            # float_value = ((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue))
            lenght = int(round((lenght / (self.maxValue - self.minValue)) * (self.value - self.minValue)))
            

        # mymax = 0

        for i in range(lenght+1):                                              # add the points of polygon
            t = w * i + start - self.angle_offset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        for i in range(lenght+1):                                              # add the points of polygon
            t = w * (lenght - i) + start - self.angle_offset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygon_pie.append(QPointF(x, y))

        # close outer line
        polygon_pie.append(QPointF(x, y))
        return polygon_pie

    def draw_filled_polygon(self, outline_pen_with=0):
        if not self.scale_polygon_colors == None:
            painter_filled_polygon = QPainter(self)
            painter_filled_polygon.setRenderHint(QPainter.Antialiasing)
            # Koordinatenursprung in die Mitte der Flaeche legen
            painter_filled_polygon.translate(self.width() / 2, self.height() / 2)

            painter_filled_polygon.setPen(Qt.NoPen)

            self.pen.setWidth(outline_pen_with)
            if outline_pen_with > 0:
                painter_filled_polygon.setPen(self.pen)

            colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width() / 2)) * self.gauge_color_outer_radius_factor,
                (((self.widget_diameter / 2) - (self.pen.width() / 2)) * self.gauge_color_inner_radius_factor),
                self.scale_angle_start_value, self.scale_angle_size)

            gauge_rect = QRect(QPoint(0, 0), QSize(self.widget_diameter / 2 - 1, self.widget_diameter - 1))
            grad = QConicalGradient(QPointF(0, 0), - self.scale_angle_size - self.scale_angle_start_value +
                                    self.angle_offset - 1)

            # todo definition scale color as array here
            for eachcolor in self.scale_polygon_colors:
                grad.setColorAt(eachcolor[0], eachcolor[1])
            # grad.setColorAt(.00, Qt.red)
            # grad.setColorAt(.1, Qt.yellow)
            # grad.setColorAt(.15, Qt.green)
            # grad.setColorAt(1, Qt.transparent)
            # self.brush = QBrush(QColor(255, 0, 255, 255))
            # grad.setStyle(Qt.Dense6Pattern)
            # painter_filled_polygon.setBrush(self.brush)
            painter_filled_polygon.setBrush(grad)
           

            painter_filled_polygon.drawPolygon(colored_scale_polygon)
            # return painter_filled_polygon

    def draw_icon_image(self):
        pass

    ###############################################################################################
    # BIG SCALE MARKERS
    ###############################################################################################
    def draw_big_scaled_marker(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        # my_painter.setPen(Qt.NoPen)
        self.pen = QPen(self.bigScaleMarker)
        self.pen.setWidth(2)
        # # if outline_pen_with > 0:
        my_painter.setPen(self.pen)

        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 20)
        for i in range(self.scalaCount+1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter/2 * text_radius_factor

        scale_per_div = int((self.maxValue - self.minValue) / self.scalaCount)

        angle_distance = (float(self.scale_angle_size) / float(self.scalaCount))
        for i in range(self.scalaCount + 1):
            # text = str(int((self.maxValue - self.minValue) / self.scalaCount * i))
            text = str(int(self.minValue + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname, self.scale_fontsize, QFont.Bold))
            angle = angle_distance * i + float(self.scale_angle_start_value - self.angle_offset)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))

            text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
        # painter.restore()

    ################################################################################################
    # FINE SCALE MARKERS
    ################################################################################################
    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(self.fineScaleColor)
        my_painter.rotate(self.scale_angle_start_value - self.angle_offset)
        steps_size = (float(self.scale_angle_size) / float(self.scalaCount * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter/2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 40)
        for i in range((self.scalaCount * self.scala_subdiv_count)+1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    ################################################################################################
    # VALUE TEXT
    ################################################################################################
    def create_values_text(self):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
        except AttributeError:
            try:
                painter.setRenderHint(QPainter.Antialiasing)
            except AttributeError:
                pass

        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, self.value_fontsize, QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(int(self.value))

        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, self.value_fontsize, QFont.Bold))

        angle_end = float(self.scale_angle_start_value + self.scale_angle_size - 360)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])


    ################################################################################################
    # UNITS TEXT
    ################################################################################################
    def create_units_text(self):
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
        except AttributeError:
            try:
                painter.setRenderHint(QPainter.Antialiasing)
            except AttributeError:
                # Neither hint is available; you can handle this case as needed
                pass


        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.DisplayValueColor)
        painter.setPen(pen_shadow)

        text_radius = self.widget_diameter / 2 * self.text_radius_factor

        text = str(self.units)
        w = fm.width(text) + 1
        h = fm.height()
        painter.setFont(QFont(self.value_fontname, int(self.value_fontsize / 2.5), QFont.Bold))

      
        angle_end = float(self.scale_angle_start_value + self.scale_angle_size + 180)
        angle = (angle_end - self.scale_angle_start_value) / 2 + self.scale_angle_start_value

        x = text_radius * math.cos(math.radians(angle))
        y = text_radius * math.sin(math.radians(angle))
        text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
        painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])


    ################################################################################################
    # CENTER POINTER
    ################################################################################################
    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        # painter.setPen(Qt.NoPen)

        # painter.setBrush(self.CenterPointColor)
        # diameter = diameter # self.widget_diameter/6
        # painter.drawEllipse(int(-diameter / 2), int(-diameter / 2), int(diameter), int(diameter))


        # create_polygon_pie(self, outer_radius, inner_raduis, start, lenght)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 12) - (self.pen.width() / 2)),
                0,
                self.scale_angle_start_value, 360, False)

        # 150.0 0.0 131 360

        grad = QConicalGradient(QPointF(0, 0), 0)

        # todo definition scale color as array here
        for eachcolor in self.needle_center_bg:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        # grad.setColorAt(.00, Qt.red)
        # grad.setColorAt(.1, Qt.yellow)
        # grad.setColorAt(.15, Qt.green)
        # grad.setColorAt(1, Qt.transparent)
        painter.setBrush(grad)
        # self.brush = QBrush(QColor(255, 0, 255, 255))
        # painter_filled_polygon.setBrush(self.brush)

        painter.drawPolygon(colored_scale_polygon)
        # return painter_filled_polygon

    ################################################################################################
    # CREATE OUTER COVER
    ################################################################################################
    def draw_outer_circle(self, diameter=30):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        colored_scale_polygon = self.create_polygon_pie(
                ((self.widget_diameter / 2) - (self.pen.width())), # Radio exterior del ciculo
                (0), # Radio interior del círculo
                self.scale_angle_start_value / 10,
                360, False)

        radialGradient = QRadialGradient(QPointF(0, 0), self.width())

        for eachcolor in self.outer_circle_bg:
            radialGradient.setColorAt(eachcolor[0], eachcolor[1])


        painter.setBrush(radialGradient)

        painter.drawPolygon(colored_scale_polygon)


    ################################################################################################
    # NEEDLE POINTER
    ################################################################################################
    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])
        # Koordinatenursprung in die Mitte der Flaeche legen

    def draw_needle_2(self): 
    #     
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 54, 255, 255))
        painter.rotate(((self.value - self.value_offset - self.minValue) * self.scale_angle_size /
                        (self.maxValue - self.minValue)) - 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # EVENTS
    ###############################################################################################

    ################################################################################################
    # ON WINDOW RESIZE
    ################################################################################################
    def resizeEvent(self, event):
        # self.resized.emit()
        # return super(self.parent, self).resizeEvent(event)
        self.rescale_method()
        # self.emit(QtCore.SIGNAL("resize()"))

    ################################################################################################
    # ON PAINT EVENT
    ################################################################################################
    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html

        self.draw_outer_circle()
        self.draw_icon_image()
        # colored pie area
        if self.enable_filled_Polygon:
            self.draw_filled_polygon()

        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_marker()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # Display Value
        if self.enable_value_text:
            self.create_values_text()
            self.create_units_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()
            self.draw_needle_2()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(diameter=(self.widget_diameter / 6))


#################################################################################################
# END ==>
################################################################################################
