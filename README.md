## Raspberry Pi Car Code Base

> A 4WD smart car kit for Raspberry Pi.

<img src='https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/blob/master/Picture/icon.png' width='30%'/>

This code base is customized from the original Freenove [Repo](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi).

Other useful links includes: 
- [Official tutorial](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/blob/master/Tutorial.pdf)
- [Battery Usage](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/blob/master/About_Battery.pdf)
- [Data Sheets](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/tree/master/Datasheet)

### Raspberry Pi OS setup
- Enable `ssh`
- Enable `I2C`:
  - `sudo raspi-config`
  - "Interfacing Options" -> "P5 I2C"
- Enable Camera:
  - `sudo raspi-config`
  - "Interfacing Options" -> "Camera"
