import csv
import glob
import os
from datetime import date

from Item import Item


class Album(Item):

    def __init__(self, code, released, title, description=''):
        super().__init__(code, title, description)
        self.released = released

    @property
    def year(self):
        return self.released.year

    @property
    def cover(self):
        paths = glob.glob('static/images/' + self.code + '_cover.*')
        return '/static/images/' + (os.path.basename(paths[0]) if paths else 'no_image.jpg')


def read_discography():
    discography = {}
    for path in glob.glob("data/discography/*.csv"):
        try:
            band = os.path.splitext(os.path.basename(path))[0]
            with open(path, encoding='utf-8', newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                discography[band] = []
                for row in reader:
                    try:
                        code = row['code']
                        title = row['name']
                        released = date.fromisoformat(row['released'])
                        if code and title:
                            album = Album(code, released, title, row['description'])
                            discography[band].append(album)
                            album.cover
                    except Exception as ex:
                        print(f"${type(ex)}: {ex} path: {path} {row}")
        except Exception as ex:
            print(f"${type(ex)}: {ex} path: {path}")

    return discography


all_discography = read_discography()
