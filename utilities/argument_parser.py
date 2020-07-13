import argparse
import os

class Arguments:
    """
    Parses all command-line arguments and config.pupt parameters.
    """

    def __init__(self) -> None:

        parser = argparse.ArgumentParser(description='Help list')
        parser.add_argument("-v","--video", default="0", type=str, help="Input a video sequence for offline processing.")

        parser.add_argument("-d","--destination", default=os.path.dirname(os.path.realpath(__file__))[:-9], type=str, help="Specify output destination.")
        parser.add_argument("-c","--config", default="0", type=str, help="Input a .pupt config file (preset).")
        parser.add_argument("-i","--importer", default="cv", type=str, help="Set import route of stream (cv, vimba, ...)")
        parser.add_argument("-sc","--scale", default=1, type=float, help="Scale the stream (default: 1; 0-1)")
        parser.add_argument("-m","--model", default="ellipsoid", type=str, help="Set pupil model type (circular; ellipsoid = default).")
        parser.add_argument("-ma","--markers", default=0, type=int, help="Enable/disable artifact removing markers (0: disable/default; 1: enable)")
        parser.add_argument("-tr","--tracking", default=1, type=int, help="Enable/disable tracking (1/enabled: default).")

        args = parser.parse_args()

        self.config = args.config

        if self.config != "0": #config file was set.
            self.parse_config(self.config)

        self.markers = args.markers
        self.video = args.video
        self.destination = args.destination
        self.importer = args.importer.lower()
        self.scale = args.scale
        self.tracking = args.tracking
        self.model = args.model.lower()

    def parse_config(self, config:str) -> None:

        try:
            content = open(config, "r")
            print("Loading config preset: ", config)
            for line in content:
                split = line.split("=")
                parameter = split[0]
                parameter = split[1].rstrip("\n").split("\"")

                if len(parameter) != 1:
                    parameter = parameter[1]
                else:
                    parameter = parameter[0]

                if parameter == "video":
                    print("Video preset: ", parameter)
                    self.video = parameter
                elif parameter == "dest":
                    print("Destination preset: ", parameter)
                    self.destination = parameter

                elif parameter == "import":
                    print("Importer preset: ", parameter)
                    self.importer = parameter
                elif parameter == "model":
                    print("Model preset: ", parameter)
                    self.model = parameter
                elif parameter == "markers":
                    print("Markers preset: ", parameter)
                    self.markers = parameter
            print("")

        except Exception as e:
            print("Error opening .pupt config preset.")
            print(e)
