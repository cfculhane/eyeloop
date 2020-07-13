import argparse
from pathlib import Path

EYELOOP_DIR = Path(__file__).parent.parent
PROJECT_DIR = EYELOOP_DIR.parent


class Arguments:
    """
    Parses all command-line arguments and config.pupt parameters.
    """

    def __init__(self) -> None:
        parser = argparse.ArgumentParser(description='Help list')
        parser.add_argument("-v", "--video", default="0", type=str,
                            help="Input a video sequence for offline processing.")
        parser.add_argument("-d", "--destination", default=PROJECT_DIR / "output", type=str,
                            help="Specify output destination.")
        parser.add_argument("-c", "--config", default=str(EYELOOP_DIR.absolute()), type=str,
                            help="Input a .yaml config file (preset).")
        parser.add_argument("-i", "--importer", default="cv", type=str,
                            help="Set import route of stream (cv, vimba, ...)")
        parser.add_argument("-sc", "--scale", default=1, type=float, help="Scale the stream (default: 1; 0-1)")
        parser.add_argument("-m", "--model", default="ellipsoid", type=str,
                            help="Set pupil model type (circular; ellipsoid = default).")
        parser.add_argument("-ma", "--markers", default=0, type=int,
                            help="Enable/disable artifact removing markers (0: disable/default; 1: enable)")
        parser.add_argument("-tr", "--tracking", default=1, type=int,
                            help="Enable/disable tracking (1/enabled: default).")

        args = parser.parse_args()

        self.config = args.config
        self.markers = args.markers
        self.video = args.video
        self.destination = args.destination
        self.importer = args.importer.lower()
        self.scale = args.scale
        self.tracking = args.tracking
        self.model = args.model.lower()
