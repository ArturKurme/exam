class Page:
    def __init__(self, code, title, href):
        self.code = code
        self.title = title
        self.href = href


all_pages = (
    Page('home', 'Home', '/home'),
    Page('bands', 'Bands', '/bands'),
)


def current_page_title(nav_current):
    return next((page.title for page in all_pages if page.code == nav_current), 'Hello!')
