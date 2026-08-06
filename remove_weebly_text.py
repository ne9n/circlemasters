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
        
        # Look for any text node containing "powered by" and "weebly"
        for text_node in soup.find_all(string=re.compile(r'powered by.*?weebly', re.IGNORECASE)):
            parent = text_node.parent
            if parent:
                parent.decompose()
                changed = True
        
        # Look for any elements with 'weebly' in the class name or id that look like footers
        for el in soup.find_all(class_=re.compile(r'weebly-footer', re.IGNORECASE)):
            el.decompose()
            changed = True
            
        # Also remove if id has weebly-footer
        for el in soup.find_all(id=re.compile(r'weebly-footer', re.IGNORECASE)):
            el.decompose()
            changed = True
            
        # Let's also remove any a tag with href containing weebly.com just to be safe if it's the footer link
        for a in soup.find_all('a', href=re.compile(r'weebly\.com', re.IGNORECASE)):
            if a.parent and a.parent.name == 'span' or a.parent.name == 'div':
                # if it's just a link we can remove the link
                a.decompose()
                changed = True
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned weebly references from {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
