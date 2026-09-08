import glob
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning
import re

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # Remove the mobile-nav
        for nav in soup.find_all('div', class_=re.compile(r'mobile-nav', re.IGNORECASE)):
            nav.decompose()
            changed = True
            
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Removed mobile-nav from {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
