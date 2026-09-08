import glob
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
import re
import os

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def make_relative(url, file_path):
    if not url or url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:', '//', '#')):
        return url
    
    # Calculate depth
    depth = file_path.count(os.sep)
    if depth == 0:
        return url.lstrip('/') if url.startswith('/') else url
    else:
        return ('../' * depth) + url.lstrip('/')

# First, extract the list of links from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

nav_div = soup.find('div', class_='nav desktop-nav')
if not nav_div:
    nav_div = soup.find('ul', class_='wsite-menu-default')

links = []
if nav_div:
    for a in nav_div.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        if text and href and text != '>':
            # Remove any > that might be in the text from weebly arrows
            text = text.replace('>', '').strip()
            links.append((text, href))

# Remove duplicates while preserving order
seen = set()
unique_links = []
for text, href in links:
    if href not in seen:
        seen.add(href)
        unique_links.append((text, href))

print("Found links:")
for t, h in unique_links:
    print(f"- {t}: {h}")

# Now build a simple nav block
def build_nav(file_path):
    nav_html = ['<div class="simple-nav" style="padding: 20px; background: #333; margin-bottom: 20px;">']
    nav_html.append('<ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 15px;">')
    for text, href in unique_links:
        rel_href = make_relative(href, file_path)
        nav_html.append(f'<li><a href="{rel_href}" style="color: white; text-decoration: none;">{text}</a></li>')
    nav_html.append('</ul></div>')
    return '\n'.join(nav_html)

# Replace the nav in all files
html_files = glob.glob('**/*.html', recursive=True)
for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the header or nav wrapper to replace
        # Weebly usually puts the nav in a div with class 'nav-wrap' or 'nav desktop-nav' or 'unite-header'
        header = soup.find('div', class_=re.compile(r'nav-wrap|desktop-nav|unite-header'))
        if not header:
            # Fallback
            header = soup.find('ul', class_=re.compile(r'wsite-menu-default'))
            
        if header:
            # Create our new nav element
            new_nav_soup = BeautifulSoup(build_nav(file_path), 'html.parser')
            header.replace_with(new_nav_soup)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated nav in {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

