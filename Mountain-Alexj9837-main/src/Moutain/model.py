import mesa
import numpy as np
from Moutain.agents import finder_Robot, healer_Robot, Patient
from Moutain.mountain_loc import mountain_location
from .agents import DONE
from Moutain.agents import Found_patients
from Moutain.agents import BIDDING, FREE
import random as rand


def pending_patients(model):
    return len([a for a in model.schedule.agents if isinstance(a, Patient) and a.state != DONE])


class Mountain(mesa.Model):
    """ Model representing an automated Mountain recuse"""

    def __init__(self, n_robots=3, n_healers=3, n_Patient=3, width=50, height=50, seed=123):
        """
            * Set schedule defining model activation
            * Sets the number of robots as per user input
            * Sets the grid space of the model
            * Create n Robots as required and place them randomly on the edge of the left side of the 2D space.
            * Create m Boxes as required and place them randomly within the model (Hint: To simplify you can place them in the same horizontal position as the Robots). Make sure robots or boxes do not overlap with each other.
        """
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.n_robots = n_robots
        self.n_Patient = n_Patient
        self.n_healers = n_healers

        # Use a simple grid, where edges wrap around.
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.tick = 0
        y_s = []
        for n in range(self.n_robots):
            heading = (1, 0)
            # append element in vector
            x = 49
            y = 1
            while True:
                y = self.random.randint(1, height-1)
                if self.grid.is_cell_empty((x, y)):
                    break

            y_s.append(y)
            pr = finder_Robot(n, (x, y), self)

            self.schedule.add(pr)
            self.grid.place_agent(pr, (x, y))

        for n in range(self.n_healers):
            heading = (1, 0)
            # append element in vector
            x = 1
            y = 1
            while True:
                y = self.random.randint(1, height-1)
                if self.grid.is_cell_empty((x, y)):
                    break

            y_s.append(y)
            pr = healer_Robot(n+self.n_robots, (x, y), self,
                              battery=rand.randint(80, 100))

            self.schedule.add(pr)
            self.grid.place_agent(pr, (x, y))

        for n in range(self.n_Patient):
            MountainPositions = mountain_location.keys()
            keys = [key for key in mountain_location]
            while True:
                x, y = self.random.choice(mountain_location[keys[n]])
                if self.grid.is_cell_empty((x, y)):
                    break

            b = Patient(n+self.n_healers+self.n_robots, (x, y), self)
            self.schedule.add(b)
            self.grid.place_agent(b, (x, y))

        self.running = True

        self.datacollector = mesa.DataCollector(
            model_reporters={"pending_patients": pending_patients}, agent_reporters={"state": "state", "battery": "battery"}
        )

    def step(self):
        if pending_patients(self) > 0:
            if Found_patients != 0:
                self.run_auction()
            self.schedule.step()
        else:
            self.running = False
        print("running...", self.tick)
        self.datacollector.collect(self)

    def run_auction(self):
        healer_agents_l = [a for a in self.schedule.agents if isinstance(
            a, healer_Robot) and a.state == BIDDING]
        for a in healer_agents_l:
            tokens_amount = []
            tokens_amount.append(a.tokens)
            for token in tokens_amount:
                if token >= max(tokens_amount):
                    a.tokens = None
                    a.state = FREE
                    tokens_amount.pop(tokens_amount.index(max(tokens_amount)))
