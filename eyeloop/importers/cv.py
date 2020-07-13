from pathlib import Path
from typing import Union

import cv2
import numpy as np

from importers.importer import Importer

class CVImporter(Importer):

    def __init__(self, scale: float, input_dir: Union[Path, str], output_dir: Union[Path, str]) -> None:
        super().__init__(scale=scale, input_dir=input_dir, output_dir=output_dir)

    def first_frame(self) -> None:
        self.path = config.arguments.video

        # load first frame
        if Path(self.path).is_file():  # or stream
            if self.path == "0":
                self.capture = cv2.VideoCapture(0)
            else:
                self.capture = cv2.VideoCapture(self.path)

            self.route_frame = self.route_cam
            width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

            _, image = self.capture.read()
            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            except:
                image = image[..., 0]
        elif Path(self.path).is_dir():

            image = self.read_image(self.frame)

            try:
                height, width, _ = image.shape
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.route_frame = self.route_sequence_sing
            except:
                height, width = image.shape
                self.route_frame = self.route_sequence_flat
        else:
            raise ValueError(f"Could not find impage to import from ")

        self.arm(width, height, image)

    def route(self) -> None:
        self.first_frame()
        try:
            while True:
                self.route_frame()
        except Exception as e:
            print(e)
            print("Importer released.")

    def proceed(self, image) -> None:
        image = self.resize(image)
        image = self.rotate(image, config.engine.angle)
        config.engine.update_feed(image)
        self.save(image)
        self.frame += 1

    def route_sequence_sing(self) -> None:

        image = self.read_image(self.frame)[..., 0]
        self.proceed(image)

    def route_sequence_flat(self) -> None:

        image = self.read_image(self.frame)

        self.proceed(image)

    def route_cam(self) -> None:
        """
        Routes the capture frame to:
        1: eyeloop for online processing
        2: frame save for offline processing
        """

        _, image = self.capture.read()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.proceed(image)

    def release(self) -> None:
        self.route_frame = lambda _: None


