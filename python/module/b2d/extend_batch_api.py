from ._b2d import _BodyVector

import numpy


def _2d_out(n, out, dtype):
    if out is None:
        out = numpy.zeros([n, 2], dtype=dtype)
        return out
    else:
        if out.ndim != 2:
            raise RuntimeError("out needs to be 2D ndarray")
        if out.shape[1] != 2:
            raise RuntimeError("out shape  needs to be [n,2]")
        if out.shape[0] < n:
            out = numpy.zeros([n, 2], dtype=dtype)

        out = numpy.require(out, dtype=dtype, requirements=["C"])
        return out[:n, :]


def _1d_out(n, out, dtype):
    if out is None:
        out = numpy.zeros([n], dtype=dtype)
        return out
    else:
        if out.ndim != 1:
            raise RuntimeError("out needs to be 1D ndarray")
        if out.shape[0] < n:
            out = numpy.zeros([n], dtype=dtype)

        out = numpy.require(out, dtype=dtype, requirements=["C"])
        return out[:n]


class BodyVector(_BodyVector):
    def __init__(self):
        super(BodyVector, self).__init__()

    def position(self, out=None):
        return self._position(out=_2d_out(n=len(self), out=out, dtype="float32"))

    def world_center(self, out=None):
        return self._world_center(out=_2d_out(n=len(self), out=out, dtype="float32"))

    def local_center(self, out=None):
        return self._local_center(out=_2d_out(n=len(self), out=out, dtype="float32"))

    def linear_velocity(self, out=None):
        return self._linear_velocity(out=_2d_out(n=len(self), out=out, dtype="float32"))

    def angle(self, out=None):
        return self._angle(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def angular_velocity(self, out=None):
        return self._angular_velocity(
            out=_1d_out(n=len(self), out=out, dtype="float32")
        )

    def mass(self, out=None):
        return self._mass(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def inertia(self, out=None):
        return self._inertia(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def linear_damping(self, out=None):
        return self._linear_damping(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def angular_damping(self, out=None):
        return self._angular_damping(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def bullet(self, out=None):
        return self._bullet(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def sleeping_allowed(self, out=None):
        return self._sleeping_allowed(
            out=_1d_out(n=len(self), out=out, dtype="float32")
        )

    def awake(self, out=None):
        return self._awake(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def angular_damping(self, out=None):
        return self._angular_damping(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def enabled(self, out=None):
        return self._enabled(out=_1d_out(n=len(self), out=out, dtype="float32"))

    def fixed_rotation(self, out=None):
        return self._fixed_rotation(out=_1d_out(n=len(self), out=out, dtype="float32"))
