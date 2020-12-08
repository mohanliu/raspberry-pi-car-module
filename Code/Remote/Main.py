#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import os
import io
import time
import imghdr
import sys
from threading import Timer
from threading import Thread
from PIL import Image
from Command import COMMAND as cmd
from Thread import *
from Client_Ui import Ui_Client
from Video import *

class SmartCarRemoteControl():
    def __init__(self, **kwargs):
        self._host = kwargs.get("ip_address", "192.168.2.17")
        self._init_TCP_client()
#         self.TCP = VideoStreaming()
        
        # servos
        
        # motors
        
        # LEDs
        
        # Buzzer
        
        # Video
        
    def _init_TCP_client(self):
        self.client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def sendData(self,s):
        if self.connect_Flag:
            self.client_socket1.send(s.encode('utf-8'))

    def recvData(self):
        data=""
        try:
            data=self.client_socket1.recv(1024).decode('utf-8')
        except:
            pass
        return data

    def socket1_connect(self):
        try:
            self.client_socket1.connect((self._host, 5000))
            self.connect_Flag = True
            print("Connecttion Successful !")
        except Exception as e:
            print("Connect to server Faild!: Server IP is right? Server is opend?")
            self.connect_Flag = False

        
    def on_btn_ForWard(self):
        ForWard=self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+ForWard)

    def on_btn_Turn_Left(self):
        Turn_Left=self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+ Turn_Left)

    def on_btn_BackWard(self):
        BackWard=self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+BackWard)

    def on_btn_Turn_Right(self):
        Turn_Right=self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+Turn_Right)

    def on_btn_Stop(self):
        Stop=self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+Stop)

    def on_btn_video(self):
        if self.Btn_Video.text()=='Open Video':
            self.timer.start(34)
            self.Btn_Video.setText('Close Video')
        elif self.Btn_Video.text()=='Close Video':
            self.timer.stop()
            self.Btn_Video.setText('Open Video')
    def on_btn_Up(self):
        self.servo2=self.servo2+10
        if self.servo2>=180:
            self.servo2=180
        self.VSlider_Servo2.setValue(self.servo2)
        
    def on_btn_Left(self):
        self.servo1=self.servo1-10
        if self.servo1<=0:
            self.servo1=0
        self.HSlider_Servo1.setValue(self.servo1)
    def on_btn_Down(self):
        self.servo2=self.servo2-10
        if self.servo2<=80:
            self.servo2=80
        self.VSlider_Servo2.setValue(self.servo2)
    def on_btn_Right(self):
        self.servo1=self.servo1+10
        if self.servo1>=180:
            self.servo1=180
        self.HSlider_Servo1.setValue(self.servo1)
    def on_btn_Home(self):
        self.servo1=90
        self.servo2=90
        self.HSlider_Servo1.setValue(self.servo1)
        self.VSlider_Servo2.setValue(self.servo2)
    def on_btn_Buzzer(self):
        if self.Btn_Buzzer.text()=='Buzzer':
            self.TCP.sendData(cmd.CMD_BUZZER+self.intervalChar+'1'+self.endChar)
            self.Btn_Buzzer.setText('Noise')
        else:
            self.TCP.sendData(cmd.CMD_BUZZER+self.intervalChar+'0'+self.endChar)
            self.Btn_Buzzer.setText('Buzzer')
    def on_btn_Ultrasonic(self):
        if self.Ultrasonic.text()=="Ultrasonic":
            self.TCP.sendData(cmd.CMD_SONIC+self.intervalChar+'1'+self.endChar)
        else:
            self.TCP.sendData(cmd.CMD_SONIC+self.intervalChar+'0'+self.endChar)
            self.Ultrasonic.setText("Ultrasonic")
 
    def on_btn_Light(self):
        if self.Light.text() == "Light":
            self.TCP.sendData(cmd.CMD_LIGHT+self.intervalChar+'1'+self.endChar)
        else:
            self.TCP.sendData(cmd.CMD_LIGHT+self.intervalChar+'0'+self.endChar)
            self.Light.setText("Light")
        
    def LedChange(self,b):
        R=self.Color_R.text()
        G=self.Color_G.text()
        B=self.Color_B.text()
        led_Off=self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.endChar
        color=self.intervalChar+str(R)+self.intervalChar+str(G)+self.intervalChar+str(B)+self.endChar
        if b.text() == "Led1":
           self.led_Index=str(0x01)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led2":
           self.led_Index=str(0x02)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)              
        if b.text() == "Led3":
           self.led_Index=str(0x04)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led4":
           self.led_Index=str(0x08)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led5":
           self.led_Index=str(0x10)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led6":
           self.led_Index=str(0x20)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led7":
           self.led_Index=str(0x40)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led8":
           self.led_Index=str(0x80)
           if b.isChecked() == True:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+color)
           else:
               self.TCP.sendData(cmd.CMD_LED+self.intervalChar+ self.led_Index+led_Off)
        if b.text() == "Led_Mode1":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'1'+self.endChar)
           else:
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'0'+self.endChar)
        if b.text() == "Led_Mode2":
           if b.isChecked() == True:

               self.checkBox_Led_Mode1.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'2'+self.endChar)
           else:
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'0'+self.endChar)
        if b.text() == "Led_Mode3":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode1.setChecked(False)
               self.checkBox_Led_Mode4.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'3'+self.endChar)
           else:
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'0'+self.endChar)
        if b.text() == "Led_Mode4":
           if b.isChecked() == True:
               self.checkBox_Led_Mode2.setChecked(False)
               self.checkBox_Led_Mode3.setChecked(False)
               self.checkBox_Led_Mode1.setChecked(False)
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'4'+self.endChar)
           else:
               self.TCP.sendData(cmd.CMD_LED_MOD+self.intervalChar+'0'+self.endChar)

 
    def on_btn_Connect(self):
        if self.Btn_Connect.text() == "Connect":
            self.h=self.IP.text()
            self.TCP.StartTcpClient(self.h,)
            try:
                self.streaming=Thread(target=self.TCP.streaming,args=(self.h,))
                self.streaming.start()
            except:
                print ('video error')
            try:
                self.recv=Thread(target=self.recvmassage)
                self.recv.start()
            except:
                print ('recv error')
            self.Btn_Connect.setText( "Disconnect")
            print ('Server address:'+str(self.h)+'\n')
        elif self.Btn_Connect.text()=="Disconnect":
            self.Btn_Connect.setText( "Connect")
            try:
                stop_thread(self.recv)
                stop_thread(self.power)
                stop_thread(self.streaming)
            except:
                pass
            self.TCP.StopTcpcClient()


    def close(self):
        self.timer.stop()
        try:
            stop_thread(self.recv)
            stop_thread(self.streaming)
        except:
            pass
        self.TCP.StopTcpcClient()
        try:
            os.remove("video.jpg")
        except:
            pass
        QCoreApplication.instance().quit()
        os._exit(0)

    def Power(self):
        while True:
            try:
                self.TCP.sendData(cmd.CMD_POWER+self.endChar)
                time.sleep(60)
            except:
                break
    def recvmassage(self):
            self.TCP.socket1_connect(self.h)
            self.power=Thread(target=self.Power)
            self.power.start()
            restCmd=""
            while True:
                Alldata=restCmd+str(self.TCP.recvData())
                restCmd=""
                print (Alldata)
                if Alldata=="":
                    break
                else:
                    cmdArray=Alldata.split("\n")
                    if(cmdArray[-1] != ""):
                        restCmd=cmdArray[-1]
                        cmdArray=cmdArray[:-1]
                for oneCmd in cmdArray:
                    Massage=oneCmd.split("#")
                    if cmd.CMD_SONIC in Massage:
                        self.Ultrasonic.setText('Obstruction:%s cm'%Massage[1])
                    elif cmd.CMD_LIGHT in Massage:
                        self.Light.setText("Left:"+Massage[1]+'V'+' '+"Right:"+Massage[2]+'V')
                    elif cmd. CMD_POWER in Massage:
                        percent_power=int((float(Massage[1])-7)/1.40*100)
                        self.progress_Power.setValue(percent_power) 

    def time(self):
        self.TCP.video_Flag=False
        try:
            if  self.is_valid_jpg('video.jpg'):
                self.label_Video.setPixmap(QPixmap('video.jpg'))
                if self.Btn_Tracking_Faces.text()=="Tracing-Off":
                        self.find_Face(self.TCP.face_x,self.TCP.face_y)
        except Exception as e:
            print(e)
        self.TCP.video_Flag=True
        
            
if __name__ == '__main__':
    t = SmartCarRemoteControl()
    t.socket1_connect()


