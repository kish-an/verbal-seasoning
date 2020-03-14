import animus_client_py3 as animus_py
import animus_utils as utils
import json
import logging

log = utils.create_logger("AnimusClient", logging.INFO)


def default_audio_params():
    return utils.AudioParams(["alsa"], 16000, 1, 20, True)


def version():
    version_string = animus_py.Version()
    log.info(version_string)
    return version_string


def login_user(username, password):
    log.info("Logging in user")
    aparams = default_audio_params()
    stringparams = json.dumps(aparams._asdict())
    error = animus_py.LoginUser(username, password, stringparams)
    return utils.check_error(error, "Login Success", "Failed to login")


def get_robots(getLocal, getRemote):
    # if not isinstance(geoRange, utils.GeoRange):
    #     log.info("geoRange is not of type utils.GeoRange")
    #     return []
    georange = utils.GeoRange(0, 0, 0, 0)

    json_robots_array = animus_py.GetRobots(getLocal, getRemote, json.dumps(georange._asdict()))
    robot_arr = json.loads(json_robots_array)
    return [utils.RobotDetails(**k) for k in robot_arr]


def close_client_interface():
    log.info("Logging out of Animus")
    animus_py.CloseClientInterface()


class Robot:
    def __init__(self, robot_details):
        self.robot_details = robot_details
        self.robot_id = self.robot_details.ID

    def connect(self):
        log.info("Connecting with robot {}".format(self.robot_details.Name))
        result = animus_py.Connect(json.dumps(self.robot_details._asdict()))
        return result

    def open_modality(self, modality_name):
        log.info("Opening {} modality".format(modality_name))
        if modality_name == "audition" or modality_name=="voice":
            internal = True
        else:
            internal = False

        result = animus_py.OpenModality(self.robot_id, modality_name, internal)
        return result
        # success = "{} modality opened successfully".format(modality_name)
        # fail = "Failed to open {} modality".format(modality_name)
        # return utils.check_error(result, success, fail)

    def set_modality(self, modality_name, sample):
        dtype, frame_settings, data_len, data = utils.validate_encode_data(sample)
        if dtype is not None:
            return animus_py.SetModality(self.robot_id, modality_name, dtype, frame_settings)
        else:
            return False

    def get_modality(self, modality_name):
        jsonData = animus_py.GetModality(self.robot_id, modality_name)
        if jsonData is not None:
            sampledict = json.loads(jsonData)
            if "DataType" in sampledict:
                return utils.decode_data(sampledict["DataType"], jsonData)
            else:
                log.error("json decoding undefined")
                return None
        else:
            return None

    def close_modality(self, modality_name):
        log.info("Closing {} modality".format(modality_name))
        result = animus_py.CloseModality(self.robot_id, modality_name)

        success = "{} modality closed successfully".format(modality_name)
        fail = "Failed to close {} modality".format(modality_name)
        return utils.check_error(result, success, fail)

    def disconnect(self):
        log.info("Disconnecting from {}".format(self.robot_details.Name))
        return animus_py.Disconnect(self.robot_id)
