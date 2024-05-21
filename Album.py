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
        band = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding='utf-8', newline='') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            discography[band] = []
            for row in reader:
                discography[band].append(Album(row['code'], date.fromisoformat(row['released']), row['name']))
    return discography


all_discography = read_discography()
