from flask import Flask, render_template, Response
import pyautogui
import cv2
import numpy as np

app = Flask(__name__)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width, height = pyautogui.size()

@app.route('/')
def index():
    return render_template('index.html')

def generate():
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
