from flask import Flask, url_for, redirect
from flask import render_template

from Album import all_discography
from Band import all_bands
from Page import current_page_title, all_pages, Page

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def main():
    nav_current = 'home'
    return render_template('main.html',
                           title=current_page_title(nav_current),
                           nav_current=nav_current,
                           nav_items=all_pages)


@app.route("/bands")
def bands():
    nav_current = 'bands'
    return render_template('bands.html',
                           title=current_page_title(nav_current),
                           bands=sorted(all_bands.values(), key=lambda band: band.title),
                           nav_current=nav_current,
                           nav_items=all_pages)


@app.route("/band/<band_code>")
def band_page(band_code):
    try:
        band = all_bands[band_code]
    except KeyError:
        return redirect(url_for('bands'))
    try:
        discography = all_discography[band.code]
    except KeyError:
        discography = []

    return render_template('band_page.html',
                           title=band.title,
                           band=band,
                           discography=sorted(discography, key=lambda album: album.released, reverse=True),
                           nav_current='band',
                           nav_items=all_pages + (Page('band', band.title, '/band/' + band.code),))


@app.route("/album/<band_code>/<album_code>")
def album_page(band_code, album_code):
    try:
        band = all_bands[band_code]
    except KeyError:
        return redirect(url_for('bands'))
    try:
        album = next(a for a in all_discography[band.code] if album_code == a.code)
    except (KeyError, StopIteration):
        return redirect(url_for('band_page', band_code=band_code))

    return render_template('album_page.html',
                           title=album.title,
                           band=band,
                           album=album,
                           nav_current='album',
                           nav_items=all_pages + (Page('band', band.title, '/band/' + band.code),
                                                  Page('album', f'{album.title} ({album.year})',
                                                       '/album/' + band.code + '/' + album_code)))
