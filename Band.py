import glob
import json

from Item import Item


class Band(Item):

    def __init__(self, file_name):
        with open(file_name, encoding='utf-8') as f:
            obj = json.load(f)
        super().__init__(obj['code'], obj['title'], obj['description'])

    @property
    def logo(self):
        return '/static/images/' + self.code + '_logo.jpg'


def read_all_bands():
    for path in glob.glob("data/bands/*.json"):
        try:
            yield Band(path)
        except Exception as ex:
            print(f"${type(ex)}: ${ex} path: ${path}")


all_bands = {band.code: band for band in read_all_bands()}
