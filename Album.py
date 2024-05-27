import csv
import glob
import os
import re
from datetime import date, timedelta

from PIL import Image
from pytimeparse.timeparse import timeparse
from werkzeug.utils import secure_filename

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

    def __init__(self, code, released=date(1970, 1, 1), title='', description=''):
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
        return f'{int(total_seconds / 60)}:{total_seconds % 60:02}'


def save_cover(album_code, cover_file):
    file_name, file_extension = os.path.splitext(secure_filename(cover_file.filename))
    file_extension = file_extension.lower()
    file_name = f'static/images/{album_code}_cover{file_extension}'
    cover_file.save(file_name)

    with Image.open(file_name) as image:
        image.thumbnail((220, 220), Image.Resampling.LANCZOS)
        file_name = f'static/images/{album_code}_cover.png'
        image.save(file_name, "PNG")
    file_name = os.path.basename(glob.glob(file_name)[0])
    for path in glob.glob(f'static/images/{album_code}_cover.*'):
        if os.path.basename(path) != file_name:
            try:
                print('remove', path)
                os.remove(path)
            except (PermissionError, IOError):
                pass


def read_tracks(code):
    tracks = []
    for path in glob.glob('data/albums/' + code + '.csv'):
        try:
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


def write_tracks(code, tracks):
    with open('data/albums/' + code + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('title', 'length'))
        for track in tracks:
            writer.writerow((track.title, track.length))


def parse_released(text):
    return date.fromisoformat(text.strip())


def read_discography():
    discography = {}
    for path in glob.glob("data/discography/*.csv"):
        try:
            band_code = os.path.splitext(os.path.basename(path))[0]
            with open(path, encoding='utf-8', newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                discography[band_code] = {}
                for row in reader:
                    try:
                        code = row['code']
                        title = row['name']
                        released = parse_released(row['released'])
                        if code and title:
                            album = Album(code, released, title, row['description'])
                            album.tracks = read_tracks(code)
                            discography[band_code][code] = album
                    except Exception as ex:
                        print(f"${type(ex)}: {ex} path: {path} {row}")

        except Exception as ex:
            print(f"${type(ex)}: {ex} path: {path}")

    return discography


def write_albums(band_code):
    with open('data/discography/' + band_code + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('code', 'released', 'name', 'description'))
        for album in all_discography[band_code].values():
            writer.writerow((album.code, album.released.isoformat(), album.title, album.description))


def save_album(band_code, album):
    if not album.code:
        album.code = generate_album_code(album)
    all_discography[band_code][album.code] = album
    write_tracks(album.code, album.tracks)
    write_albums(band_code)


def get_album(band_code, album_code):
    return all_discography[band_code][album_code]


def has_album_code(album_code):
    for albums in all_discography.values():
        if albums.get(album_code, None) is not None:
            return True
    return False


def generate_album_code(album):
    album_code = re.sub(r'[^a-z0-9]+', '_', album.title.lower())
    counter = 1
    while has_album_code(album_code):
        album_code = album_code + str(++counter)
    return album_code


track_line_regex = re.compile(r'^(\d+)\.\s*(.+)\s+(\d+:\d{2})$')


def parse_tracks(text):
    return [e[1] for e in sorted(
        [(int(match.group(1)), Track(match.group(2), timedelta(seconds=timeparse(match.group(3)))))
         for match in [track_line_regex.fullmatch(line.strip()) for line in text.split('\n')] if match],
        key=lambda e: e[0])]


all_discography = read_discography()
