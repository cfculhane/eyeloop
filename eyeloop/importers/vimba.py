import time
from pathlib import Path
from typing import Union

from pymba import Frame
from pymba import Vimba

from importers.importer import Importer


# For pymba documentation, see:
# https://github.com/morefigs/pymba


class VimbaImporter(Importer):
    def __init__(self, scale: float, input_dir: Union[Path, str], output_dir: Union[Path, str]) -> None:
        super().__init__(scale=scale, input_dir=input_dir, output_dir=output_dir)

    def first_frame(self) -> None:
        # load first frame
        with Vimba() as vimba:
            camera = vimba.camera(0)
            camera.open()
            camera.arm('SingleFrame')
            frame = camera.acquire_frame()
            camera.disarm()

        image = frame.buffer_data_numpy()
        height, width = frame.shape

        self.arm(width, height, image)

    def acquire_frame(self, frame_obj: Frame, angle: float, callback, delay: int = 1) -> None:
        """
        Routes the capture frame to two destinations:
        1: EyeLoop for online processing
        2: frame save for offline processing

        :param frame_obj: The frame object to display.
        :param delay: Display delay in milliseconds, use 0 for indefinite.
        """

        image = frame_obj.buffer_data_numpy()

        # image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

        image = self.rotate(image, angle)

        image = self.resize_image(scale=self.scale, image=image)
        callback(image)
        # config.engine.update_feed(image)
        self.save_image(image, frame=self.frame)

        self.frame += 1

    def release(self) -> None:
        self.live = False

    def route(self) -> None:
        self.first_frame()

        with Vimba() as vimba:
            camera = vimba.camera(0)

            camera.open()

            camera.ExposureTime = 200  # play around with this if exposure is too low
            camera.ExposureAuto = "Off"
            camera.AcquisitionFrameRateMode = 'Basic'

            max_fps = camera.AcquisitionFrameRate
            camera.AcquisitionFrameRate = max_fps

            # arm the camera and provide a function to be called upon frame ready
            camera.arm('Continuous', self.acquire_frame)
            camera.start_frame_acquisition()

            while self.live:
                time.sleep(0.1)

            print("Terminating capture...")

            camera.stop_frame_acquisition()
            camera.disarm()

            camera.close()
