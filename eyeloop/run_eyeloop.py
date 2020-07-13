import time
from importlib import import_module
from pathlib import Path

import yaml

from engine.engine import Engine
from extractors.DAQ import DAQ_extractor
from extractors.frametimer import FPS_extractor
# sys.path.append('../')
from eyeloop import __version__
from guis.minimum.minimum_gui import GUI
from utilities.argument_parser import Arguments
from utilities.format_print import welcome

CONFIG = yaml.safe_load("config.yaml")

def main():
    """
    EyeLoop is a Python 3-based eye-tracker tailored specifically to dynamic, closed-loop experiments on consumer-grade hardware.
    Lead developer: Simon Arvin
    Git: https://github.com/simonarvin/eyeloop
    """


    welcome(version=__version__, label="Server")
    arguments = Arguments()
    output_dir = Path(arguments.destination, f"{time.strftime('%Y%m%d-%H%M%S')}")
    try:
        print(f"Initiating tracking via {CONFIG['chosen_importer']}")
        importer = import_module("importers", CONFIG["chosen_importer"])
    except ImportError as e:
        msg = (f"Invalid importer '{CONFIG['chosen_importer']}' selected. \n"
               f"Available importers are: {CONFIG['available_importers']}")
        raise ImportError(msg)

    engine = Engine(config=CONFIG, model=arguments.model)
    graphical_user_interface = GUI(engine=engine, importer=importer, markers=arguments.markers)

    fps_counter = FPS_extractor()
    data_acquisition = DAQ_extractor(output_dir)

    extractors = [fps_counter, data_acquisition]
    engine.load_extractors(extractors)





if __name__ == '__main__':
    main()
