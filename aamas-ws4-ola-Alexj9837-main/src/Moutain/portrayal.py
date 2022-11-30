
from Moutain.agents import finder_Robot
from Moutain.agents import healer_Robot
from Moutain.agents import Patient


def Moutain_portrayal(agent):
    """
    Determine which portrayal to use according to the type of agent.
    """
    if isinstance(agent, finder_Robot):
        return robot_portrayal(agent)

    elif isinstance(agent, healer_Robot):
        return healer_portrayal(agent)ls

    else:
        return patient_portrayal(agent)


def robot_portrayal(robot):

    if robot is None:
        raise AssertionError
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": robot.x,
        "y": robot.y,
        "scale": 2,
        "heading_x": -1 if robot.isBusy else 1,
        "heading_y": 0,
        # "r":4,
        "Color": "red" if robot.isBusy else "green",
    }


def healer_portrayal(robot):

    if robot is None:
        raise AssertionError
    return {
        "Shape": "arrowHead",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": robot.x,
        "y": robot.y,
        "scale": 2,
        "heading_x": -1 if robot.isBusy else 1,
        "heading_y": 0,
        # "r":4,
        "Color": "black" if robot.isBusy else "purple",
    }


def patient_portrayal(Patient):

    if Patient is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": Patient.x,
        "y": Patient.y,
        "Color": "gold" if Patient.state else "Green",
    }
