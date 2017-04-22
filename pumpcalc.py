#! python3
"""
pumpcalc.py - Calculates the pressure drop for incompressible flow in a pipeline for pump sizing.

Note: currently only set up for clean commercial steel pipe, schedule 40. Valid for Re > 4000
"""

import math as m

# todo: calculate pressure drop in pipe system

# constants
EPSILON = 0.00015  # absolute roughness (ft) for commercial steel pipe Crane TP-410 page A-24
GRAV_CONST = 32.174      # gravitational constant in ft/sec^2


# pressure drop for feet of commercial steel schedule 40 straight pipe
def head_loss_straight_pipe(vflow, dia, length):
    """
    Determines head loss for a incompressible fluid in a straight pipe of commercial steel, sch40.
    :param vflow: volumetric flow of fluid (GPM)
    :param dia: internal pipe diameter (inches)
    :param length: length of straight pipe (feet)
    :return: head_loss (ft), avg. velocity of fluid (ft/s)
    """
    # determine average velocity of flow

    area = (m.pi * (dia / 2) ** 2) / 144    # cross sectional area of pipe in square feet NOTE: Technically there are
                                            # more exact table data on cross sectional areas of pipe. Can add precision
                                            # later.

    q = vflow * 0.002228                    # convert from GPM to ft^3/sec.  Constant from Crane TP-410 page B-9
    v = q / area                            # average velocity. needs to be in feet per second

    # determine darcy friction factor (f)
    f = 0.25 / (m.log10((EPSILON / (dia / 12)) / 3.7) ** 2)  # only valid for commercial steel pipe sch40

    # Darcy's formula for head loss in feet of fluid
    head_loss = f * (length / (dia / 12)) * (v ** 2 / (2 * GRAV_CONST))

    return head_loss, v

# todo: pressure drop for velocity of flow through fittings

# todo: pressure drop from change in elevation


flow = 400     # in GPM
D = 6           # nominal pipe diameter in inches
L = 100    # length of pipe in feet

H, velocity = head_loss_straight_pipe(flow, D, L)
print('Head loss for a pipe {} inches in diameter and {} feet long is {:.2f} feet'.format(D, L, H))
print('Average velocity for this section is {:.2f}'.format(velocity))
