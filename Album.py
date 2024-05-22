import csv
import glob
import os
from datetime import date


class Album:
    def __init__(self, code, released, title):
        self.code = code
        self.released = released
        self.title = title

    @property
    def year(self):
        return self.released.year


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
                            album = Album(code, released, title)
                            discography[band].append(album)
                    except Exception as ex:
                        print(f"${type(ex)}: {ex} path: {path} {row}")
        except Exception as ex:
            print(f"${type(ex)}: {ex} path: {path}")

    return discography


all_discography = read_discography()
