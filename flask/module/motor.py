import time
from .PCA9685 import PCA9685
import argparse

class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)
        self.duty_cutoff = 4095
        self.reverse = True

    def _set_duty_range(self, duty):
        if duty > self.duty_cutoff:
            return self.duty_cutoff

        if duty < - self.duty_cutoff:
            return - self.duty_cutoff

        return duty
        
    def left_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(0, 0)
            self.pwm.setMotorPwm(1, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(1, 0)
            self.pwm.setMotorPwm(0, abs(duty))
        else:
            self.pwm.setMotorPwm(0, self.duty_cutoff)
            self.pwm.setMotorPwm(1, self.duty_cutoff)

    def left_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(3, 0)
            self.pwm.setMotorPwm(2, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(2, 0)
            self.pwm.setMotorPwm(3, abs(duty))
        else:
            self.pwm.setMotorPwm(2, self.duty_cutoff)
            self.pwm.setMotorPwm(3, self.duty_cutoff)

    def right_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(6, 0)
            self.pwm.setMotorPwm(7, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(7, 0)
            self.pwm.setMotorPwm(6, abs(duty))
        else:
            self.pwm.setMotorPwm(6, self.duty_cutoff)
            self.pwm.setMotorPwm(7, self.duty_cutoff)

    def right_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(4, 0)
            self.pwm.setMotorPwm(5, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(5, 0)
            self.pwm.setMotorPwm(4, abs(duty))
        else:
            self.pwm.setMotorPwm(4, self.duty_cutoff)
            self.pwm.setMotorPwm(5, self.duty_cutoff)
            
 
    def setMotorModel(self, duty1, duty2, duty3, duty4):

        duty_list = [duty1, duty2, duty3, duty4]

        if self.reverse:
            reverse_flag = -1
        else:
            reverse_flag = 1

        duty_list_ = [self._set_duty_range(d)*reverse_flag for d in duty_list]

        self.left_Upper_Wheel(duty_list_[0])
        self.left_Lower_Wheel(duty_list_[1])
        self.right_Upper_Wheel(duty_list_[2])
        self.right_Lower_Wheel(duty_list_[3])

    def move_forward(self, length, time_):
        self.setMotorModel(length, length, length, length)       
        time.sleep(time_)
        self.setMotorModel(0, 0, 0, 0)                   

    def move_backward(self, length, time_):
        self.setMotorModel(-length, -length, -length, -length)       
        time.sleep(time_)
        self.setMotorModel(0, 0, 0, 0)                   

    def move_left(self, length, time_):
        self.setMotorModel(-500, -500, length, length)      
        time.sleep(time_)
        self.setMotorModel(0, 0, 0, 0)                   

    def move_right(self, length, time_):
        self.setMotorModel(length, length, -500, -500)      
        time.sleep(time_)
        self.setMotorModel(0, 0, 0, 0)                   

    def move_forward_start(self, length):
        self.setMotorModel(length, length, length, length)       

    def move_backward_start(self, length):
        self.setMotorModel(-length, -length, -length, -length)       

    def move_left_start(self, length, _backstep=500):
        self.setMotorModel(-_backstep, -_backstep, length, length)      

    def move_right_start(self, length, _backstep=500):
        self.setMotorModel(length, length, -_backstep, -_backstep)      

    def move_stop(self):
        self.setMotorModel(0, 0, 0, 0)
        
            
PWM = Motor()

def loop(): 
    PWM.setMotorModel(2000, 2000, 2000, 2000)       #Forward
    time.sleep(3)
    PWM.setMotorModel(-2000, -2000, -2000, -2000)   #Back
    time.sleep(3)
    PWM.setMotorModel(-500, -500, 2000, 2000)       #Left 
    time.sleep(3)
    PWM.setMotorModel(2000, 2000, -500, -500)       #Right    
    time.sleep(3)
    PWM.setMotorModel(0, 0, 0, 0)                   #Stop

def destroy():
    PWM.setMotorModel(0, 0, 0, 0)                   

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--forward", "-F", type=int, help="Speed moving forward")
    parser.add_argument("--backward", "-B", type=int, help="Speed moving backward")
    parser.add_argument("--left", "-L", type=int, help="Speed moving left")
    parser.add_argument("--right", "-R", type=int, help="Speed moving right")
    parser.add_argument("--time", "-t", type=float, default=1, help="Moving time")
    args = parser.parse_args()

    try:
        if args.forward:
            m = Motor()
            m.move_forward(args.forward, args.time)
        if args.backward:
            m = Motor()
            m.move_backward(args.backward, args.time)
        if args.left:
            m = Motor()
            m.move_left(args.left, args.time)
        if args.right:
            m = Motor()
            m.move_right(args.right, args.time)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
