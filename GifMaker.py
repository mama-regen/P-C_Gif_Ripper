import imageio, os
import regex as re
from PIL import Image, ImageFilter
import numpy as np

class GifMaker(object):
    _list = {}
    _path = '.'
    _options = {
        'scale': None,
        'blur': None
    }

    def __init__(self, dir: str = '.', scale: int = None, blur: int = None):
        self._options['scale'] = scale
        self._options['blur'] = blur
        self._path = dir.replace("\\", "/").rstrip("/")

    def __getattr__(self, name):
        return self.__getattribute__(f"_{name}_")() if f"_{name}_" in dir(self) else None

    def scan(self):
        for file_name in os.listdir(self._path):
            if not file_name.endswith(".png") or not re.search("f\d", file_name): continue
            name = re.sub(r"\s+", "_", " ".join(re.split(r"f\d+", file_name[:-4]))).rstrip("_")
            if not name in self._list: self._list[name] = []
            self._list[name].append(file_name)
        for name in self._list:
            try: self._list[name].sort(key=lambda f: int(re.search(r"f(\d+)", f).group(1)))
            except: continue

    def generate(self):
        for name, img_list in self._list.items():
            if len(img_list) < 2: continue
            with imageio.get_writer(f"{self._path}/{name}.gif", mode="I") as writer:
                for img in img_list:
                    image = Image.fromarray(imageio.imread(f"{self._path}/{img}"))
                    if self._options['scale']:
                        image = image.resize((image.shape[0] * self._options['scale'], image.shape[1] * self._options['scale']))
                    if self._options['blur']:
                        image = image.filter(ImageFilter.GaussianBlur(self._options['blur']))
                    writer.append_data(np.array(image))

    _list_ = lambda s: [k for k in s._list]
    option = lambda s, n, v = '~': s._options[n] if not type(v).__name__ in ['int', 'float', 'NoneType'] else s._options.__setitem__(n, v)
