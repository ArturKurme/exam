import glob
import json


class Band:

    def __init__(self, file_name):
        with open(file_name) as f:
            obj = json.load(f)
        self.code = obj['code']
        self.title = obj['title']
        self.description = obj['description']

    @property
    def logo(self):
        return 'static/images/' + self.code + '_logo.jpg'


all_bands = {band.code: band for band in [Band(path) for path in glob.glob("data/bands/*.json")]}