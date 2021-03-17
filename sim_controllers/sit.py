"""sit controller."""

from controller import Supervisor

import optparse
import math


class Sit (Supervisor):
    """Control a Sit PROTO."""

    def __init__(self):
        """Constructor: initialize constants."""
        self.BODY_PARTS_NUMBER = 19
        self.MOVE_SEQUENCES_NUMBER = 2
        self.CYCLE_TO_DISTANCE_RATIO = 0.5
        self.speed = 1.00
        self.joints_position_field = []
        self.joint_names = [
            "leftArmAngle", "leftLowerArmAngle", "leftHandAngle",
            "rightArmAngle", "rightLowerArmAngle", "rightHandAngle",
            "leftLegAngle", "leftLowerLegAngle", "leftFootAngle",
            "rightLegAngle", "rightLowerLegAngle", "rightFootAngle",
            "headAngle", "middleTorsoAngle1", "middleTorsoAngle2", 
            "middleTorsoAngle3", "upperTorsoAngle1", "upperTorsoAngle2", 
            "upperTorsoAngle3"
        ]
        self.angles = [
            [-0.80, -2.20],  # left arm
            [-0.80, -0.80],  # left lower arm
            [+0.00, +0.00],  # left hand
            [-0.80, -2.20],  # right arm
            [-0.70, -0.70],  # right lower arm
            [+0.00, +0.00],  # right hand
            [-1.57, -1.57],  # left leg
            [+1.57, +1.57],  # left lower leg
            [+0.00, +0.00],  # left foot
            [-1.57, -1.57],  # right leg
            [+1.57, +1.57],  # right lower leg
            [+0.00, +0.00],  # right foot
            [+0.00, +0.10],  # head
            [+0.00, +0.00],  # middle torso turn left/right
            [+0.00, -0.40],  # middle torso bend front/behind
            [+0.00, +0.00],  # middle torso bend left/right
            [+0.00, +0.00],  # upper torso turn left/right
            [+0.00, -0.40],  # upper torso bend front/behind
            [+0.00, +0.00],  # upper torso bend left/right
        ]
        
        Supervisor.__init__(self)

    def run(self):
        """Set the sitting pose and position."""
        opt_parser = optparse.OptionParser()
        opt_parser.add_option("--speed", type=float, default=0.5, help="Specify speed")
        opt_parser.add_option("--step", type=int, help="Specify time step (otherwise world time step is used)")
        options, args = opt_parser.parse_args()
        
        if options.speed and options.speed > 0:
            self.speed = options.speed
        if options.step and options.step > 0:
            self.time_step = options.step
        else:
            self.time_step = int(self.getBasicTimeStep())
        self.root_node_ref = self.getSelf()
        self.root_translation_field = self.root_node_ref.getField("translation")
        self.root_rotation_field = self.root_node_ref.getField("rotation")
        
        for i in range(0, self.BODY_PARTS_NUMBER):
            self.joints_position_field.append(self.root_node_ref.getField(self.joint_names[i]))

        while not self.step(self.time_step) == -1:
            time = self.getTime()
            current_sequence = int(((time * self.speed) / self.CYCLE_TO_DISTANCE_RATIO) % self.MOVE_SEQUENCES_NUMBER)
            # compute the ratio
            ratio = (time * self.speed) / self.CYCLE_TO_DISTANCE_RATIO - \
                int(((time * self.speed) / self.CYCLE_TO_DISTANCE_RATIO))

            for i in range(0, self.BODY_PARTS_NUMBER):
                current_angle = self.angles[i][current_sequence] * (1 - ratio) + \
                    self.angles[i][(current_sequence + 1) % self.MOVE_SEQUENCES_NUMBER] * ratio
                self.joints_position_field[i].setSFFloat(current_angle)

                        
controller = Sit()
controller.run()
