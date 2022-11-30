# Make a world that is 50x50, on a 250x250 display.
import mesa
from mesa.visualization.UserParam import UserSettableParameter
from Moutain.model import Mountain
from .portrayal import Moutain_portrayal
from .agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 400
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

simulation_params = {   
    }
grid = mesa.visualization.CanvasGrid(Moutain_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    Mountain, [grid], "Risky Moutain", simulation_params
)
