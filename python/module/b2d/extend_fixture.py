from ._b2d import *
from .tools import _classExtender


def report_filter(**kwargs):
    f = ReportFilter()
    for k, v in kwargs.items():
        setattr(f, k, v)
    return f


def filter(**kwargs):
    f = Filter()
    for k, v in kwargs.items():
        setattr(f, k, v)
    return f


def fixture_def(
    shape=None,
    friction=None,
    restitution=None,
    density=None,
    is_sensor=None,
    shape_filter=None,
    user_data=None,
    group_index=None,
):
    fd = FixtureDef()
    if shape is not None:
        fd.shape = shape
    if friction is not None:
        fd.friction = friction
    if restitution is not None:
        fd.restitution = restitution
    if density is not None:
        fd.density = density
    if is_sensor is not None:
        fd.is_sensor = is_sensor

    if group_index is not None:
        if shape_filter is None:
            shape_filter = b2Filter()
        shape_filter.group_index = int(group_index)

    if shape_filter is not None:
        fd.filter = shape_filter

    if user_data is not None:
        fd.user_data = user_data
    return fd


class _FixtureDef(FixtureDef):
    @property
    def user_data(self):
        if self._has_user_data():
            return self._get_user_data()
        else:
            return None

    @user_data.setter
    def user_data(self, ud):
        if self._has_user_data():
            return self._delete_user_data()
        self._set_user_data(ud)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._set_shape(shape)


_classExtender(_FixtureDef, ["user_data", "shape"])


class _Fixture(Fixture):
    @property
    def user_data(self):
        if self._has_user_data():
            return self._get_user_data()
        else:
            return None

    @user_data.setter
    def user_data(self, ud):
        if self._has_user_data():
            return self._delete_user_data()
        self._set_user_data(ud)

    @property
    def next(self):
        if self._has_next():
            return self._get_next()
        else:
            return None


_classExtender(_Fixture, ["user_data", "next"])
