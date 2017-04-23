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


# noinspection PyPep8
def find_area(dia):
    """
    Determines pipe area (ft^2) from pipe diameter (in)
    :param dia: inner pipe diameter (inches)
    :return: pipe area (ft^2) - float
    """
    area = (m.pi * (dia / 2) ** 2) / 144    # cross sectional area of pipe in square feet NOTE: Technically there are
                                            # more exact table data on cross sectional areas of pipe. Can add precision
                                            # later.
    return area


def vflow_gpm_to_ft3_per_sec(gpm):
    """
    Converts volume flow from GPM to ft^3/sec
    :param gpm: 
    :return: 
    """
    q = gpm * 0.002228  # convert from GPM to ft^3/sec.  Constant from Crane TP-410 page B-9
    return q


def find_avg_velocity(vflow, area):
    """
    Calculates average velocity
    :param vflow: volumetric flow of fluid (GPM)
    :param area: cross-sectional area of pipe (ft^2)
    :return: average velocity of fluid (ft/s)
    """
    q = vflow_gpm_to_ft3_per_sec(vflow)
    vel = q / area  # average velocity. needs to be in feet per second
    return vel


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

    area = find_area(dia)

    q = vflow_gpm_to_ft3_per_sec(vflow)
    vel = q / area                            # average velocity. needs to be in feet per second

    # determine darcy friction factor (f)
    f = friction_factor_commercial_steel_sch40(dia)

    # Darcy's formula for head loss in feet of fluid
    head_loss = f * (length / (dia / 12)) * (vel ** 2 / (2 * GRAV_CONST))

    return head_loss, vel


def friction_factor_commercial_steel_sch40(dia):
    """
    Calculates Darcy friction factor for Re > 10,000 for commercial steel pipe sch40
    :param dia: inner pipe diameter in inches.
    :return: friction factor f (float)
    """
    f = 0.25 / (m.log10((EPSILON / (dia / 12)) / 3.7) ** 2)  # only valid for commercial steel pipe sch40
    return f


# pressure drop for velocity of flow through fittings
# noinspection PyPep8Naming
def head_loss_fittings(fittings_dict, dia, vflow):
    """
    Returns the sum of resistance coefficients K for valves and fittings.
    :param fittings_dict: dictionary in the format: {'fitting name': {'number': X}}
    :param dia: nominal or inner diameter in inches 
    :type dia: int
    :param vflow: volume flow in GPM
    
    :return: K (float)
    """
    K = 0
    for key, data in fittings_dict.items():
        if key == 'Gate Valve':
            K += 8 * friction_factor_commercial_steel_sch40(dia) * data['number']
        elif key == 'Globe Valve':
            K += 340 * friction_factor_commercial_steel_sch40(dia) * data['number']
        elif key == 'Swing Check Valve':
            K += 100 * friction_factor_commercial_steel_sch40(dia) * data['number']
        elif key == 'Ball Valve':
            K += 3 * friction_factor_commercial_steel_sch40(dia) * data['number']
        elif key == '90 Deg Elbow LR':
            K += 14 * friction_factor_commercial_steel_sch40(dia) * data['number']
        else:
            print('Fitting of unknown type: {}'.format(key))
    area = find_area(dia)
    vel = find_avg_velocity(vflow, area)
    head_loss = K * (vel ** 2 / (2 * GRAV_CONST))

    return head_loss

# todo: pressure drop from change in elevation

flow = 400      # in GPM
D = 6           # nominal pipe diameter in inches
L = 100         # length of pipe in feet

fittings = {'Gate Valve': {'number': 1},
            'Globe Valve': {'number': 1},
            'Ball Valve': {'number': 4},
            '90 Deg Elbow LR': {'number': 8},
            'Sprocket': {'number': 1, 'L/D': 50}}

H, velocity = head_loss_straight_pipe(flow, D, L)
H_fittings = head_loss_fittings(fittings, D, flow)
print('Head loss for a pipe {} inches in diameter and {} feet long is {:.2f} feet'.format(D, L, H))
print('Average velocity for this section is {:.2f}'.format(velocity))
print('Head loss from fittings is {:.2f}'.format(H_fittings))
