import time
from PCA9685 import PCA9685
import argparse

class Servo:
    def __init__(self):
        self.PwmServo = PCA9685(0x40, debug=True)
        self.PwmServo.setPWMFreq(50)

    def setServoPwm(self, channel, angle, error=10):
        angle = int(angle)
        if channel == '0':
            self.PwmServo.setServoPulse(8, 2500-int((angle+error)/0.09))
        elif channel == '1':
            self.PwmServo.setServoPulse(9, 500+int((angle+error)/0.09))
        elif channel == '2':
            self.PwmServo.setServoPulse(10, 500+int((angle+error)/0.09))
        elif channel == '3':
            self.PwmServo.setServoPulse(11, 500+int((angle+error)/0.09))
        elif channel == '4':
            self.PwmServo.setServoPulse(12, 500+int((angle+error)/0.09))
        elif channel == '5':
            self.PwmServo.setServoPulse(13, 500+int((angle+error)/0.09))
        elif channel == '6':
            self.PwmServo.setServoPulse(14, 500+int((angle+error)/0.09))
        elif channel == '7':
            self.PwmServo.setServoPulse(15, 500+int((angle+error)/0.09))

    def reset_servo(self):
        self.PwmServo.setServoPulse(8,1500)
        self.PwmServo.setServoPulse(9,1500)

    def initial_position(self):
        self.setServoPwm('0', 90)
        self.setServoPwm('1', 90)
    
    def head_nod(self, step):
        step = max(step, 60)
        step = min(step, 180)
    
        self.setServoPwm('1', step)
    
    def head_shake(self, step):
        step = max(step, 5)
        step = min(step, 175)
    
        self.setServoPwm('0', step)


# Main program logic follows:
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialization", "-I", action="store_true", help="Initialize head")
    parser.add_argument("--reset", "-R", action="store_true", help="Reset Servo")
    parser.add_argument("--nod", "-N", type=int, help="Nodding degree")
    parser.add_argument("--shake", "-S", type=int, help="shaking degree")
    args = parser.parse_args()

    if args.initialization:
        s = Servo()
        s.initial_position()

    if args.reset:
        s = Servo()
        s.reset_servo()

    if args.nod:
        s = Servo()
        s.head_nod(args.nod)

    if args.shake:
        s = Servo()
        s.head_shake(args.shake)
