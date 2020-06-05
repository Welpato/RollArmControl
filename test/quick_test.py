from robot import Robot

servo_min_max_values = {
    0: [10, 170],
    1: [10, 170],
    2: [10, 170],
    3: [100, 180]
}

arduino_port = ''

arduino = Robot(arduino_port, servo_min_max_values, delay_time=1.5)

while True:
    arduino.send_command(0, 10)
    arduino.send_command(0, 170)
    arduino.send_command(1, 170)
    arduino.send_command(1, 90)
    arduino.send_command(2, 90)
    arduino.send_command(2, 170)
    arduino.send_command(3, 100)
    arduino.send_command(3, 180)
