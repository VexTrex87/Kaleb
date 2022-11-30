from vex import *
import math

brain = Brain()
controller = Controller()

front_left_wheel = Motor(Ports.PORT3)
back_left_wheel = Motor(Ports.PORT4)
left_wheels = MotorGroup(front_left_wheel, back_left_wheel)

front_right_wheel = Motor(Ports.PORT1, True)
back_right_wheel = Motor(Ports.PORT2, True)
right_wheels = MotorGroup(front_right_wheel, back_right_wheel)

drivetrain = DriveTrain(left_wheels, right_wheels)
intaker = Motor(Ports.PORT5, GearSetting.RATIO_6_1)
indexer = Motor(Ports.PORT6, GearSetting.RATIO_6_1)
launcher = Motor(Ports.PORT7, GearSetting.RATIO_6_1)
inertia_sensor = Inertial(Ports.PORT8)
gps_sensor = Gps(Ports.PORT9)

expansion = DigitalOut(brain.three_wire_port.b)

class Robot():
    def __init__(self):
        Competition(self.driver_controlled, self.autonomous)

        drivetrain.set_stopping(COAST)
        inertia_sensor.calibrate()

        self.intake_forward()
        launcher.set_velocity(100, PERCENT)
        launcher.spin(FORWARD)

        print('Ready')

        while True:
            self.update_brain()
            wait(1, SECONDS)

    def driver_controlled(self):
        controller.axis1.changed(self.on_controller_changed)
        controller.axis3.changed(self.on_controller_changed)

        controller.buttonL1.pressed(self.intake_forward)
        controller.buttonL2.pressed(self.intake_reverse)

        controller.buttonR1.pressed(self.launch)
        controller.buttonR2.pressed(self.expand)

    def autonomous(self):
        pass

    def programming_skills_left(self):
        pass

    def programming_skills_right(self):
        pass

    def move(self, target_distance, velocity):
        WHEEL_CIRCUMFERENCE = math.pi * 3.4

        left_wheels.reset_position()
        right_wheels.reset_position()
        drivetrain.set_stopping(COAST)
        drivetrain.set_drive_velocity(velocity, PERCENT)
        drivetrain.drive(FORWARD)

        ### PID STARTS HERE
        Kp = 0.01
        Kd = 0
        Ki = 0

        error = 0
        last_error = 0
        integral = 0
        derivative = 0

        distance_traveled = 0

        while distance_traveled < target_distance:
            left_degrees = left_wheels.position(DEGREES)
            right_degrees = right_wheels.position(DEGREES)
            average_degrees = (left_degrees + right_degrees) / 2
            distance_traveled = average_degrees / 360 * WHEEL_CIRCUMFERENCE

            error = target_distance - distance_traveled
            integral += error
            derivative = error - last_error

            power = (error * Kp) + (integral * Ki) + (derivative * Kd)
            print(error, error * Kp, integral * Ki, derivative * Kd, power)
            drivetrain.set_drive_velocity(power, PERCENT)
            last_error = error
            wait(0.02, SECONDS)

            # PID ENDS HERE

        drivetrain.stop(COAST)

    def turn(self, degrees):
        pass

    def intake_forward(self):
        controller.rumble('.')
        intaker.set_velocity(100, PERCENT)
        intaker.spin(FORWARD)

    def intake_reverse(self):
        controller.rumble('.')
        intaker.set_velocity(100, PERCENT)
        intaker.spin(REVERSE)

    def launch(self):
        controller.rumble('.')

        indexer.set_timeout(1, SECONDS)
        indexer.set_stopping(COAST)
        indexer.set_max_torque(100, PERCENT)

        indexer.spin_for(FORWARD, 75, DEGREES, 100, PERCENT)
        wait(0.5, SECONDS)
        indexer.spin_for(REVERSE, 90, DEGREES, 100, PERCENT)

    def expand(self):
        controller.rumble('.')
        expansion.set(True)

    def on_controller_changed(self):
        x_power = controller.axis1.position()
        y_power = controller.axis3.position()

        left_wheels.set_velocity(y_power + x_power, PERCENT)
        right_wheels.set_velocity(y_power - x_power, PERCENT)

        left_wheels.spin(FORWARD)
        right_wheels.spin(FORWARD)

    def update_brain(self):
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.set_font(FontType.MONO30)

        drivetrain_temperature = drivetrain.temperature(PERCENT)
        brain.screen.set_pen_color(drivetrain_temperature > 60 and Color.RED or Color.GREEN)
        brain.screen.print('Drivetrain: ', round(drivetrain_temperature))
        brain.screen.next_row()

        intaker_temperature = intaker.temperature(PERCENT)
        brain.screen.set_pen_color(intaker_temperature > 60 and Color.RED or Color.GREEN)
        brain.screen.print('Intake: ', round(intaker_temperature))
        brain.screen.next_row()

        indexer_temperature = indexer.temperature(PERCENT)
        brain.screen.set_pen_color(indexer_temperature > 60 and Color.RED or Color.GREEN)
        brain.screen.print('Indexer: ', round(indexer_temperature))
        brain.screen.next_row()

        launcher_temperature = launcher.temperature(PERCENT)
        brain.screen.set_pen_color(launcher_temperature > 60 and Color.RED or Color.GREEN)
        brain.screen.print('Launcher: ', round(launcher_temperature))
        brain.screen.next_row()

        battery = brain.battery.capacity()
        brain.screen.set_pen_color(battery < 20 and Color.RED or Color.GREEN)
        brain.screen.print('Battery: ', round(battery))
        brain.screen.next_row()

        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_font(FontType.MONO60)
        brain.screen.print('23322A (Orion)')

if __name__ == '__main__':
    robot = Robot()
    # robot.move(24, 100)
