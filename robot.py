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
        """
        Sends the command to the arduino via serial
        Please note: the servoId need to be the same set in the rollarm_control.ino file

        :param servo_id:int
        :param value:int
        :return:void
        """
        if bool(self.input_min_max_values):
            value = self.map_values(servo_id, value)
        
        self.arduino.write(f"#{servo_id}%{self.correct_value(servo_id, value)}$".encode())

        time.sleep(self.delay_time)

    def map_values(self, servo_id, value_to_map):
        """
        This function returns the value mapped in the same range as the servo_min_max_values

        :param servo_id:int
        :param value_to_map:int
        :return:int
        """
        # Setting the map range
        input_span = self.input_min_max_values[servo_id][1] - self.input_min_max_values[servo_id][0]
        servo_span = self.servo_min_max_values[servo_id][1] - self.servo_min_max_values[servo_id][0]

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(value_to_map - self.input_min_max_values[servo_id][0]) / input_span
        # Convert the 0-1 range into a value in the right range.
        return int(0 + (value_scaled * servo_span))

    def correct_value(self, servo_id, value_to_check):
        """
        Correct the value to it not be more or lesser then the maximum expected by the servo

        :param servo_id:int
        :param value_to_check:int
        :return: int
        """

        if value_to_check <= self.servo_min_max_values[servo_id][0]:
            value_to_check = self.servo_min_max_values[servo_id][0]
        elif value_to_check >= self.servo_min_max_values[servo_id][1]:
            value_to_check = self.servo_min_max_values[servo_id][1]

        return value_to_check
