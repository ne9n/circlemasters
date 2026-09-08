import os
import glob
from bs4 import BeautifulSoup
import urllib.parse

def check_case_links():
    html_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'html'))
    html_files = []
    for root, dirs, files in os.walk(html_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
                
    case_mismatches = []
    
    # Pre-build a dictionary of lower-case to actual-case paths for all files in html/
    actual_files = {}
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            full_path = os.path.join(root, file).replace('\\', '/')
            actual_files[full_path.lower()] = full_path

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
                        full_path = os.path.normpath(os.path.join(html_dir, decoded_href.lstrip('/'))).replace('\\', '/')
                    else:
                        full_path = os.path.normpath(os.path.join(os.path.dirname(file_path), decoded_href)).replace('\\', '/')
                    
                    if os.path.exists(full_path):
                        lower_full_path = full_path.lower()
                        if lower_full_path in actual_files:
                            actual_case = actual_files[lower_full_path]
                            if actual_case != full_path:
                                case_mismatches.append((file_path, href, full_path, actual_case))

    if not case_mismatches:
        print("No case mismatches found!")
    else:
        print(f"Found {len(case_mismatches)} case mismatches:")
        for doc, href, expected_path, actual_case in case_mismatches:
            print(f"In {os.path.basename(doc)}:")
            print(f"  Href: {href}")
            print(f"  Expected case: {expected_path}")
            print(f"  Actual case:   {actual_case}")

if __name__ == '__main__':
    check_case_links()
