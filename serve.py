from flask import Flask, request
from PIL import Image
import numpy as np
import hyper as hp
import flask
import json
import io
import utils
import imagenet

# khởi tạo model
global model
model = None 
# Khởi tạo flask application
app = Flask(__name__)
# Khai báo route 1 cho API và method. Rõ hơn thì đây là khai báo đường link
# Nó chính là decorator có tác dụng bổ sung chức năng cho hàm bên dưới
@app.route("/", methods=["GET"])    # nhận dữ liệu từ serve
# Hàm xử lý dữ liệu
def _hello_world(): 
    return "Hello World!"

# Khai báo route 2 cho API
@app.route("/predict", methods=["POST"])
# Khai báo hàm xử lý dữ liệu
def _predict():
    data = {"success": False}

    if request.files.get("image"):
        # lấy ảnh người dùng upload lên
        image = request.files["image"].read()
        # convert ảnh sang array image
        image = Image.open(io.BytesIO(image))
        # resize ảnh
        image_rz = utils._prepocess_image(image, (hp.IMAGE_WIDTH, hp.IMAGE_HEIGHT))

        # dự đoán phân phối xác suất
        dist_probs = model.predict(image_rz)

        # argmax 5
        argmax_k = np.argsort(dist_probs[0])[::-1][:5]

        # classes 5
        classes = [imagenet.classes[idx] for idx in list(argmax_k)]

        # probability of classes
        classes_prob = [dist_probs[0, idx] for idx in list(argmax_k)]

        data["probability"] = dict(zip(classes, classes_prob))

        data["succces"] = True

    return json.dumps(data, ensure_ascii=False, cls=utils.NumpyEncoder)

if __name__ == "__main__":
    print("App run!")
    # load model 
    model = utils._load_model()
    # app.run(debug=False, threaded=False)
    app.run()

# curl -X POST -F image=@test1.jpg 'http://127.0.0.1:5000/predict'

