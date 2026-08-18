import os
import glob
from bs4 import BeautifulSoup
import urllib.parse

def check_case_links():
    html_files = glob.glob('c:/circlemasters/cm_web/*.html')
    case_mismatches = []
    
    # Pre-build a dictionary of lower-case to actual-case paths for all files in uploads
    actual_files = {}
    for root, dirs, files in os.walk('c:/circlemasters/cm_web/uploads'):
        for file in files:
            full_path = os.path.join(root, file).replace('\\', '/')
            actual_files[full_path.lower()] = full_path

    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.startswith('http'):
                    continue
                if 'uploads/' in href or '.pdf' in href:
                    clean_href = href
                    if clean_href.startswith('./'):
                        clean_href = clean_href[2:]
                    elif clean_href.startswith('/'):
                        clean_href = clean_href[1:]
                    
                    decoded_href = urllib.parse.unquote(clean_href)
                    full_path = os.path.join('c:/circlemasters/cm_web', decoded_href).replace('\\', '/')
                    
                    if os.path.exists(full_path):
                        # But is the case correct?
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
