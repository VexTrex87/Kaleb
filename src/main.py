from vex import *
import time

brain = Brain()
controller = Controller()

front_left_wheel = Motor(Ports.PORT17)
back_left_wheel = Motor(Ports.PORT16)
left_wheels = MotorGroup(front_left_wheel, back_left_wheel)

front_right_wheel = Motor(Ports.PORT1, True)
back_right_wheel = Motor(Ports.PORT2, True)
right_wheels = MotorGroup(front_right_wheel, back_right_wheel)

inertia_sensor = Inertial(Ports.PORT3)
back_distance_sensor = Distance(Ports.PORT4)
front_distance_sensor = Distance(Ports.PORT5)
roller_sensor = Optical(Ports.PORT6)
auton_selector = Bumper(brain.three_wire_port.b)

drivetrain = SmartDrive(left_wheels, right_wheels, inertia_sensor)
intaker = Motor(Ports.PORT19, GearSetting.RATIO_6_1)
indexer = Motor(Ports.PORT18, GearSetting.RATIO_36_1)
launcher = Motor(Ports.PORT14, GearSetting.RATIO_6_1)
roller = Motor(Ports.PORT13, GearSetting.RATIO_36_1)
expansion = DigitalOut(brain.three_wire_port.a)

class Robot():
    def __init__(self):
        Competition(self.driver_controlled, self.auton)
        
        self.selected_auton = 3
        self.autons = [
            {'name': 'LEFT SINGLE', 'action': self.left_single_auton}, 
            {'name': 'LEFT DOUBLE', 'action': self.left_double_auton}, 
            {'name': 'RIGHT SINGLE', 'action': self.right_single_auton}, 
            {'name': 'PROGRAMMING SKILLS', 'action': self.programming_skills}]
        
        self.pre_auton()

    def pre_auton(self):
        auton_selector.pressed(self.select_auton)

        drivetrain.set_stopping(COAST)

        inertia_sensor.calibrate()
        while inertia_sensor.is_calibrating():
            wait(0.1, SECONDS)

        print('Ready')

        while True:
            self.update_brain()
            wait(1, SECONDS)

    def driver_controlled(self):
        controller.axis1.changed(self.on_controller_changed)
        controller.axis3.changed(self.on_controller_changed)

        controller.buttonL1.pressed(self.start_intake)
        controller.buttonL1.released(self.stop_intake)
        controller.buttonL2.pressed(self.start_roller)
        controller.buttonL2.released(self.stop_roller)

        controller.buttonR1.pressed(self.launch)
        controller.buttonR2.pressed(self.expand)

        controller.buttonUp.pressed(self.start_launcher)
        controller.buttonDown.pressed(self.stop_launcher)

    def left_single_auton(self):
        # Move backward and get the back roller
        inertia_sensor.set_heading(90, DEGREES)
        self.start_launcher(100)

        drivetrain.drive_for(REVERSE, 2, INCHES, 50, PERCENT)
        roller.spin(FORWARD)
        wait(0.5, SECONDS)
        roller.stop(COAST)

        # Launch 2 discs into the goal

        drivetrain.drive_for(FORWARD, 7, INCHES, 50, PERCENT)
        drivetrain.turn_to_heading(133, DEGREES)
        drivetrain.drive_for(FORWARD, 70, INCHES, 50, PERCENT)

        drivetrain.turn_to_heading(45, DEGREES)
        self.launch()
        wait(2, SECONDS)
        self.launch()
        wait(2, SECONDS)

    def left_double_auton(self):
        pass

    def right_single_auton(self):
        pass

    def programming_skills(self):
        ROLLER_DISTANCE = 8
        inertia_sensor.set_heading(90, DEGREES)

        # Get the back roller

        drivetrain.drive(REVERSE, 50, PERCENT)
        while True:
            if back_distance_sensor.object_distance(INCHES) < ROLLER_DISTANCE:
                drivetrain.stop(COAST)
                break

        roller.spin(FORWARD)
        wait(0.5, SECONDS)
        roller.stop(COAST)

        # Move towards and get the left roller
        drivetrain.drive_for(FORWARD, 24, INCHES, 50, PERCENT)
        drivetrain.turn_to_heading(180, DEGREES, 25, PERCENT)

        drivetrain.drive(REVERSE, 50, PERCENT)
        while True:
            if back_distance_sensor.object_distance(INCHES) < ROLLER_DISTANCE:
                drivetrain.stop(COAST)
                break

        roller.spin(FORWARD)
        wait(0.5, SECONDS)
        roller.stop(COAST)

        # Move towards the high goal while intaking, and launch discs
        drivetrain.drive_for(FORWARD, 7, INCHES, 50, PERCENT)
        drivetrain.turn_to_heading(130, DEGREES, 25, PERCENT)
        drivetrain.drive_for(FORWARD, 148, INCHES, 60, PERCENT)

        drivetrain.turn_to_heading(270, DEGREES, 25, PERCENT)

        # Move towards and get the top roller
        drivetrain.drive(REVERSE, 50, PERCENT)
        while True:
            if back_distance_sensor.object_distance(INCHES) < ROLLER_DISTANCE:
                drivetrain.stop(COAST)
                break

        roller.spin(FORWARD)
        wait(0.5, SECONDS)
        roller.stop(COAST)

        # Move towards and get the right roller

        drivetrain.drive_for(FORWARD, 24, INCHES, 50, PERCENT)
        drivetrain.turn_to_heading(0, DEGREES, 25, PERCENT)

        drivetrain.drive(REVERSE, 50, PERCENT)
        while True:
            if back_distance_sensor.object_distance(INCHES) < ROLLER_DISTANCE:
                drivetrain.stop(COAST)
                break

        roller.spin(FORWARD)
        wait(0.5, SECONDS)
        roller.stop(COAST)

        pass

    def auton(self):
        start_time = time.time()
        self.autons[self.selected_auton]['action']()
        auton_duration = time.time() - start_time
        print('Auton took {} seconds'.format(auton_duration))

    def select_auton(self):
        if self.selected_auton == len(self.autons) - 1:
            self.selected_auton = 0
        else:
            self.selected_auton += 1

    def start_intake(self):
        intaker.set_velocity(100, PERCENT)
        intaker.spin(FORWARD)

    def stop_intake(self):
        intaker.stop()

    def start_launcher(self, velocity=75):
        launcher.set_velocity(velocity, PERCENT)
        launcher.spin(FORWARD)

    def stop_launcher(self):
        launcher.stop(COAST)

    def launch(self):
        indexer.spin(FORWARD, 100, PERCENT)
        wait(0.35, SECONDS)
        indexer.spin(REVERSE, 100, PERCENT)
        wait(0.35, SECONDS)
        indexer.stop(COAST)

    def start_roller(self, velocity=100):
        roller.set_velocity(velocity, PERCENT)
        roller.spin(FORWARD)

    def stop_roller(self):
        roller.stop()

    def expand(self):
        expansion.set(True)

    def on_controller_changed(self):
        x_power = controller.axis1.position()
        y_power = controller.axis3.position()
        left_velocity = y_power + x_power
        right_velocity = y_power - x_power

        left_wheels.spin(FORWARD, left_velocity, PERCENT)
        right_wheels.spin(FORWARD, right_velocity, PERCENT)

    def update_brain(self):
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.set_font(FontType.MONO30)

        drivetrain_temperature = drivetrain.temperature(PERCENT)
        brain.screen.set_pen_color(drivetrain_temperature >= 70 and Color.RED or Color.GREEN)
        brain.screen.print('Drivetrain: ', round(drivetrain_temperature))
        brain.screen.next_row()

        intaker_temperature = intaker.temperature(PERCENT)
        brain.screen.set_pen_color(intaker_temperature >= 70 and Color.RED or Color.GREEN)
        brain.screen.print('Intake: ', round(intaker_temperature))
        brain.screen.next_row()

        indexer_temperature = indexer.temperature(PERCENT)
        brain.screen.set_pen_color(indexer_temperature >= 70 and Color.RED or Color.GREEN)
        brain.screen.print('Indexer: ', round(indexer_temperature))
        brain.screen.next_row()

        launcher_temperature = launcher.temperature(PERCENT)
        brain.screen.set_pen_color(launcher_temperature >= 70 and Color.RED or Color.GREEN)
        brain.screen.print('Launcher: ', round(launcher_temperature))
        brain.screen.next_row()

        battery = brain.battery.capacity()
        brain.screen.set_pen_color(battery < 20 and Color.RED or Color.GREEN)
        brain.screen.print('Battery: ', round(battery))
        brain.screen.next_row()

        auton = self.autons[self.selected_auton]['name']
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.set_font(FontType.MONO60)
        brain.screen.print(auton)

if __name__ == '__main__':
    robot = Robot()
