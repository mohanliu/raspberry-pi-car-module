from flask import Flask, Response, jsonify, render_template, request
import cv2
import numpy as np

app = Flask(__name__)
video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

        face_cascade = cv2.CascadeClassifier(r'static/haarcascade_frontalface_default.xml')

        img = cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img,cv2. COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0 :
            for (x,y,w,h) in faces:
                face_x = float(x+w/2.0)
                face_y = float(y+h/2.0)
                img = cv2.circle(img, (int(face_x), int(face_y)), int((w+h)/4), (0, 255, 0), 2)

        _, new_jpeg = cv2.imencode('.jpg', img)

        frame = new_jpeg.tobytes()
        # frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/_startmovemotor')
def startmovemotor():
    speed = request.args.get("speed", "1000")
    direction = request.args.get("direction", "forward")

    from module import motor
    m = motor.Motor()

    if direction == "forward":
        m.move_forward_start(int(speed))

    if direction == "backward":
        m.move_backward_start(int(speed))

    if direction == "left":
        m.move_left_start(int(speed))

    if direction == "right":
        m.move_right_start(int(speed))

    return jsonify()

@app.route('/_stopmovemotor')
def stopmovemotor():
    from module import motor
    m = motor.Motor()

    m.move_stop()
    
    return jsonify()

@app.route('/_rotatecamera')
def rotatecamera():
    from module import servo

    nod = request.args.get("nod", "90")
    shake = request.args.get("shake", "90")

    s = servo.Servo()

    s.head_nod(int(nod))
    s.head_shake(int(shake))

    return jsonify()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



