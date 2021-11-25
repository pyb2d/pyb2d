import sys
import os

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
        return MatplotlibGifGui,{}
    elif is_pyodide():
        raise RuntimeError("pyodide has not yet a backend")
    elif is_notebook():
        from b2d.testbed.backend.jupyter import JupyterGui
        return JupyterGui,{}
    else:
        from b2d.testbed.backend.pygame import PygameGui
        return PygameGui,{}



def run(example_cls, backend_cls=None, gui_settings=None):

    if backend_cls is None:
        backend_cls, default_gui_settings = default_backend()
        if gui_settings is None:
            gui_settings = default_gui_settings

    if gui_settings is None:
        gui_settings = dict()

    return example_cls.run(backend_cls, gui_settings=gui_settings)