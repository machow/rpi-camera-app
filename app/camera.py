from time import time
from datetime import datetime, timezone 
import os


class Settings:
    def __init__(self):
        self.resolution = (1280, 960)
        self.hflip = True
        self.vflip = False

class Camera(object):
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    def __init__(self):
        self.frames = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]
        self.camera = Settings()

    def get_frame(self):
        return self.frames[int(time()) % 3]

    def snapshot(self, _dir=""):
        fname = str(datetime.now(timezone.utc)) + '.jpeg'
        full_fname = os.path.join(_dir, fname)
        stream = self.get_frame()
        with open(full_fname, 'wb') as f: f.write(stream)
        return fname

    def gen(self):
        """Video streaming generator function."""
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @property
    def settings(self):
        attrs = ['resolution', 'hflip', 'vflip']
        camera = self.camera
        return {k: getattr(camera, k) for k in attrs}

    @settings.setter
    def settings(self, d):
        for k, v in d.items(): setattr(self.camera, k, v)
