TASK ONE-
Task one may be found inside the task one folder.



TASK TWO-
The basic operation of robots include:

    • Exploring and movement towards the mountain and the missing persons
        This has been done by the function move mountain in agents.py line 172

    • Drones locate the persons to be rescued and wait for the first-aid      terrain robots, once they get there, they all return to their base stations.

        This task has been acheived using .randchoice and making a list of all availbe choices and legal choices(keeps on the mountain) once the direction has been move it calls the search area function, if it finds a patient that isn't on the list of found patients it then waits by the patient and adds its location onto a list of pending patients which the terain robots bid on. once the Terain robot is at the patients location, the scout robot heads to base using the Move_charging function.

    • First-aid terrain robots move randomly to locate the persons and deliver
    the first-aid kit.

        this task is super ccided by later tasks, and won't be shown in the code base. terrain robot no longer randomly search and simply heads straight to the patients as it has its location as a target.

        evidence of this is on line 272-275 in the make decision func, and 377-385 for giving the pateint the health. it does this buy setting the pateints health to 100 and change the patient state to HEALTHY



    The extended operation of robots include:
    • Communication of drone and terrain robots to provide first-aid. Drone
    can send messages to individual robots or broadcast location of a person,
    once found.

        This task as been complted, this is done via three lists lines 26-28,
        Found_patients = [] - this stores all the x and ys of found patients, the scout drones when searching CODE FOUND 199-215 check if the patient they've discoved is on this list if they're not on the list it says else it carries on searching 217-220, the stop them getting caught on the same patient.

        waiting_for_healer_patients = [] -this list holds patient that have been asaigned a healer drone, this is to eliminte the risk of 2 healer drones being sent to the same location.

        healed_patients = [] = this list just keeps track of all healed_patients.

    • Robots have a battery whose energy is consumed as the simulation progresses.

        All robots are given a battery state, this is reducded by an X amount per step they move, the minus happens during the move_to function.
        CODE FOUND LINE 139


    • Team cooperation among terrain robots. For example, by enabling choosing
    the terrain robot that will serve a particular person, based on the available
    robot battery and the urgency for serving the persons.

        this task has been achieved by the use of a auction, a robot can only bid if its battery is high enough to make the trip, elimnating the risk of it dying mid route. CODE FOUND in Model.py 96-106 

Task 3: Multiagent System Analysis (15% assignment marks)
Create a Jupyter notebook for analysis of the performance of the robots. This
should include at least two relevant performance indicators:

1. How long (time steps) did it take the robots to find the three persons

   Please look at Simulation_aa for this. The secound heading "pending patients and steps taken" covers this part of the marking scheme. It tracks the list pending_patients

2. Propose an additional indicator that you see fit.Create plots for each indicator and briefly provide a descriptive analysis of them.

   The first heading "battery drain for each agent", this shows the battery state of the three healers and three recon drones.

Task 4: Agent Learning (20% assignment marks)
You are required to explore and choose one of the Reinforcement Learning
algorithms not covered in the module sessions and write a short report (300
words) describing in your own words how the algorithm works. In addition, a
flow chart of the algorithm and an example would make your report stronger.
Some of the algorithms available are listed here, however you are encouraged to
browse around and choose the one you feel more comfortable with.

    Please find inside folder task4.
    

all tasks and targets met.Thank you for reading, and enjoy your holidays

