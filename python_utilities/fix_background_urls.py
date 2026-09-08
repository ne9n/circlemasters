import glob
import os
import re
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

html_files = glob.glob('**/*.html', recursive=True)

def make_relative(url, file_path):
    # Only fix root-relative paths starting with /uploads/
    if url.startswith('/uploads/'):
        # Calculate depth (number of directories in file_path)
        # Using os.path.split to safely count depth
        parts = []
        path = os.path.dirname(file_path)
        while path:
            path, tail = os.path.split(path)
            if tail:
                parts.append(tail)
                
        depth = len(parts)
        if depth == 0:
            return '.' + url
        else:
            return ('../' * depth) + url.lstrip('/')
            
    return url

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # Update inline styles with background-image urls
        for tag in soup.find_all(style=True):
            style = tag['style']
            original_style = style
            
            # Find all url(...) patterns in style
            def replace_url(match):
                full_url = match.group(1)
                # Strip quotes if present
                clean_url = full_url.strip('\'"')
                new_url = make_relative(clean_url, file_path)
                return f'url("{new_url}")'
                
            new_style = re.sub(r'url\(([^)]+)\)', replace_url, style)
            
            if new_style != original_style:
                tag['style'] = new_style
                changed = True
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
