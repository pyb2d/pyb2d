import sys
import os


import os, sys


def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False    

def is_pyodide():
    return "pyodide" in sys.modules


def is_doc_build():
    return os.environ.get('READTHEDOCS') == 'True' or os.environ.get('PYB2D_SPHINX_BUILD') == 'True' 

def default_backend():
    if is_doc_build():
        from b2d.testbed.backend.matplotlib_gif_gui import MatplotlibGifGui
        return MatplotlibGifGui
    elif is_pyodide():
        raise RuntimeError("pyodide has not yet a backend")
    elif is_notebook():
        from b2d.testbed.backend.jupyter import JupyterGui
        return JupyterGui

    else:
        try:
            from b2d.testbed.backend.pygame import PygameGui
            return PygameGui
        except:
            pass

        try:
            from b2d.testbed.backend.kivy import KivyGui
            return KivyGui
        except:
            raise RuntimeError("no backend found: try installing pygame or kivy")



def run(example_cls, backend=None, settings=None, gui_settings=None):

    if isinstance(backend, str):
        backend_name = backend
        backend_cls = None
    else:
        backend_name = None
        backend_cls = backend

    if backend_name is not None:
        if backend_name == "pygame":
            from b2d.testbed.backend.pygame import PygameGui
            backend_cls = PygameGui
        elif backend_name == "kivy":
            from b2d.testbed.backend.kivy import KivyGui
            backend_cls = KivyGui
        elif backend_name == "matplotlib_gif":
            from b2d.testbed.backend.matplotlib_gif_gui import MatplotlibGifGui
            backend_cls = MatplotlibGifGui
        elif backend_name == "jupyter":
            from b2d.testbed.backend.jupyter import JupyterGui
            backend_cls = JupyterGui

    if backend_cls is None:
        backend_cls = default_backend()

    if gui_settings is None:
        gui_settings = backend_cls.Settings()


    return example_cls.run(backend_cls, settings=settings, gui_settings=gui_settings)