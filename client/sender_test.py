import logging
import base64
import requests
import timeit
import time
import random
import traceback
from PIL import Image
from io import  BytesIO

def unbuffered_print(p_str):
    print(p_str, flush=True)

class tf_serving_cls():
    def __init__(self):
        self.image_path = 'cat.jpg'


    def data_preprocess(self,data_path, data_version):
        # compress data
        size = int (224 - data_version * 12)
        data_size = (size, size)
        im = Image.open (data_path)
        im = im.resize (data_size, Image.ANTIALIAS)
        image_io = BytesIO ()
        im.save (image_io, 'JPEG')
        byte_data = image_io.getvalue ()
        image_bytes = base64.b64encode (byte_data).decode ('utf-8')
        return image_bytes

    def tf_serving_request(self, url="http://18.139.235.198:8501/v1/models/mobile_dcp_3:classify"):
        data_version = 11
        SERVER_URL = url
        image_bytes = self.data_preprocess (self.image_path, data_version)
        predict_request = '{"signature_name":"serving_default" ,"examples":[{"image/encoded":{"b64": "%s"}}]}' % image_bytes

        start_time = timeit.default_timer()
        response = requests.post (SERVER_URL, data=predict_request)
        response.raise_for_status ()
        prediction = response.json ()['results'][0]

        end_time = timeit.default_timer ()
        latency = end_time-start_time

        print('Prediction class: %s, avg latency: %.2f ms'%(prediction[0][0],latency*1000))

        return

tf_serving_cls().tf_serving_request()
