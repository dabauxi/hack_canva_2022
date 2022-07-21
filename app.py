import io
import os
import queue
from base64 import encodebytes

from PIL import Image
from flask import Flask, Response, render_template, request, flash, url_for, jsonify
from flask_cors import cross_origin, CORS
from werkzeug.utils import redirect, secure_filename

from camera import VideoCamera

app = Flask(__name__)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = "./uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class FrameBuffer:
    def __init__(self, buffer_size: int):
        self._queue = queue.Queue(maxsize=buffer_size)

    def put(self, frame):
        try:
            self._queue.put(frame, block=False)
        except queue.Full:
            try:
                self._queue.get(block=False)
            except queue.Empty:
                pass
            self._queue.put(frame, block=False)

    def get(self):
        try:
            return self._queue.get(block=False)
        except queue.Empty:
            return None


STATE = {"current_frame": None, "frame_buffer": FrameBuffer(5), "animation_frame": None}


def gen(camera):
    while True:
        frame = camera.get_frame()
        STATE["frame_buffer"].put(frame)
        yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_files = request.files.getlist("file[]")

        #file = request.files['file']
        for file in uploaded_files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    images_dict = {}

    return Response()


@app.route("/test", methods=["GET", "POST"])
@cross_origin()
def upload_images():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploaded-images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_files = request.files.getlist("uploaded-images")

        #file = request.files['file']
        for file in uploaded_files:
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('download_file', name=filename))
    return Response()


@app.route("/video_feed")
def video_feed():
    return Response(
        gen(VideoCamera()), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/picture")
def take_picture():
    with open("current_frame.jpg", "wb") as f:
        f.write(STATE["frame_buffer"].get())
    return render_template("redirect.html")


@app.route("/start")
def start_animate():
    if STATE["animation_frame"] is None:
        STATE["animation_frame"] = STATE["frame_buffer"].get()
    return Response(
        b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + STATE["animation_frame"] + b"\r\n\r\n", mimetype="multipart/x-mixed-replace; boundary=frame"
    )


def get_image(image_path):
    pil_img = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


@app.route("/uploaded-images")
@cross_origin()
def get_uploaded_images():
    images = {"original": [], "modified": []}
    for image_path in os.listdir(UPLOAD_FOLDER):
        images["original"].append(get_image(os.path.join(UPLOAD_FOLDER, image_path)))
    return jsonify(images)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
