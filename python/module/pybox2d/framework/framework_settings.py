class FrameworkSettings(object):
    # which gui backend
    backend = 'pg'

    # Physics options
    hz = 60.0
    velocit_iterations = 8
    position_iterations = 3
    # Makes physics results more accurate (see Box2D wiki)
    enable_warm_starting = True
    enable_continuous = True     # Calculate time of impact
    enable_sub_stepping = False

    # Drawing
    draw_stats = True
    draw_shapes = True
    draw_joints = True
    draw_core_shapes = False
    draw_aabbs = False
    draw_obbs = False
    draw_pairs = False
    draw_contact_points = False
    draw_particles = True
    max_contact_points = 100
    draw_contact_normals = False
    draw_ffps = True
    draw_menu = True             # toggle by pressing F1
    draw_coms = False            # Centers of mass
    point_size = 2.5             # pixel radius for drawing points



    # particle drawing
    draw_colored_particles = True


    # Miscellaneous testbed options
    pause = False
    single_step = False
    # run the test's initialization without graphics, and then quit (for
    # testing)
    only_init = False

