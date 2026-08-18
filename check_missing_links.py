import os
import glob
from bs4 import BeautifulSoup
import urllib.parse

def check_links():
    html_files = glob.glob('c:/circlemasters/cm_web/*.html')
    missing_files = []
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if 'uploads/' in href or '.pdf' in href:
                    # some hrefs might start with './' or '/'
                    # strip off the leading './' or '/'
                    clean_href = href
                    if clean_href.startswith('./'):
                        clean_href = clean_href[2:]
                    elif clean_href.startswith('/'):
                        clean_href = clean_href[1:]
                    
                    decoded_href = urllib.parse.unquote(clean_href)
                    full_path = os.path.join('c:/circlemasters/cm_web', decoded_href)
                    
                    # Also try without decoding just in case
                    raw_full_path = os.path.join('c:/circlemasters/cm_web', clean_href)
                    
                    if not os.path.exists(full_path) and not os.path.exists(raw_full_path):
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
