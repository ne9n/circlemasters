import os
import glob
from bs4 import BeautifulSoup
import urllib.parse

def check_links():
    html_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'html'))
    html_files = []
    for root, dirs, files in os.walk(html_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
                
    missing_files = []
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for tag in soup.find_all(['a', 'img', 'link', 'script', 'video', 'source']):
                for attr in ['href', 'src']:
                    if not tag.has_attr(attr):
                        continue
                    href = tag[attr]
                    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:', 'data:', '//')):
                        continue
                    
                    clean_href = href.split('?')[0].split('#')[0]
                    if not clean_href:
                        continue
                        
                    decoded_href = urllib.parse.unquote(clean_href)
                    if decoded_href.startswith('/'):
                        full_path = os.path.normpath(os.path.join(html_dir, decoded_href.lstrip('/')))
                    else:
                        full_path = os.path.normpath(os.path.join(os.path.dirname(file_path), decoded_href))
                    
                    if not os.path.exists(full_path):
                        missing_files.append((file_path, href, full_path))

    if not missing_files:
        print("All linked upload/pdf files exist!")
    else:
        print(f"Found {len(missing_files)} missing links:")
        for doc, href, expected_path in missing_files:
            print(f"In {os.path.basename(doc)}:")
            print(f"  Href: {href}")
            print(f"  Missing: {expected_path}")

if __name__ == '__main__':
    check_links()
