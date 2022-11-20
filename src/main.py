from vex import *

brain = Brain()
controller = Controller()

front_left_wheel = Motor(Ports.PORT1)
front_right_wheel = Motor(Ports.PORT2)
left_wheels = MotorGroup(front_left_wheel, front_right_wheel)

back_left_wheel = Motor(Ports.PORT3)
back_right_wheel = Motor(Ports.PORT4)
right_wheels = MotorGroup(back_left_wheel, back_right_wheel)
drivetrain = DriveTrain(left_wheels, right_wheels)

intaker = Motor(Ports.PORT5)
launcher = Motor(Ports.PORT6, GearSetting.RATIO_6_1)

indexer = DigitalOut(brain.three_wire_port.a)
expansion = DigitalOut(brain.three_wire_port.b)

class Robot():
    def __init__(self):
        Competition(self.driver_controlled, self.autonomous)

        launcher.set_velocity(100, PERCENT)
        launcher.spin(FORWARD)

        self.intake_forward()

    def driver_controlled(self):
        controller.axis1.changed(self.on_controller_changed)
        controller.axis3.changed(self.on_controller_changed)

        controller.buttonL1.pressed(self.intake_forward)
        controller.buttonL2.pressed(self.intake_reverse)

        controller.buttonR1.pressed(self.launch)
        controller.buttonR1.pressed(self.expand)

    def autonomous(self):
        pass

    def programming_skills_left(self):
        pass

    def programming_skills_right(self):
        pass

    def move(self, distance):
        pass

    def turn(self, degrees):
        pass

    def intake_forward(self):
        intaker.set_velocity(100, PERCENT)
        intaker.spin(FORWARD)

    def intake_reverse(self):
        intaker.set_velocity(100, PERCENT)
        intaker.spin(REVERSE)

    def launch(self):
        indexer.set(True)
        wait(0.5, SECONDS)
        indexer.set(False)

    def expand(self):
        expansion.set(True)

    def on_controller_changed(self):
        x_power = controller.axis1.value()
        y_value = controller.axis3.value()

        left_wheels.set_velocity(y_value + x_power)
        right_wheels.set_velocity(y_value - x_power)

if __name__ == '__main__':
    Robot()
