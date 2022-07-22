import base64
import concurrent.futures
import io
import multiprocessing
import os
import queue
from base64 import encodebytes

import PIL.Image
from PIL import Image
from flask import Flask, Response, render_template, request, flash, jsonify
from flask_cors import cross_origin, CORS
from werkzeug.utils import redirect, secure_filename

from camera import VideoCamera
from triangler.triangulate import generate_del_tri

app = Flask(__name__)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = "./uploads"
TRIANGULATE_FOLDER = "./triangulate"

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


def triangulate(image):
    return generate_del_tri(image)


@app.route("/test", methods=["GET", "POST"])
def upload_images():
    images = []
    uploaded_images = []
    modified = []
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploaded-images' not in request.files:
            flash('No file part')
            return redirect(request.url)

        uploaded_files = request.files.getlist("uploaded-images")

        # file = request.files['file']
        # for file in uploaded_files:
        #     # If the user does not select a file, the browser submits an
        #     # empty file without a filename.
        #     if file.filename == '':
        #         flash('No selected file')
        #         return redirect(request.url)
        #     if file and allowed_file(file.filename):
        #         filename = secure_filename(file.filename)
        #         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(file_path)
        #         #return redirect(url_for('download_file', name=filename))
        #
        #         image = generate_del_tri(file_path)
        #         image.save(os.path.join("./triangulated", filename))
        for file in uploaded_files:
            pass
            file.seek(0)
            image_bytes = file.read()
            uploaded_images.append(image_bytes)

        with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            results = executor.map(triangulate, uploaded_images)
        for result in results:
            byte_arr = io.BytesIO()
            result.save(byte_arr, format='PNG')
            encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
            modified.append(encoded_img)
        for image_bytes in uploaded_images:
            image = PIL.Image.open(io.BytesIO(image_bytes))
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')
            encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
            images.append(encoded_img)
    response = jsonify({"original": images, "modified": modified})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


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


@app.route("/reset")
def reset():
    if os.path.exists(UPLOAD_FOLDER):
        try:
            os.rmdir(UPLOAD_FOLDER)
        except OSError:
            pass
        os.mkdir(UPLOAD_FOLDER)
    if os.path.exists(TRIANGULATE_FOLDER):
        try:
            os.rmdir(TRIANGULATE_FOLDER)
        except OSError:
            pass
        os.mkdir(TRIANGULATE_FOLDER)


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
        file_path = os.path.join(UPLOAD_FOLDER, image_path)
        images["original"].append(get_image(file_path))
        triangulated_path = os.path.join("./triangulated", image_path)
        images["modified"].append(get_image(triangulated_path))
    if len(images["original"]) == len(images["modified"]):
        return jsonify(images)
    else:
        return jsonify({"original": [], "modified": []})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
