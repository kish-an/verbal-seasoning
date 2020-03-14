import json
import logging
import threading
import time
import types
from collections import namedtuple, OrderedDict
import numpy as np
from functools import partial
import cv2
import base64

HEAD_RIGHT = -1.0
HEAD_LEFT = 1.0
HEAD_UP = -1.0
HEAD_DOWN = 1.0
BODY_FORWARD = 1.0
BODY_BACKWARD = -1.0
BODY_LEFT = -1.0
BODY_RIGHT = 1.0
BODY_CLOCKWISE = 1.0
BODY_ANTICLOCKWISE = -1.0


def check_error(err_str, success, fail):
    if err_str == "":
        log.info(success)
        return True
    else:
        log.error(fail + " : " + err_str)
        return False


def create_logger(name, level):
    logger = logging.getLogger(name)
    if not len(logger.handlers):
        formatter = logging.Formatter('[ %(levelname)-5s - {:10} ] %(asctime)s - %(message)s'.format(name))
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        logger.setLevel(level)

    return logger


log = create_logger("AnimusUtils", logging.INFO)
discover_log = create_logger("DiscoverModalities", logging.INFO)
dummy_log = create_logger("DummyModality", logging.INFO)
encode_log = create_logger("Encoder", logging.INFO)

# Connection struct definitions
LocationDetails = namedtuple("LocationDetails", ["ip", "hostname", "city", "region", "country", "loc", "postal", "org"])
RobotDetails = namedtuple("RobotDetails", ["ID", "Make", "Model", "Name", "License", "Location",
                                           "InputModalities", "OutputModalities", "InternalModalities",
                                           "IP", "NetworkMode", "Available", "AudioParams", "DevHash"])
UserDetails = namedtuple("UserDetails", ["ID", "Name", "Location", "RequestedModalities", "InternalModalities"])
GeoRange = namedtuple("GeoRange", ["UpperLat", "LowerLat", "UpperLong", "LowerLong"])
AudioParams = namedtuple("AudioParams", ["Backends", "SampleRate", "Channels", "TransmitRate", "SizeInFrames"])
emotions_list = ["angry", "fear", "sad", "happy", "surprised", "neutral"]
audio_backends = ["alsa", "wasapi", "dsound", "winmm", "pulse", "jack", "coreaudio",
                  "sndio", "audio4", "oss", "opensl", "openal", "sdl"]

# Data struct definitions
ImageSample = namedtuple("ImageSample", ["Data", "DataType", "DataShape", "Format"])
AudioSample = namedtuple("AudioSample", ["Data", "DataType", "Channels", "SampleRate", "NumSamples", "Format"])
StrSample = namedtuple("StrSample", ["DataType", "Data"])
F32ArrSample = namedtuple("F32ArrSample", ["DataType", "Data"])


def get_motor_dict():
    ret = OrderedDict()
    ret["tracking_left_arm"] = -1.0
    ret["tracking_right_arm"] = -1.0
    ret["head_left_right"] = 0.0
    ret["head_up_down"] = 0.0
    ret["head_roll"] = 0.0
    ret["body_forward"] = 0.0
    ret["body_sideways"] = 0.0
    ret["body_rotate"] = 0.0
    return ret


def decode_data(dataType, jsonData):
    if dataType == "floatarray":
        return [float(f) for f in json.loads(jsonData)]

    elif dataType == "string":
        return str(json.loads(jsonData))

    elif dataType == "image":
        image_dict = json.loads(jsonData)
        im = ImageSample(**image_dict)
        npimage = np.frombuffer(base64.b64decode(im.Data), np.uint8).reshape([int(im.DataShape[1] * 3 / 2), im.DataShape[0]])
        npimage = cv2.cvtColor(npimage, cv2.COLOR_YUV2RGB_I420)
        return npimage

    elif dataType == "audio":
        audio_dict = json.loads(jsonData)
        return AudioSample(**audio_dict)
    else:
        encode_log.info("decoding {} datatype unhandled".format(dataType))
        return None


def validate_encode_data(sample):
    if isinstance(sample, list):
        if isinstance(sample[0], float):
            return "floatarray", json.dumps(sample), 0, None
        elif isinstance(sample[0], int):
            return "floatarray", json.dumps([float(f) for f in sample]), 0, None
        else:
            encode_log.error("list of {} data type is unsupported".format(type(sample[0])))
            return None, None, 0, None
    elif isinstance(sample, ImageSample):
        sample_dict = sample._asdict()
        data = sample_dict["Data"]
        sample_dict["Data"] = ""

        return "image", json.dumps(sample_dict), len(data), data
    elif isinstance(sample, AudioSample):
        sample_dict = sample._asdict()
        data = sample_dict["Data"]
        sample_dict["Data"] = ""

        return "audio", json.dumps(sample_dict), len(data), data
    elif isinstance(sample, str):
        return "string", json.dumps(sample), 0, None
    elif isinstance(sample, int):
        return "int64", json.dumps(sample), 0, None
    else:
        encode_log.error("{} data type is unsupported".format(type(sample)))
        return None, None, 0, None


def encode_audio(audio, sample_rate, channels):
    if not isinstance(audio, np.ndarray):
        raise TypeError("Encode audio expects a numpy array object")

    return AudioSample(Data=audio.tostring(),
                       DataType="audio",
                       Channels=channels,
                       SampleRate=sample_rate,
                       NumSamples=int(len(audio) / channels),
                       Format="raw")


# vision receives an rgb image which is turned into yuv
def encode_image(image):
    if not isinstance(image, np.ndarray):
        raise TypeError("Encode audio expects a numpy array object")

    dshape = [image.shape[1], image.shape[0], image.shape[2]]
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV_I420)

    return ImageSample(Data=yuv.tostring(),
                       DataType="image",
                       DataShape=dshape,
                       Format="raw")


def discover_modalities(driver_class):
    method_list = [func for func in dir(driver_class) if
                   callable(getattr(driver_class, func)) and not func.startswith("__")]

    init_modalities = [m.replace("_initialise", "") for m in method_list if "_initialise" in m]
    close_modalities = [m.replace("_close", "") for m in method_list if "_close" in m]
    set_modalities = [m.replace("_set", "") for m in method_list if "_set" in m]
    get_modalities = [m.replace("_get", "") for m in method_list if "_get" in m]

    # After getting lists for init close set and get,
    # find modalities that are present in init, close and get or set.
    modalities_dict = OrderedDict()

    input_modalities = []
    output_modalities = []
    for priority, mod in enumerate(init_modalities):
        if mod in close_modalities:
            if mod in set_modalities:
                modalities_dict[mod] = ["input", priority]
                input_modalities.append(mod)
            elif mod in get_modalities:
                modalities_dict[mod] = ["output", priority]
                output_modalities.append(mod)
            else:
                discover_log.warning("{} Modality incomplete. No set or get method".format(mod))
        else:
            discover_log.warning("{} Modality incomplete. No close method".format(mod))

    return input_modalities, output_modalities


class EmptyHelperClass(object):
    def __init__(self):
        pass


class DummyModality(object):
    def __init__(self, name):
        self.name = name

    def open(self):
        dummy_log.error("{} modality is not implemented for this robot. Cannot open()".format(self.name))
        return False

    def get(self):
        dummy_log.error("{} modality is not implemented for this robot. Cannot get()".format(self.name))
        return None

    def set(self):
        dummy_log.error("{} modality is not implemented for this robot. Cannot set()".format(self.name))
        pass

    def close(self):
        dummy_log.error("{} modality is not implemented for this robot. Cannot close()".format(self.name))
        pass


def check_function(func):
    if isinstance(func, types.MethodType) or isinstance(func, types.FunctionType) or isinstance(func, partial):
        return True
    else:
        return False


class FpsLag:
    def __init__(self, log, modality_name, interval=128):
        self.count = 0
        self.interval = interval
        self.cumulative_lag = 0
        self.fps_startt = time.time()
        self.name = modality_name
        self.log = log
        self.average_fps = 0
        self.average_lag = 0

    def increment(self, send_timestamp=None):
        self.count += 1
        if send_timestamp is not None:
            self.cumulative_lag += time.time() - send_timestamp

        if self.count == self.interval:
            endt = time.time()
            self.average_fps = self.interval / (endt - self.fps_startt)
            if send_timestamp is not None:
                self.average_lag = self.cumulative_lag / self.interval
                self.log.info("{} - {:.2f} fps ------ {:.2f} lag".format(self.name.capitalize(),
                                                                         self.average_fps, self.average_lag))
            else:
                self.log.info("{} - {:.2f} fps ".format(self.name.capitalize(), self.average_fps))

            self.fps_startt = endt
            self.count = 0
            self.cumulative_lag = 0
            return True
        return False


class PeriodicSampler(threading.Thread):
    def __init__(self, name, periodic_function, rate, success_callback=None):

        threading.Thread.__init__(self)
        self._name = name
        self._periodic_function = periodic_function
        self.requested_rate = rate

        if check_function(success_callback):
            self._success_callback = success_callback
        else:
            raise ValueError("Callback must be a function")

        self._result = None
        self._run_flag = True
        self.log = create_logger(name="Sample Loop".format(self._name), level=logging.INFO)
        self.perf = FpsLag(log=self.log, modality_name=self._name, interval=128)

    def run(self):
        rate_delay = 1.0/self.requested_rate

        self.log.info("Started {} sampling loop".format(self._name))

        average_fps = -1
        while self._run_flag:
            time.sleep(rate_delay)

            self._result = self._periodic_function()

            if self._result is not None:
                self._success_callback(self._result, average_fps)
                if self.perf.increment():
                    rate_delay += 1.0 / self.requested_rate - 1.0 / self.perf.average_fps

                    # samp_log.info("{} - {:.2f} fps".format(self._name.capitalize(), average_fps))

                    if rate_delay < 0:
                        rate_delay = 0

        self.log.info("{} sampling loop stopped".format(self._name.capitalize()))

    @property
    def result(self):
        """
        Returns:
            Result of the function.
        """
        return self._result

    def stop(self):
        self._run_flag = False
