[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9112942&assignment_repo_type=AssignmentRepo)
# AA-MAS - Worksheet Week 4 - OLA Submission

**IMPORTANT** <u>This worksheet is an OPTIONAL Assessment (OLA).</u>. If you submit it, it will be assessed. This OLA is worth 5 marks.

**Date**: 28/Oct/22
 
**Topic**: Agent Architectures 

**Objective**: To assess and practice the design and implementation of basic agent architectures and decision-making approaches in the context of a warehouse application.

## Overview

We have seen how a "perfect" modern warehouse works with robots picking and carrying boxes to the *shipping* area at the left of the grid. 

For this worksheet, consider a risky warehouse where there is a risk that the contents of the boxes gets damaged while being transported by the robots. In that case, the robots need to take the boxes to the *workshops* instead of taking them to the *shipping* area. The expected behaviour is presented in this [video](risky-warehouse.mp4)

When the contents of the box gets damaged the box is turned to *yellow* and the robots take it to the *workshop*.

There are only two robots in the warehouse and *workshops* are located at the top and bottom of the grid. 

## **TASKS**

### Task 1:  Design (40% worksheet marks)

For this task you need to create a statechart diagram for the robot working in the risky warehouse. 

**HINT**

The robot is capable of performing the following actions:

* `move_fw`: move forward towards a box in the lane (row) it is assigned to.
* `move_bw`: move backwards towards ths shipping area
* `move_ws`: move towards the workshop
* `move_lane`: move towards the lane (row) it is assigned to.
* `pick`: Pick up a box
* `drop_off`: Drop off the box.
* `wait`: wait in a give position.

You can start identifying the relevant states, then identify transitions based on these actions. Moreover, transitions can also come from *environment events* e.g. the items in a box get damaged.

[!] Create a folder named "task_1" in the root of your repo and save the image file (.png, .jpg, .pdf) with your diagram in that folder. Then commit and push to your github remote repo.

**Assessment Criteria**

* (1) Key states identified: 10% marks
* (2) Key transitions identified: 10% marks
* (3) Both (1) and (2) are achieved: 20% marks
* Apart from (3), the diagram is submitted during the practical session: 40% marks

### Task 2: Implementation (60% worksheet marks)

Use your diagram to implement the `make-decision` method of the robot agent in the `agents.py` file. The states provided in the implementation are the ones used in the previous worksheets and might not be enough for the *risky warehouse* robots. So you might need to modify existing states or add new ones as you see fit. **If you rename a state or remove it, you need to check other methods where this state was used and update these accordingly**.

**HINT**

* The method `is_payload_safe` enables you to check whether the payload is safe or it is broken.

[!] You need to update existing source code, then commit and push to your github repo. It is not expected that you create new source files.

**Assessment Criteria**

* (4) Code compiles with some behaviour achieved: 30% marks
* (5) Whole behaviour achieved: 50% marks
* In addition to (5), the code is submitted within the practical session: 60% marks
