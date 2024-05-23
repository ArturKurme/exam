import csv
import glob
import os
from datetime import date, timedelta

from pytimeparse.timeparse import timeparse

from Item import Item


class Track:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    @property
    def length(self):
        total_seconds = int(self.duration.total_seconds())
        return f'{int(total_seconds / 60) % 60}:{total_seconds % 60:02}'


class Album(Item):

    def __init__(self, code, released, title, description=''):
        super().__init__(code, title, description)
        self.released = released
        self.tracks = []

    @property
    def year(self):
        return self.released.year

    @property
    def cover(self):
        paths = glob.glob('static/images/' + self.code + '_cover.*')
        return '/static/images/' + (os.path.basename(paths[0]) if paths else 'no_image.jpg')

    @property
    def duration(self):
        return sum([track.duration for track in self.tracks], start=timedelta(0))

    @property
    def length(self):
        total_seconds = int(self.duration.total_seconds())
        return f'{int(total_seconds / 60) % 60}:{total_seconds % 60:02}'


def read_tracks(code):
    tracks = []
    for path in glob.glob('data/albums/' + code + '.csv'):
        try:
            band = os.path.splitext(os.path.basename(path))[0]
            with open("data/albums/" + code + ".csv", encoding='utf-8', newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                for row in reader:
                    try:
                        duration = timedelta(seconds=timeparse(row['length']))
                        title = row['title']
                        if title and duration:
                            tracks.append(Track(title, duration))
                    except Exception as ex:
                        print(f"${type(ex)}: {ex} path: {path} {row}")
        except Exception as ex:
            print(f"${type(ex)}: {ex} path: {path}")

    return tracks


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
                            album.tracks = read_tracks(code)
                            discography[band].append(album)
                    except Exception as ex:
                        print(f"${type(ex)}: {ex} path: {path} {row}")
        except Exception as ex:
            print(f"${type(ex)}: {ex} path: {path}")

    return discography


all_discography = read_discography()
