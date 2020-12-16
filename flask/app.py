from flask import Flask, Response
import cv2
import numpy as np

app = Flask(__name__)
video = cv2.VideoCapture(0)


@app.route('/')
def index():
    return "Default Message"

def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

        face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
