# RollArmControl
This small project has the initial objective to create a simple way 
to control via serial command the arduino RollArm kit from SunFounder.
But it can also easily be adapted to control other arduino servo projects
with just some small adjusts.

## Quick test
Running the `quick_test.py` in the RollArm:
 
1. you just need to upload the `rollarm_control.ino` file to your arduino. 

2. Set the variable `arduino_port` in the `quick_test.py` file 
to be the same as the port which are your arduino.
    - You can find it in the arduino IDE under **Tools->Port**.

3. Install de python requirements.

4. Run the `quick_test.py` file and see your robot dancing.
      
