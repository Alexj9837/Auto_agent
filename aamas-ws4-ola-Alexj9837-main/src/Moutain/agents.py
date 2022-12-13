from optparse import check_builtin
import mesa
from Moutain.mountain_loc import mountain_location
import random as rand


NUMBER_OF_CELLS = 50

UNDONE = 0
DONE = 1

Mountain = mountain_location["3k"] + \
    mountain_location["2k"] + mountain_location["1k"]
BIDDING = 10
DEAD_BATTERY = 9
HEALTHY = 8
BUSY_ON_ROUTE_TO_GIVE_AID = 7
WAITING_ON_PATIENTS = 6
ON_MOUNTAIN = 5
BUSY_RETURNING_HOME = 4
BUSY_GIVING_AID = 3
BUSY_FOUND_HUMAN = 2
BUSY = 1
FREE = 0

Found_patients = []
waiting_for_healer_patients = []
healed_patients = []


class finder_Robot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE, battery=rand.randint(80, 100)):
        """
        Initialise state attributes, including:
          * current and next position of the robot
          * state 
          * payload (id of any Patient the robot is carrying)
        """
        super().__init__(id, model,)
        self.x, self.y = pos
        self.next_x, self.next_y = None, None
        self.state = init_state
        self.start_pos = [20, 35]
        self.charging_station = [50, 25]
        self.injured = None
        self.battery = battery

    @property
    def isBusy(self):
        return self.state == BUSY

    def step(self):
        """
        * Obtain action as a result of decision-making
        * trigger action
        """
        str_action = self.make_decision()
        action = getattr(self, str_action)

        action()

    # Robot decision model

    def make_decision(self):
        """
        Simple rule-based architecture, should determine the action to execute based on the robot state.
        """

        if self.state == FREE and (self.x, self.y) not in Mountain:
            print(self.x, self.y)
            action = "move_mountain"
        else:
            if (self.x, self.y) in Mountain and self.state != BUSY_FOUND_HUMAN:
                if self.state != BUSY_RETURNING_HOME:
                    self.state = ON_MOUNTAIN

            if self.state == ON_MOUNTAIN:

                if self.Search_area() == True:
                    action = "wait"
                else:

                    action = self.possible_moves()
        if self.state == DEAD_BATTERY:
            action = "wait"
            print("dead battery ")

        """ 
        setting the state to BUSY_FOUND_HUMAN to force the action wait, while the healer robots move to the area
        """

        if self.state == BUSY_FOUND_HUMAN:
            if self.injured in healed_patients:
                self.state = BUSY_RETURNING_HOME

            else:
                action = "wait"

        if self.state == BUSY_RETURNING_HOME:
            action = "move_charging"

        print("ag_", self.unique_id, " action:",
              action, " State:", self.state,)
        return action

    # Robot actions

    def move(self):
        """
        Move robot to the next position.
        """
        self.model.grid.move_agent(self, (self.next_x, self.next_y))

    def move_to(self, destination):
        """
        Generic method to move robot to a given destination, considering the edges of the grid.
        """
        if self.battery == 0:
            self.state = DEAD_BATTERY
            return "wait"

        else:
            delta_y = 0
            delta_x = 0

            if self.y > destination[1] and self.pos[1] >= 2:
                delta_y = -1
            elif self.y < destination[1] and self.pos[1] <= NUMBER_OF_CELLS - 1:
                delta_y = 1

            if self.x > destination[0] and self.pos[0] >= 2:
                delta_x = -1
            elif self.x < destination[0] and self.pos[0] < NUMBER_OF_CELLS - 1:
                delta_x = 1

            self.next_x = self.x + delta_x
            self.next_y = self.y + delta_y

            self.battery = self.battery - 0.1
            print(self.battery)
            self.move()

    def move_up(self):
        self.move_to((self.x, self.y + 1))
        self.move()

    def move_down(self):
        self.move_to((self.x, self.y - 1))
        self.move()

    def move_left(self):
        self.move_to((self.x - 1, self.y))
        self.move()

    def move_right(self):
        self.move_to((self.x + 1, self.y))
        self.move()

    def possible_moves(self):
        possible_moves_list = []
        if (self.x + 1, self.y) in Mountain:
            possible_moves_list.append("move_right")
        if (self.x - 1, self.y) in Mountain:
            possible_moves_list.append("move_left")
        if (self.x, self.y - 1) in Mountain:
            possible_moves_list.append("move_down")
        if (self.x, self.y + 1) in Mountain:
            possible_moves_list.append("move_up")

        return rand.choice(possible_moves_list)

    def move_mountain(self):
        """
        Move the robot to the mountain base
        """
        if self.pos == self.start_pos:
            return "wait"
        else:
            self.move_to([self.start_pos[0], self.start_pos[1]])

    def move_charging(self):

        self.move_to([self.charging_station[0], self.charging_station[1]])

    def wait(self):
        """
        Keep the same position as the current one.
        """
        self.next_x = self.x
        self.next_y = self.y

    def advance(self):
        """
        Advances position of the robot.
        """
        self.x = self.next_x
        self.y = self.next_y

    def Search_area(self):
        """
        Search the local area around the finder robot. and append
        """
        nbs = [nb for nb in self.model.grid.neighbor_iter(
            (self.x, self.y), True)]
        for i in range(len(nbs)):
            if isinstance(nbs[i], Patient):
                patient = nbs[0]
                if (patient.x, patient.y) not in Found_patients:
                    waiting_for_healer_patients.append((patient.x, patient.y))
                    Found_patients.append((patient.x, patient.y))
                    self.injured = (patient.x, patient.y)
                    self.state = BUSY_FOUND_HUMAN
                    return True
                else:
                    return False

    def Found_patients():
        print(len(Found_patients))
        if len(Found_patients) == 3:
            print("all patients have been found")


class healer_Robot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=BIDDING, battery=100):
        """
        Initialise state attributes, including:
          * current and next position of the robot
          * state 
        """
        super().__init__(id, model)
        self.x, self.y = pos
        self.pos = (self.x, self.y)
        self.lane = self.y
        self.next_x, self.next_y = None, None
        self.state = init_state
        self.start_loc = [0, 24]
        self.target = None
        self.future_key = None
        self.current_key = None
        self.counter = 0
        self.battery = battery
        self.tokens = battery

    @property
    def isBusy(self):
        return self.state == BUSY  # **TODO Revise if robot states are updated  **

    def step(self):
        """
        * Obtain action as a result of decision-making
        * trigger action
        """
        str_action = self.make_decision()
        action = getattr(self, str_action)

        action()

    # Robot decision model

    def make_decision(self):
        """

        Simple rule-based architecture, should determine the action to execute based on the robot state.

        """
        if self.state == BIDDING:
            action = "wait"

        if self.state == FREE:
            action = self.check_patient_list()

        if self.state == BUSY_ON_ROUTE_TO_GIVE_AID:
            action = "move_give_aid"
            if self.pos == self.target:
                action = self.give_aid()

        if self.state == BUSY_RETURNING_HOME:
            action = "move_home"
        # **TODO Implement **

        print("ag_", self.unique_id, " action:",
              action, " State:", self.state,)
        return action

    # Robot actions

    def check_patient_list(self):
        if waiting_for_healer_patients == []:
            return "wait"
        else:
            if self.target in Found_patients:
                return "wait"
            else:
                self.target = waiting_for_healer_patients.pop()
                print(self.target)
                self.state = BUSY_ON_ROUTE_TO_GIVE_AID

    def move(self):
        """
        Move robot to the next position.
        """
        self.model.grid.move_agent(self, (self.next_x, self.next_y))

    def move_to(self, destination):
        """
        Generic method to move robot to a given destination, considering the edges of the grid.
        """
        delta_y = 0
        delta_x = 0

        if self.y > destination[1] and self.pos[1] >= 2:
            delta_y = -1
        elif self.y < destination[1] and self.pos[1] <= NUMBER_OF_CELLS - 1:
            delta_y = 1

        if self.x > destination[0] and self.pos[0] >= 2:
            delta_x = -1
        elif self.x < destination[0] and self.pos[0] < NUMBER_OF_CELLS - 1:
            delta_x = 1

        self.next_x = self.x + delta_x
        self.next_y = self.y + delta_y

        if self.climbing() == True:
            self.battery = self.battery - 0.1
            self.move()
            print("Not climbing")

        elif self.counter == 3:
            self.battery = self.battery - 0.1
            self.move()
            self.counter = 0
            print(self.counter)
        else:
            self.counter += 1
            self.next_x = self.x
            self.next_y = self.y
            print(f"climbing stage {self.counter} of 3")
            print(self.counter)

    def climbing(self):
        next_pos1 = (self.next_x, self.next_y)

        if self.pos not in Mountain:
            return True

        for keys1 in mountain_location:
            if next_pos1 in mountain_location[keys1]:
                self.future_key = keys1

        for keys2 in mountain_location:
            if self.pos in mountain_location[keys2]:
                self.current_key = keys2

        return self.current_key == self.future_key

    def wait(self):
        """
        Keep the same position as the current one.
        """
        self.next_x = self.x
        self.next_y = self.y

    def move_start(self):
        """
        Move the robot to the workshop
        """
        self.move_to([self.start_loc[0], self.start_loc[1]])

    def move_give_aid(self):
        """
        Move the robot to deliver aid to patient
        """

        self.move_to(self.target)

    def give_aid(self):
        "setting the health of the target to 100"
        patient = self.model.grid.get_cell_list_contents((self.x, self.y))[0]
        patient.health = 100
        patient.state = HEALTHY
        patient.state = DONE
        waiting_for_healer_patients.pop
        healed_patients.append((patient.x, patient.y))
        self.state = BUSY_RETURNING_HOME

    def advance(self):
        """
        Advances position of the robot.
        """
        self.x = self.next_x
        self.y = self.next_y

    def move_up(self):

        if self.move_to((self.x, self.y + 1)):

            self.move()

    def move_down(self):
        self.move_to((self.x, self.y - 1))
        self.move()

    def move_left(self):
        self.move_to((self.x - 1, self.y))
        self.move()

    def move_right(self):
        self.move_to((self.x + 1, self.y))
        self.move()

    def move_home(self):

        self.move_to((1, 25))


class Patient(mesa.Agent):
    """Represents a Patient in the mountain."""

    def __init__(self, id, pos, model, init_state=UNDONE, health=60, found=False):
        """
        Intialise state and position of the Patient
        """
        super().__init__(id, model)
        self.state = UNDONE
        self.next_state = UNDONE
        self.x, self.y = pos
        self.pos
        self.health = health
        self.battery = None
        self.found = found

    def set_state(self, new_state):
        """
        Enables update of the state of the Patient by the robot.
        """
        self.state = new_state
