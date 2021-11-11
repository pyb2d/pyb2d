import PyQt5
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import pybox2d
import logging
from pybox2d import JointType

import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

from . tools import *
from . recording_renderer import *
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def same_point(a,b):
    a = pg.Point(a)
    b = pg.Point(b)
    return isclose(a.x(), b.x()) and isclose(a.y(), b.y())
        

class PgDebugDraw(pybox2d.DebugDraw):
    def __init__(self, canvas):
        super(PgDebugDraw,self).__init__(float_colors=False)

        self.canvas = canvas
        self.framework_settings = self.canvas.framework_settings
        self.painter = None
        self.option = None
        self.widget = None

        #self.ppm = ppm
        #self.ippm = 1.0 / self.ppm
        self.outline_width = 0.01
        self.segment_width = 0.01
        self._bounding_box = [ [0,0],[0,0]]

        self.joint_colors = {
            JointType.unknown_joint :   (230, 25, 75),
            JointType.revolute_joint :  (255,0, 0),
            JointType.prismatic_joint : (255, 225, 25),
            JointType.distance_joint :  (0, 130, 200),
            JointType.pulley_joint :    (245, 130, 48),
            JointType.mouse_joint :     (145, 30, 180),
            JointType.gear_joint :      (70, 240, 240),
            JointType.wheel_joint :     (240, 50, 230),
            JointType.weld_joint :      (210, 245, 60),
            JointType.friction_joint :  (250, 190, 190),
            # JointType.rope_joint :      (0, 128, 128),
            JointType.motor_joint :     (230, 190, 255),
        }

    def set_painter(self, painter, option, widget):
        self.painter = painter
        self.option = option
        self.widget = widget

    def reset_bounding_box(self):
        self._bounding_box = [ [0,0],[0,0]]

    def _update_bounding_box(self, p):
        for c in range(2):
            if p[c] < self._bounding_box[0][c]:
                self._bounding_box[0][c] = p[c]

            if p[c] > self._bounding_box[1][c]:
                self._bounding_box[1][c] = p[c]

    def draw_solid_circle(self, center, radius, axis, color):


        painter  = self.painter
        with SaveRestore(painter):
            
            p = QtCore.QPointF(center[0],center[1])


         
            with SaveRestore(painter):
                brush_color = QtGui.QColor(*color)
                pen = QtGui.QPen(brush_color, self.outline_width, QtCore.Qt.SolidLine)
                painter.setBrush(QtGui.QBrush(brush_color))
                painter.setPen(pen)
                painter.drawEllipse(p, radius, radius)

            # with SaveRestore(painter):
            #     axis_color = QtGui.QColor(*[30.0 * c for c in color])
            #     pen = QtGui.QPen(axis_color, self.outline_width, QtCore.Qt.SolidLine)
            #     painter.setPen(pen)
            #     raxis = [float(radius)*float(a) for a in axis]
            #     painter.drawLine(    pg.Point(center), 
            #                          pg.Point(center[0] + raxis[0], center[1] +raxis[1]))
                
    def draw_circle(self, center, radius, color):


        color = QtGui.QColor(*color)

        p = QtCore.QPointF(*center)
        pen = QtGui.QPen(color, self.outline_width, QtCore.Qt.SolidLine)
        with SaveRestore(self.painter):
            self.painter.setPen(pen)
            self.painter.drawEllipse(p, radius, radius)

    def draw_segment(self,v1, v2, color):


        color = QtGui.QColor(*color)
        pen = QtGui.QPen(color, self.outline_width)
        if True:#not same_point(v1,v2):
            with SaveRestore(self.painter):
                self.painter.setPen(pen)
                qline = QtCore.QLineF(pg.Point(v1), pg.Point(v2))
                #print(v1, v2, qline)
                self.painter.drawLine(qline)
            
    def draw_polygon(self,vertices, color):


        color = QtGui.QColor(*color)
        pen = QtGui.QPen(color, self.outline_width)#, QtCore.Qt.SolidLine)
        with SaveRestore(self.painter):
            self.painter.setPen(pen)
            self.painter.drawConvexPolygon(numpy_to_qpoly(vertices))

    def draw_solid_polygon(self,vertices, color):

        brush_color = QtGui.QColor(*color)
        pen_color = brush_color

        pen = QtGui.QPen(pen_color, self.outline_width)#, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(brush_color)
        with SaveRestore(self.painter):
            self.painter.setBrush(brush)
            self.painter.setPen(pen)
            self.painter.drawConvexPolygon(numpy_to_qpoly(vertices))

    def draw_particles(self, centers, radius, colors=None):
        #print("draw")
        painter = self.painter
        if True:#colors is None or not self.framework_settings.draw_colored_particles:
            color = (1,0,0)
            brush_color = QtGui.QColor(*[255.0 * c for c in color])
            pen_color = brush_color
            pen = QtGui.QPen(pen_color, radius, QtCore.Qt.SolidLine)
            brush = QtGui.QBrush(brush_color)


            with SaveRestore(painter):
                #pen.setCapStyle(QtCore.Qt.RoundCap);
                painter.setBrush(QtGui.QBrush(brush_color))
                painter.setPen(pen)
                #print(centers)
                painter.drawPoints(numpy_to_qpoly(centers))
        else:
            with SaveRestore(painter):
                for center,color in zip(centers,colors):

                    pen_color = QtGui.QColor(color)
                    pen = QtGui.QPen(pen_color, radius, QtCore.Qt.SolidLine)
                    painter.setPen(pen)
                    
                    painter.drawPoints(numpy_to_qpoly(centers))

    def draw_joint(self, joint):
        
        anchor_a = joint.anchor_a
        anchor_b = joint.anchor_b
        joint_color = self.joint_colors[joint.type]

        color = QtGui.QColor(*joint_color)
        pen = QtGui.QPen(color, self.outline_width*3, QtCore.Qt.SolidLine)
        with SaveRestore(self.painter):
            self.painter.setPen(pen)
            if not same_point(anchor_a, anchor_b):
                self.painter.drawLine(pg.Point(anchor_a), pg.Point(anchor_b))

        anchor_rad =  self.outline_width * 5
        pen = QtGui.QPen(color, self.outline_width, QtCore.Qt.SolidLine)

        self._update_bounding_box([c + anchor_rad for c in anchor_a])
        self._update_bounding_box([c - anchor_rad for c in anchor_b])

        with SaveRestore(self.painter):
            self.painter.setPen(pen)
            self.painter.drawEllipse(pg.Point(anchor_a), anchor_rad, anchor_rad)
            self.painter.drawEllipse(pg.Point(anchor_b), anchor_rad, anchor_rad)

class PgBatchDebugDraw(pybox2d.BatchDebugDraw):
    def __init__(self, debug_draw_graphics_object):
        super(PgBatchDebugDraw, self).__init__()

        self.debug_draw_graphics_object = debug_draw_graphics_object
        self.painter = None
        self.paint_option = None
        self.widget = None

        #self.ppm = ppm
        #self.ippm = 1.0 / self.ppm
        self.outline_width = 0.01
        self.segment_width = 0.01     

    def set_painter(self, painter, option, widget):
        self.painter = painter
        self.paint_option = option
        self.widget = widget

    def drawing_aabb(self, aabb):
        #print("aabb",aabb)
        lower_bound = aabb.lower_bound
        upper_bound = aabb.upper_bound
        shape = upper_bound - lower_bound 
        
        # enlarge bb
        extended_lower_bound = lower_bound - shape/2.0
        extended_upper_bound = lower_bound + shape/2.0
        extended_shape = extended_upper_bound - extended_lower_bound 
        rect = QtCore.QRectF(pg.Point(extended_lower_bound), pg.Point(extended_shape))
        self.debug_draw_graphics_object._bounding_rect = rect

    def draw_solid_polygons(self, points, connect, color):
        if points.size > 0:
            path = QtGui.QPainterPath()
            path.moveTo(pg.Point(points[0,:]))
            path2 = pg.arrayToQPath(x=points[:,0], y=points[:,1], connect=connect)
            path.addPath(path2)
            painter = self.painter
            with SaveRestore(painter):
                path.setFillRule(QtCore.Qt.WindingFill)
                brush_color = QtGui.QColor(*[255.0 * c for c in color])
                pen_color = QtGui.QColor(*[100.0 * c for c in color])
                pen = QtGui.QPen(pen_color, self.outline_width)#, QtCore.Qt.SolidLine)
                brush = QtGui.QBrush(brush_color)
                painter.setPen(pen)
                painter.setBrush(brush)
                path.moveTo(0,0)
                painter.drawPath(path)

    def draw_polygons(self, points, connect, color):
        path = pg.arrayToQPath(x=points[:,0], y=points[:,1], connect=connect)
        painter = self.painter
        with SaveRestore(painter):
            pen_color = QtGui.QColor(*[255.0 * c for c in color])
            pen = QtGui.QPen(pen_color, self.outline_width)#, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            path.moveTo(0,0)
            #painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawPath(path)


    def draw_segments(self, points, connect, color):
        path = pg.arrayToQPath(x=points[:,0], y=points[:,1], connect=connect)
        painter = self.painter
        with SaveRestore(painter):
            pen_color = QtGui.QColor(*[255.0 * c for c in color])
            pen = QtGui.QPen(pen_color, self.outline_width)#, QtCore.Qt.SolidLine)
            painter.setPen(pen)
            #painter.setBrush(pen_color)
            painter.drawPath(path)

    def draw_particles(self, centers, radius, colors=None):
        #print("draw parts")
        painter = self.painter
        if True:#colors is None or not self.framework_settings.draw_colored_particles:
            color = (1,0,0)
            brush_color = QtGui.QColor(*[255.0 * c for c in color])
            pen_color = brush_color
            pen = QtGui.QPen(pen_color, radius, QtCore.Qt.SolidLine)
            brush = QtGui.QBrush(brush_color)


            with SaveRestore(painter):
                #pen.setCapStyle(QtCore.Qt.RoundCap);
                painter.setBrush(QtGui.QBrush(brush_color))
                painter.setPen(pen)
                #print(centers)
                painter.drawPoints(numpy_to_qpoly(centers))
        else:
            with SaveRestore(painter):
                for center,color in zip(centers,colors):

                    pen_color = QtGui.QColor(color)
                    pen = QtGui.QPen(pen_color, radius, QtCore.Qt.SolidLine)
                    painter.setPen(pen)
                    
                    painter.drawPoints(numpy_to_qpoly(centers))

    def draw_circles(self, centers, radii, color):
        pass

class DebugDrawGraphicsObject(pg.GraphicsObject):
    def __init__(self, parent = None):
        pg.GraphicsObject.__init__(self,parent)
        self.framework = None
        self.world = None
        self.framework_settings = None
        
        # debug draw
        self.debug_draw = PgDebugDraw(self)
       

        # batch debug draw
        self.batch_debug_draw = PgBatchDebugDraw(self)


        # RECORDING RENDERER
        self.recording_renderer = RecordingRenderer()

        self._build_param()
    
        self.not_run = True
        self._bounding_rect = None
        self._supress_events = False

    def set_example(self, example):

        self.framework = example
        self.world = self.framework.world
        self.framework_settings = self.framework.framework_settings

        self.world.set_batch_debug_draw(self.batch_debug_draw)
        #self.world.set_debug_draw(self.debug_draw)

        # init shape bits
        self._supress_events = True
        self._init_param_values()
        self._supress_events = False
        self.on_debug_draw_bits_changed()

        self.not_run = True
        self._bounding_rect = None

        flags = ['particle']
        self.debug_draw.append_flags(flags)


    def _init_param_values(self):

        assert self.framework is not None, "framework is None (maybe missing set_example?)"
        fms = self.framework_settings
        batch_draw_debug_data_opts = self.batch_debug_draw.options
        draw_bit_param = self.parameter.param('draw_bits')
        draw_bit_param.param('draw shapes').setValue(fms.draw_shapes)
        draw_bit_param.param('draw joints').setValue( fms.draw_joints)
        draw_bit_param.param('draw aabb').setValue(fms.draw_aabbs)
        draw_bit_param.param('draw pairs').setValue(fms.draw_pairs)
        draw_bit_param.param('draw center of mass').setValue(fms.draw_coms)
        #draw_bit_param.param('draw particle').setValue(fms.draw_particles)

        batch_draw_debug_data_opts.draw_shapes = fms.draw_shapes
        batch_draw_debug_data_opts.draw_joints = fms.draw_joints
        batch_draw_debug_data_opts.draw_aabbs = fms.draw_aabbs
        batch_draw_debug_data_opts.draw_coms = fms.draw_coms
        #batch_draw_debug_data_opts.draw_particles = fms.draw_particles

    def _build_param(self):
        #fms = self.framework_settings
        #batch_draw_debug_data_opts = self.batch_debug_draw.options
        params = [
            {'name': 'draw_bits', 'type': 'group', 'children': 
                [
                    {'name': 'draw shapes', 'type': 'bool', 'value': False},
                    {'name': 'draw joints', 'type': 'bool', 'value': False},
                    {'name': 'draw aabb', 'type': 'bool', 'value': False},
                    {'name': 'draw pairs', 'type': 'bool', 'value': False},
                    {'name': 'draw center of mass', 'type': 'bool', 'value': False},
                    {'name': 'draw particle', 'type': 'bool', 'value': False},
                ]
            },
            {'name': 'particles', 'type': 'group', 'children': 
                [
                    {'name': 'colored', 'type': 'bool', 'value': False},
                ]
            }
        ]

        # batch_draw_debug_data_opts.draw_shapes = fms.draw_shapes
        # batch_draw_debug_data_opts.draw_joints = fms.draw_joints
        # batch_draw_debug_data_opts.draw_aabbs = fms.draw_aabbs
        # batch_draw_debug_data_opts.draw_coms = fms.draw_coms

        self.parameter =  Parameter.create(name='Debug Draw', type='group', children=params)
        draw_bit_param = self.parameter.param('draw_bits')
        for child in draw_bit_param.children():
            child.sigValueChanged.connect(self.on_debug_draw_bits_changed)

    def on_debug_draw_bits_changed(self):
        if not self._supress_events:
            fms = self.framework_settings
            batch_draw_debug_data_opts = self.batch_debug_draw.options
            draw_bit_param = self.parameter.param('draw_bits')
            self.debug_draw.clear_flags(['shape','joint','aabb','pair','center_of_mass','particle'])

            flags = []

            
            fms.draw_shapes = draw_bit_param.param('draw shapes').value()
            fms.draw_joints = draw_bit_param.param('draw joints').value()
            fms.draw_aabbs = draw_bit_param.param('draw aabb').value()
            fms.draw_pairs = draw_bit_param.param('draw pairs').value()
            fms.draw_coms = draw_bit_param.param('draw center of mass').value()
            fms.draw_particles = draw_bit_param.param('draw particle').value()


            batch_draw_debug_data_opts.draw_shapes = fms.draw_shapes
            batch_draw_debug_data_opts.draw_joints = fms.draw_joints
            batch_draw_debug_data_opts.draw_aabbs = fms.draw_aabbs
            batch_draw_debug_data_opts.draw_coms = fms.draw_coms
            #batch_draw_debug_data_opts.draw_particles = fms.draw_particles
            #if(draw_bit_param.param('draw shapes').value()):
            #    flags.append('shape')
            #if(draw_bit_param.param('draw joints').value()):
            #    flags.append('joint')
            #if(draw_bit_param.param('draw aabb').value()):
            #    flags.append('aabb')
            #if(draw_bit_param.param('draw pairs').value()):
            #    flags.append('pair')
            #if(draw_bit_param.param('draw center of mass').value()):
            #    flags.append('center_of_mass')
            if(draw_bit_param.param('draw particle').value()):
                flags.append('particle')

            self.debug_draw.append_flags(flags)

    def physics_to_canvas(self, p):
        return (p[0], p[1])
    def canvas_to_physics(self, p):
        return (p[0], p[1])

    def paint_from_recording_renderer(self, painter, option, widget):
        rec = self.recording_renderer.recordings
        for center, radius, axis, c in rec['solid_circle']:
            self.debug_draw.draw_segment(center, radius, axis, c)
        for center, radius, c in rec['circle']:
            self.debug_draw.draw_segment(center, radius, c)
        for v1, v2, c in rec['segment']:
            self.debug_draw.draw_segment(v1, v2, c)

        self.recording_renderer.reset_recordings()





    def paint(self, painter, option, widget):
        current_pixel_size = self.pixelSize()
        p = 0.5 * current_pixel_size[0]  +  0.5 * current_pixel_size[1]

        self.debug_draw.outline_width = (p) * 1.0
        self.debug_draw.segment_width = (p) * 1.0
        self.batch_debug_draw.outline_width = (p) * 1.0
        self.batch_debug_draw.segment_width = (p) * 1.0


        with SaveRestore(painter):
            self.debug_draw.set_painter(painter, option, widget)
            self.batch_debug_draw.set_painter(painter, option, widget)

            self.debug_draw.reset_bounding_box()
            self.world.draw_debug_data()
            self.world.batch_draw_debug_data()
            self.not_run = False

            self.paint_from_recording_renderer(painter, option, widget)

    def boundingRect(self):
        if self._bounding_rect is None:
            return QtCore.QRectF()
        else:
            return self._bounding_rect
