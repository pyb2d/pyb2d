from ._b2d import *
from .extend_math import vec2
from .tools import _classExtender, GenericB2dIter
from . extend_user_data import add_user_data_api
from . _make_local_anchor_ab import _make_local_anchor_ab
from enum import Enum


add_user_data_api(JointDef)
add_user_data_api(Joint)



from functools import wraps


def __joint_def(joint_def_cls, jtype, body_a,body_b,**kwargs):
    jd = kwargs.get("joint_def", joint_def_cls())
    jd.jtype = jtype
    jd.body_a = body_a
    jd.body_b = body_b
    for key,value in kwargs.items():
        setattr(jd, key, value)
    return jd

def __setup_anchers(jd, **kwargs):

    local_anchor_a, local_anchor_b = _make_local_anchor_ab(**kwargs)
    jd.local_anchor_a = local_anchor_a
    jd.local_anchor_b = local_anchor_b
    return local_anchor_a, local_anchor_b


def distance_joint_def(body_a,body_b,
                    local_anchor_a = None,
                    local_anchor_b = None,
                    local_anchor= None,
                    anchor_a = None,
                    anchor_b = None,
                    anchor= None,
                    collide_connected=False,
                    length=None, 
                    stiffness=0.0,
                    damping=0.0,
                    user_data=None,
                    int_user_data=None,
                    joint_def=None):
    if joint_def is None:
        jd = DistanceJointDef()
    else:
        jd = joint_def
    jd.jtype = JointType.distance_joint
    jd.body_a = body_a
    jd.body_b = body_b
    local_anchor_a, local_anchor_b = _make_local_anchor_ab(body_a, body_b, 
            local_anchor_a, local_anchor_b, local_anchor,
            anchor_a, anchor_b, anchor)
    jd.local_anchor_a = local_anchor_a
    jd.local_anchor_b = local_anchor_b
    jd.collide_connected = collide_connected 
    if length is None:
        anchor_a = body_a.get_world_point(local_anchor_a)
        anchor_b = body_b.get_world_point(local_anchor_b)
        length = (anchor_a - anchor_b).length
    jd.length = length
    jd.stiffness = stiffness
    jd.damping = damping
    if user_data is not None:
        jd.user_data = user_data
    if int_user_data is not None:
        jd.int_user_data = int(int_user_data)
    return jd





def mouse_joint_def(body_a,body_b,collide_connected=False,target=vec2(0,0),
                    max_force=0.0, stiffness=200.0, damping=0.0):
    jd = MouseJointDef()
    jd.jtype = JointType.mouse_joint
    jd.body_a = body_a
    jd.body_b = body_b
    jd.collide_connected = collide_connected 
    jd.target = target
    jd.max_force = max_force

    #stiffness, damping  = linear_stiffness(frequency_hz, damping_ratio, body_a, body_a)
    jd.stiffness = stiffness
    jd.damping = damping
    return jd

def mouse_joint_def(**kwargs):
    jd = MouseJointDef()
    jd.jtype = JointType.mouse_joint
    for k,v in kwargs.items():
        setattr(jd, k, v)
    # jd.body_a = body_a
    # jd.body_b = body_b
    # jd.collide_connected = collide_connected 
    # jd.target = target
    # jd.max_force = max_force

    # #stiffness, damping  = linear_stiffness(frequency_hz, damping_ratio, body_a, body_a)
    # jd.stiffness = stiffness
    # jd.damping = damping
    return jd


def joint_def(jtype,body_a,body_b,collide_connected=False):
    jd = JointDef()
    jd.jtype = jtype
    jd.body_a = body_a
    jd.body_b = body_b
    jd.collide_connected = collide_connected 
    return jd


def wheel_joint_def(body_a,body_b,
                    local_anchor_a = None,
                    local_anchor_b = None,
                    local_anchor= None,
                    anchor_a = None,
                    anchor_b = None,
                    anchor = None,
                    local_axis_a = None,
                    enable_motor = None,
                    max_motor_torque = None,
                    motor_speed=None,
                    stiffness=None,
                    damping=None,
                    user_data=None,
                    int_user_data=None,
                    joint_def=None):
    if joint_def is None:
        jd = WheelJointDef()
    else:
        jd = joint_def
    jd.jtype = JointType.wheel_joint
    jd.body_a = body_a
    jd.body_b = body_b
    local_anchor_a, local_anchor_b = _make_local_anchor_ab(body_a, body_b, 
            local_anchor_a, local_anchor_b, local_anchor,
            anchor_a, anchor_b, anchor)
    jd.local_anchor_a = local_anchor_a
    jd.local_anchor_b = local_anchor_b
 
    if local_axis_a is not None:
        jd.local_axis_a = vec2(local_axis_a)
    if enable_motor is not None:
        jd.enable_motor = enable_motor
    if max_motor_torque is not None:
        jd.max_motor_torque = max_motor_torque
    if motor_speed is not None:
        jd.motor_speed = motor_speed
    if stiffness is not None:
        jd.stiffness = stiffness
    if damping is not None:
        jd.damping = damping
    if joint_def is not None:
        jd.joint_def = joint_def


    if user_data is not None:
        jd.user_data = user_data
    if int_user_data is not None:
        jd.int_user_data = int(int_user_data)
    return jd


def rope_joint_def(body_a,body_b,
                 local_anchor_a = (0,0),
                 local_anchor_b = (0,0),
                 maxLength = 0.0,
                 collide_connected=False
):
    jd = RopeJointDef()
    #jd.jtype = JointType.mouseJoint
    jd.body_a = body_a
    jd.body_b = body_b
    jd.collide_connected = collide_connected 
    jd.local_anchor_a = vec2(local_anchor_a)
    jd.local_anchor_b = vec2(local_anchor_b)
    jd.maxLength = maxLength
    return jd

def revolute_joint_def(body_a,body_b,
                    local_anchor_a = None,
                    local_anchor_b = None,
                    local_anchor= None,
                    anchor_a = None,
                    anchor_b = None,
                    anchor= None,
                    reference_angle = 0.0,
                    lower_angle = 0.0,
                    upper_angle = 0.0,
                    max_motor_torque = 0.0,
                    motor_speed = 0.0,
                    enable_limit = False,
                    enable_motor = False,
                    collide_connected=False
):
    jd = RevoluteJointDef()
    #jd.jtype = JointType.mouseJoint
    jd.body_a = body_a
    jd.body_b = body_b
    jd.collide_connected = collide_connected 
    local_anchor_a, local_anchor_b = _make_local_anchor_ab(body_a, body_b, 
            local_anchor_a, local_anchor_b, local_anchor,
            anchor_a, anchor_b, anchor)
    jd.local_anchor_a = local_anchor_a
    jd.local_anchor_b = local_anchor_b
    jd.reference_angle = reference_angle
    jd.lower_angle = lower_angle
    jd.max_motor_torque = max_motor_torque
    jd.upper_angle = upper_angle
    jd.motor_speed = motor_speed
    jd.enable_limit = enable_limit
    jd.enable_motor = enable_motor
    return jd

def prismatic_joint_def(body_a,body_b,
                    local_anchor_a = (0,0),
                    local_anchor_b = (0,0),
                    local_axis_a = (1,0),
                    reference_angle = 0.0,
                    enable_limit = False,
                    lower_translation = 0.0,
                    upper_translation = 0.0,
                    enable_motor = False,
                    max_motor_force = 0.0,
                    motor_speed = 0.0,
                    collide_connected=False
):
    jd = PrismaticJointDef()
    #jd.jtype = JointType.mouseJoint
    jd.body_a = body_a
    jd.body_b = body_b
    jd.collide_connected = collide_connected 

    # 
    jd.local_anchor_a = vec2(local_anchor_a)
    jd.local_anchor_b = vec2(local_anchor_b)
    jd.local_axis_a = vec2(local_axis_a)
    jd.reference_angle = reference_angle
    jd.enable_limit = enable_limit
    jd.lower_translation = lower_translation
    jd.upper_translation = upper_translation
    jd.enable_motor = enable_motor
    jd.max_motor_force = max_motor_force
    jd.motor_speed = motor_speed
    return jd



class _Joint(Joint):
    @property
    def next(self):
        if self._has_next():
            return self._get_next()
        else:
            return None


_classExtender(_Joint,['next'])


