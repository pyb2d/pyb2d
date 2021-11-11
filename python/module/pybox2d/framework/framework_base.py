import pybox2d as b2d
from pybox2d import vec2
import time
import logging
# logging.warning('Watch out!')  # will print a message to the console
# logging.info('I told you so')  # will not print anything

from . framework_settings import *




class AABBCallback(b2d.QueryCallback):
    def __init__(self, testPoint):
        super(AABBCallback,self).__init__()

        self.testPoint = vec2(testPoint)
        self.fixture  = None

    def report_fixture(self, fixture):
        if fixture.test_point(self.testPoint):
            self.fixture  =fixture
            return False
        else:
            return True




class FrameworkBase(
    b2d.DestructionListener,
    b2d.ContactListener
    
):

    def __init__(self,gui=None,gravity=vec2(0,-9.81)):
        b2d.ContactListener.__init__(self)
        b2d.DestructionListener.__init__(self)
        self.gui = gui


        # Box2D-related
        self.points = []
        self.world = None
        self.bomb = None
        self.mouse_joint = None
        self.framework_settings = FrameworkSettings
        self.step_count = 0
        self.is_paused = False
        self.__time_last_step = None
        self.current_fps = 0.0

        self.canvas = None
        self.world = b2d.world(gravity)
        self.groundbody = self.world.create_body()
        
        #self.world.set_contact_listener(self)
        self.world.set_destruction_listener(self)


    def is_key_down(self, key):
        return self.gui.is_key_down(key)
    
        
    # def __reset(self):
    #     """ Reset all of the variables to their starting values.
    #     Not to be called except at initialization."""
    #     # Box2D-related
    #     self.points = []
    #     self.world = None
    #     self.bomb = None
    #     self.mouse_joint = None
    #     self.framework_settings = FrameworkSettings

       
    #     self.step_count = 0
    #     self.is_paused = False
    #     self.__time_last_step = None
    #     self.current_fps = 0.0
        
    def step(self, dt):
        
        self.world.step(dt, 5, 5)
        if self.__time_last_step is None:
            self.__time_last_step  = time.time()
        else:
            t_now = time.time()
            dt = t_now - self.__time_last_step 
            self.__time_last_step = t_now
            self.current_fps = 1.0/dt
        self.step_count += 1

    def pre_step(self, dt):
        pass

    def post_step(self, dt):
        pass
            

    def get_particle_parameter_value(self):
        return 0



    def on_mouse_move(self, p):
        """
        Mouse moved to point p, in world coordinates.
        """
        if self.mouse_joint is not None:
            self.mouse_joint.target = p
            return True
        else:
            return False

    def on_mouse_down(self, p):
        """
        Indicates that there was a left click at point p (world coordinates)
        """

       
        if self.mouse_joint is not None:
            self.world.destroy_joint(self.mouse_joint)
            self.mouse_joint = None
            return False
        else:
            pass
        body = self.world.find_body(pos=p)
        if body is not None:    
            
            self.mouse_joint = self.world.create_mouse_joint(
                body_a=self.groundbody,
                body_b=body,
                target=p,
                damping=20.0,
                max_force=10000.0 * body.mass)
            self.mouse_joint.user_data = "helloj"
            body.awake = True

        return body is not None

    def on_mouse_up(self, p):
        """
        Left mouse button up.
        """
        print("on_mouse_up")

        if self.mouse_joint is not None:
            print("pls destroy_joint from up")
            self.world.destroy_joint(self.mouse_joint)
            self.mouse_joint = None
            return True
        else:
            return False

    def on_key_down(self, key):
        return False

    def on_key_up(self, key):
        return False

    # ContactListener
    def begin_contact(self, contact):
        print("begin_contact")

    def end_contact(self, contact):
        print("end_contact")

    def begin_contact_particle_body(self, particleSystem, particleBodyContact):
        print("begin_contact_particle_body")

    def begin_contact_particle(self, particleSystem, indexA, indexB):
        print("end_contact")

    def end_contact_particle(self, particleSystem, indexA, indexB):
        pass

    def pre_solve(self, contact, oldManifold):
        pass

    def post_solve(self, contact, impulse):
        pass


    # DestructionListener
    def say_goodbye_joint(self, joint):
        print("destroy",joint)
    def say_goodbye_fixture(self, fixture):
        pass
    def say_goodbye_particle_group(self, particleGroup):
        pass
    def say_goodbye_particle_system(self, particleSystem,index):
        pass




