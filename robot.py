import time
import serial


class Robot:

    def __init__(self, arduino_port, servo_min_max_values, input_min_max_values=None, baurate=9600, delay_time=1.05):
        if input_min_max_values is None:
            input_min_max_values = {}
        elif len(input_min_max_values) != len(servo_min_max_values):
            raise Exception('servo_min_max_values nad input_min_max_values need to have the same amount of servos!')
        self.servo_min_max_values = servo_min_max_values
        self.input_min_max_values = input_min_max_values
        self.arduino = serial.Serial(arduino_port, baurate)
        self.delay_time = delay_time

    def send_command(self, servo_id, value):
        if bool(self.input_min_max_values):
            value = self.map_values(servo_id, value)
        
        self.arduino.write(f"#{servo_id}%{self.correct_value(servo_id, value)}$".encode())

        time.sleep(self.delay_time)

    def map_values(self, servo_id, value_to_map):
        # Setting the map range
        screen_span = self.input_min_max_values[servo_id][1] - self.input_min_max_values[servo_id][0]
        servo_span = self.input_min_max_values[servo_id][1] - self.input_min_max_values[servo_id][0]

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(value_to_map - self.input_min_max_values[servo_id][0]) / screen_span
        # Convert the 0-1 range into a value in the right range.
        return int(0 + (value_scaled * servo_span))

    def correct_value(self, servo_id, value_to_check):
        if value_to_check <= self.servo_min_max_values[servo_id][0]:
            value_to_check = self.servo_min_max_values[servo_id][0]
        elif value_to_check >= self.servo_min_max_values[servo_id][1]:
            value_to_check = self.servo_min_max_values[servo_id][1]

        return value_to_check
