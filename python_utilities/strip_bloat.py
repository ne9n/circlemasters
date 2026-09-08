import os
import glob
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # Remove all script tags
        scripts = soup.find_all('script')
        if scripts:
            for script in scripts:
                script.decompose()
            changed = True
            
        # Remove all style tags
        styles = soup.find_all('style')
        if styles:
            for style in styles:
                style.decompose()
            changed = True
            
        # Remove all stylesheets
        for link in soup.find_all('link', rel='stylesheet'):
            link.decompose()
            changed = True
            
        # Remove weebly specific tracking/footer stuff
        for div in soup.find_all('div', id='weebly-footer-signup-container-v3'):
            div.decompose()
            changed = True
            
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
