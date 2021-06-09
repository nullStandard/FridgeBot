import os
import json


class DarknetYoloWrapper:
    """DarknetYoloWrapper"""

    def __init__(self, network_cfg):
        self.config = dict()
        self.loadNetwork(network_cfg)

    def setDataFile(self, data_):
        self.config.update(data=data_)

    def setCfgFile(self, cfg_):
        self.config.update(cfg=cfg_)

    #refactor
    def setWeights(self, weights_):
        self.config.update(weights=weights_)

    def loadNetwork(self, network_cfg):
        self.setDataFile(network_cfg.get("data"))
        self.setCfgFile(network_cfg.get("cfg"))
        self.setWeights(network_cfg.get("weights"))

    def detect(self):
        os.chdir("./darknet_nnpack")
        print("./darknet detector test {data} {cfg} {weights} ".format(**self.config) +
                  "-ext_output -out result.json < ../taken_image_path.txt")

        with open("predictions.jpg", 'rb') as photo_w_detections:
            os.chdir("../")
            return photo_w_detections.read()

    def extractDetectedClasses(self):
        with open("darknet_nnpack/result.json", 'r') as classes:
            detection_summary = json.load(classes)
            objects_list = detection_summary[0]["objects"]
            unique_classes = set([class_["name"] for class_ in objects_list])
        return unique_classes

    def getAvailableClasses(self):
        os.chdir("darknet_nnpack")
        with open(self.config["data"], 'r') as data:
            for line in data:
                if line.startswith("names"):
                    names_file = line.lstrip("names=")
                    break

        with open(names_file.strip(), 'r') as classes:
            classes_names = [class_.strip() for class_ in classes.readlines()]

        os.chdir("../")
        return classes_names


if __name__ == "__main__":
    dyw = DarknetYoloWrapper()
    print(dyw.detect())
