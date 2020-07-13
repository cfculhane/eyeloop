from pathlib import Path
from typing import Union

import cv2
import numpy as np
from math import isclose

from utilities.general_operations import tuple_int


class Importer:

    def __init__(self, scale: float, input_dir: Union[Path, str], output_dir: Union[Path, str]):
        self.live = True
        self.scale = scale
        self.frame = 0
        self.input_dir: input_dir
        self.output_dir: output_dir

        self.center = None
        self.dimensions = None


    # TODO which of these arm methods is the correct one?
    # def arm(self, width, height, image):
    #     self.frame = 0

    def arm(self, width, height, image):

        self.dimensions = tuple_int((width * self.scale, height * self.scale))

        width, height = self.dimensions

        self.center = (width // 2, height // 2)

        self.resize_image(scale=self.scale, image=image)

        # image = self.rotate(image, self.ENGINE.angle)
        config.engine.arm(width, height, image)

    def rotate(self, image: np.ndarray, angle: float) -> np.ndarray:
        """
        Performs rotaiton of the image to align visual axes.
        """

        if angle == 0:
            return image

        M = cv2.getRotationMatrix2D(self.center, angle, 1)

        return cv2.warpAffine(image, M, self.dimensions)

    @staticmethod
    def resize_image(scale: float, image: np.ndarray) -> np.ndarray:
        """
        Resizes image to scale value. -sc 1 (default)
        """
        if isclose(scale, 1, rel_tol=1E-09):
            return image
        else:
            return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST)

    def save_image(self, image: np.ndarray, frame: int) -> None:
        """
        Saves video sequence to new folderpath.
        """

        out_path = Path(self.output_dir,  f"frame_{frame}.jpg")
        cv2.imwrite(str(out_path.absolute()), image)

    def read_image(self, frame: int) -> np.ndarray:
        """
        Reads video sequence from the input folderpath.
        Command-line argument -v [dir] sets this path.
        """
        in_path = Path(self.input_dir,  f"pic{frame}.jpg")

        return np.array(cv2.imread(str(in_path.absolute())))
