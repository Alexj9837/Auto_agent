from optparse import check_builtin
import mesa

NUMBER_OF_CELLS = 50
BUSY = 0
FREE = 1

UNDONE = 0
DONE = 1

Found_patients = []

healed_patients = []


class finder_Robot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE):
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
       # while self.y != 25:

        action = "move"

        print("ag_", self.unique_id, " action:", action)
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
            (self.x, self.y), False)]
        for i in range(len(nbs)):
            if isinstance(nbs[i], Patient):
                Patient = nbs[0]
                Found_patients.append(Patient.self.x, Patient.self.y)


class healer_Robot(mesa.Agent):
    def __init__(self, id, pos, model, init_state=FREE):
        """
        Initialise state attributes, including:
          * current and next position of the robot
          * state 
        """
        super().__init__(id, model)
        self.x, self.y = pos
        self.lane = self.y
        self.next_x, self.next_y = None, None
        self.state = init_state

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

        action = "check_patient_list"

        # **TODO Implement **

        print("ag_", self.unique_id, " action:", action)
        return action

    # Robot actions

    def check_patient_list(Found_patients):
        while Found_patients == []:
            action = "wait"
        else:
            Found_patients.pop()

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
        self.move()

    def wait(self):
        """
        Keep the same position as the current one.
        """
        self.next_x = self.x
        self.next_y = self.y

    def move_home(self):
        """
        Move the robot to the workshop
        """
        self.move_to([self.x, self.workshop])
        self.move_payload()

    def advance(self):
        """
        Advances position of the robot.
        """
        self.x = self.next_x
        self.y = self.next_y


class Patient(mesa.Agent):
    """Represents a Patient in the mountain."""

    def __init__(self, id, pos, model, init_state=UNDONE):
        """
        Intialise state and position of the Patient
        """
        super().__init__(id, model)
        self.state = UNDONE
        self.next_state = UNDONE
        self.x, self.y = pos

    def set_state(self, new_state):
        """
        Enables update of the state of the Patient by the robot.
        """
        self.state = new_state
