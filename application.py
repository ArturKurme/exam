from flask import Flask
from flask import render_template

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
    band = all_bands[band_code]
    return render_template('band_page.html',
                           title=band.title,
                           band=band,
                           nav_current='band',
                           nav_items=all_pages + (Page('band', band.title, '#'),))
