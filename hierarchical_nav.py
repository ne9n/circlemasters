import glob
import os
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

css = """
<style>
.simple-nav { padding: 10px; background: #222; margin-bottom: 20px; font-family: sans-serif; position: relative; z-index: 1000; }
.simple-nav ul { list-style: none; margin: 0; padding: 0; }
.simple-nav > ul { display: flex; flex-wrap: wrap; gap: 5px; }
.simple-nav li { position: relative; }
.simple-nav a { display: block; padding: 12px 20px; color: #ddd; text-decoration: none; border-radius: 4px; transition: background 0.2s; }
.simple-nav a:hover { background: #444; color: #fff; }
.simple-nav ul ul { display: none; position: absolute; top: 100%; left: 0; background: #333; min-width: 220px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); border-radius: 0 0 4px 4px; overflow: hidden; padding: 0; }
.simple-nav li:hover > ul { display: block; }
.simple-nav ul ul li { width: 100%; border-bottom: 1px solid #444; }
.simple-nav ul ul li:last-child { border-bottom: none; }
.simple-nav ul ul a { padding: 12px 20px; border-radius: 0; }
</style>
"""

hierarchy = [
    ("Home", "./", []),
    ("Club Info", "#", [
        ("About the Club", "./about-the-club.html"),
        ("Membership & Contact", "./membership-and-contact-information.html"),
        ("Administration", "./administration.html"),
        ("Awards", "./awards.html"),
        ("Privacy Policy", "./privacy_policy.html")
    ]),
    ("Locations & Meetings", "#", [
        ("Flying Location", "./flying-location.html"),
        ("Dan Tetzlaff Field Dedication", "./dan-tetzlaff-flying-field-dedication.html"),
        ("Club Meetings", "./club-meetings.html"),
        ("Meetings", "./meetings.html")
    ]),
    ("Newsletters", "#", [
        ("2021 Newsletter", "./2021-club-newsletter.html"),
        ("2020 Newsletter", "./2020-club-newsletter.html"),
        ("2019 Newsletter", "./2019-club-newsletter.html"),
        ("2018 Newsletter", "./2018-club-newsletter.html"),
        ("2017 Newsletter", "./2017-club-newsletter.html"),
        ("2016 Newsletter", "./2016-club-newsletter.html"),
        ("2015 Newsletter", "./2015-club-newsletter.html"),
        ("2014 Newsletters", "./2014-newsletters.html"),
        ("2012-2013 Newsletter", "./2012--2013-newsletter.html"),
        ("2011 Newsletter", "./2011-newsletter.html"),
        ("2010 Newsletter", "./2010-newsletter.html")
    ]),
    ("Control Line Links & Plans", "#", [
        ("Control Line Overview", "./control-line-overview.html"),
        ("Getting Started", "./getting-started.html"),
        ("Wikipedia Page", "http://en.wikipedia.org/wiki/Control_line"),
        ("Tutorials From Brodak", "http://brodak.com/tutorials/"),
        ("Plans Page", "./plans-page.html")
    ]),
    ("Special", "#", [
        ("EAA Kidventure", "./kidventure.html"),
        ("Eagle 1 Airplane Kidventure", "./eagle-1-airplane-kidventure.html"),
        ("Club Contest", "./club-contest.html"),
        ("Building Contest 2019", "./building-contest-2019.html"),
        ("Building Contest 2017", "./building-contest-2017.html"),
        ("Town Of Lisbon Fun Fly", "./town-of-lisbon-fun-fly.html"),
        ("Library Static Show 2014", "./library-static-show-and-open-house-2014.html"),
        ("Steam Show", "./steam-show.html"),
        ("MECA", "./meca.html"),
        ("Pictures & Videos", "./pictures-videos.html"),
        ("Videos", "./videos.html"),
        ("Dave's Blog", "./daves-blog.html"),
        ("Chris's Blog", "./chriss-blog.html")
    ])
]

def make_relative(url, file_path):
    if not url or url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '#')):
        return url
    depth = file_path.count(os.sep)
    if depth == 0:
        return url.lstrip('/') if url.startswith('/') else url
    else:
        return ('../' * depth) + url.lstrip('/')

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        old_nav = soup.find('div', class_='simple-nav')
        if old_nav:
            nav_html = ['<div class="simple-nav">', css, '<ul>']
            
            for top_name, top_href, children in hierarchy:
                top_rel = make_relative(top_href, file_path)
                nav_html.append(f'<li><a href="{top_rel}">{top_name}{" &#9662;" if children else ""}</a>')
                if children:
                    nav_html.append('<ul>')
                    for child_name, child_href in children:
                        child_rel = make_relative(child_href, file_path)
                        nav_html.append(f'<li><a href="{child_rel}">{child_name}</a></li>')
                    nav_html.append('</ul>')
                nav_html.append('</li>')
                
            nav_html.append('</ul></div>')
            new_nav_soup = BeautifulSoup(''.join(nav_html), 'html.parser')
            old_nav.replace_with(new_nav_soup)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

