from flask import Flask, url_for, redirect, request
from flask import render_template

from Album import all_discography, get_album, parse_tracks, parse_released, save_cover, save_album, Album
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
        discography = all_discography[band.code].values()
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
        album = get_album(band.code, album_code)
    except KeyError:
        return redirect(url_for('band_page', band_code=band_code))

    return render_template('album_page.html',
                           title=album.title,
                           band=band,
                           album=album,
                           nav_current='album',
                           nav_items=all_pages + (Page('band', band.title, '/band/' + band.code),
                                                  Page('album', f'{album.title} ({album.year})',
                                                       '/album/' + band.code + '/' + album_code)))


@app.route("/edit/<band_code>/")
@app.route("/edit/<band_code>/<album_code>")
def album_edit_page(band_code, album_code=''):
    try:
        band = all_bands[band_code]
    except KeyError:
        return redirect(url_for('bands'))

    try:
        album = get_album(band.code, album_code) if album_code else Album('')
    except KeyError:
        return redirect(url_for('band_page', band_code=band_code))

    return render_template_album_edit(band, album)


@app.route("/save-album", methods=['POST'])
def update_album():
    band_code = request.form['band']
    try:
        band = all_bands[band_code]
    except KeyError:
        return redirect(url_for('bands'))

    album_code = request.form['album']
    album = None
    try:
        if album_code:
            try:
                album = get_album(band_code, album_code)
            except KeyError:
                return redirect(url_for('bands'))
        else:
            album = Album('')

        album.title = request.form['title'].strip()
        album.description = request.form['description'].strip()
        album.released = parse_released(request.form['released'])
        album.tracks = parse_tracks(request.form['tracks'])

        if not album.title:
            raise ValueError('"Title" must not be blank')
        if not album.tracks:
            raise ValueError('At least one track must be specified')

        save_album(band_code, album)

        cover_file = request.files.get('cover', default=None)
        if cover_file:
            save_cover(album.code, cover_file)

        return redirect(url_for('album_page', band_code=band_code, album_code=album.code))
    except Exception as ex:
        print(f"ERROR: ${type(ex)}: {ex}")
        return render_template_album_edit(band, album, error_message=str(ex))


def render_template_album_edit(band, album, error_message=''):
    return render_template('album_edit.html',
                           error_message=error_message,
                           title=f'Edit {album.title}',
                           band=band,
                           album=album,
                           tracks='\n'.join(
                               f'{num}. {track.title} {track.length}' for num, track in
                               enumerate(album.tracks, start=1)),
                           nav_current='',
                           nav_items=all_pages)
