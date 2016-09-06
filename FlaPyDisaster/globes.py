from general import flapy_app as fla
flapy_app = None


def global_init():
    global flapy_app
    flapy_app = fla.FlaPyApp()
