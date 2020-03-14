#!/usr/bin/env python3

import animus_py3 as animus
import animus_utils as utils
import sys
import logging
import random
import cv2

animus.version()
log = utils.create_logger("MyAnimusApp", logging.INFO)

success = animus.login_user("daniel@cyberselves.com", "cyberpass123")
if success:
    log.info("Logged in")
else:
    sys.exit(-1)

robots_found = animus.get_robots(True, True)

if len(robots_found) == 0:
    log.info("No robots available")
    sys.exit(-1)

for robot in robots_found:
    if robot.Available:
        available = "Robot Available"
    else:
        available = "Robot Unavailable"
    log.info("{}: {} robot from {} - {}".format(robot.Name, robot.Model, robot.Make, available))

my_robot_name = "Agnetha"
chosen_robot_details = None

for robot in robots_found:
    if robot.Name == my_robot_name:
        chosen_robot_details = robot

if chosen_robot_details is None:
    log.error("Please specify a valid robot name")
    sys.exit(-1)

myrobot = animus.Robot(chosen_robot_details)
connected = myrobot.connect()
if not connected:
    print("Could not connect with robot {}".format(myrobot.robot_details.ID))
    sys.exit(-1)

# -------------Auditory - Voice Loop------------------------
# try:
# open_success = myrobot.open_modality("audition")
# if not open_success:
#     log.error("Could not open robot audition modality")
#     sys.exit(-1)

# open_success = myrobot.open_modality("voice")
# if not open_success:
#     log.error("Could not open robot voice modality")
#     sys.exit(-1)
    # while True:
    #     msg = input("Press q to exit")
    #     if msg == "q":
    #         break
# except KeyboardInterrupt:
#     log.info("Closing down")
# except SystemExit:
#     log.info("Closing down")


# ----------------Motor Visual Loop------------------------------------
# open_success = myrobot.open_modality("vision")
# if not open_success:
#     log.error("Could not open robot vision modality")
#     sys.exit(-1)

# open_success = myrobot.open_modality("motor")
# if not open_success:
#     log.error("Could not open robot motor modality")
#     sys.exit(-1)


# motorDict = utils.get_motor_dict()
# list_of_motions = [motorDict.copy()]

# motorDict["head_left_right"] = 20 * utils.HEAD_RIGHT
# motorDict["head_up_down"] = 20 * utils.HEAD_UP
# motorDict["head_roll"] = 0.0        # This movement is not possible with the robots
# motorDict["body_forward"] = 0.0
# motorDict["body_sideways"] = 0.0
# motorDict["body_rotate"] = 0.0
# list_of_motions.append(motorDict.copy())

# motorDict["head_left_right"] = 20 * utils.HEAD_LEFT
# list_of_motions.append(motorDict.copy())

# motorDict["head_up_down"] = 20 * utils.HEAD_DOWN
# list_of_motions.append(motorDict.copy())

# counter = 0
# motion_counter = 0

# cv2.namedWindow("RobotView")
# try:
#     while True:
#         imageFrame = myrobot.get_modality("vision")
#         if imageFrame is not None:
#             imageFrame = cv2.resize(imageFrame, (640, 480))
#             cv2.imshow("RobotView", imageFrame)
#             j = cv2.waitKey(1)
#             if j == 27:
#                 break

#             counter += 1
#             if counter > 50:
#                 counter = 0
#                 if motion_counter >= len(list_of_motions):
#                     motion_counter = 0
#                 ret = myrobot.set_modality("motor", list(list_of_motions[motion_counter].values()))
#                 motion_counter += 1

#     cv2.destroyAllWindows()
# except KeyboardInterrupt:
#     log.info("Closing down")
# except SystemExit:
#     log.info("Closing down")


# ---------------------------Emotive speech--------------------------
# open_success = myrobot.open_modality("speech")
# if not open_success:
#     log.error("Could not open robot speech modality")
#     sys.exit(-1)

# open_success = myrobot.open_modality("emotion")
# if not open_success:
#     log.error("Could not open robot emotion modality")
#     sys.exit(-1)

# log.info(utils.emotions_list)

# # Uncomment to send things for the robot to say
# try:
#     while True:
#         msg = input("Robot say: ")
#         myrobot.set_modality("speech", "Hello")
#         myrobot.set_modality("emotion", random.choice(utils.emotions_list))
# except KeyboardInterrupt:
#     log.info("Closing down")
# except SystemExit:
#     log.info("Closing down")

myrobot.disconnect()
animus.close_client_interface()
