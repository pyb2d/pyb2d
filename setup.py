import sys
import glob
import os
from pathlib import Path

from pybind11 import get_cmake_dir, get_include

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_packages

__version__ = "0.7.2"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

liquidfun = True

binding_sources = [
    "python/src/main.cpp",
    "python/src/def_build_config.cpp",
    "python/src/b2Body.cxx",
    "python/src/b2Collision.cxx",
    "python/src/b2Contact.cxx",
    "python/src/b2Draw.cxx",
    "python/src/b2Fixture.cxx",
    "python/src/b2Joint.cxx",
    "python/src/b2JointDef.cxx",
    "python/src/b2Math.cxx",
    "python/src/b2Shape.cxx",
    "python/src/b2WorldCallbacks.cxx",
    "python/src/b2World.cxx",
    "python/src/batch_api.cxx",
    "python/src/b2_user_settings.cpp",
]

include_dirs = ["external/pybind11-2.8.1/include/", "python/src/"]
macros = [("B2_USER_SETTINGS", 1)]
if liquidfun:
    binding_sources += [
        "python/src/b2Particle.cxx",
        "python/src/b2ParticleGroup.cxx",
        "python/src/b2ParticleSystem.cxx",
        "python/src/pyEmitter.cxx",
        "python/src/extensions/b2Emitter.cpp",
    ]
    macros += [("PYBOX2D_LIQUID_FUN", 1)]
    base_dir = "external/box2d-ecf398ca73f31b282cf9e6a500d8af6665654617"


else:
    base_dir = "external/box2d-2.4.1"


box2d_include_dirs = [os.path.join(base_dir, "include"), os.path.join(base_dir, "src")]
src_dir = os.path.join(base_dir, "src")
box2d_sources = sorted([str(path) for path in Path(src_dir).rglob("*.cpp")])


ext_modules = [
    Pybind11Extension(
        "b2d._b2d",
        binding_sources + box2d_sources,
        include_dirs=box2d_include_dirs + include_dirs,
        # Example: passing in the version to the compiled code
        define_macros=[("VERSION_INFO", __version__)] + macros,
    )
]


install_requires = ["numpy", "pydantic"]
setup(
    name="b2d",
    version=__version__,
    author="Thorsten Beier",
    author_email="derthorstenbeier@gmail.com",
    url="https://github.com/pybind/python_example",
    description="A test project using pybind11",
    long_description="",
    ext_modules=ext_modules,
    packages=find_packages(where="./python/module", exclude="test"),
    install_requires=install_requires,
    extras_require={"test": "pytest"},
    package_dir={"": "python/module"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)
