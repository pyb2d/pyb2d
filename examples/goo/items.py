
class ObjectBase(object):
    pass

class Destroyer(ObjectBase):
    def __init__(self, body):
        self.body = body

class Goal(ObjectBase):
    def __init__(self, body):
        self.body = body
