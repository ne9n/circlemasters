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
        
        # 1. Strip <font color="...">
        for font in soup.find_all('font'):
            if 'color' in font.attrs:
                del font.attrs['color']
                changed = True
                
        # 2. Strip inline style colors
        for tag in soup.find_all(style=True):
            original_style = tag['style']
            
            # Remove color: ...;
            style = re.sub(r'(?i)(?<!-)\bcolor\s*:[^;]+;?', '', original_style)
            
            # Remove background-color: ...;
            style = re.sub(r'(?i)\bbackground-color\s*:[^;]+;?', '', style)
            
            # Remove background-image: ...;
            style = re.sub(r'(?i)\bbackground-image\s*:[^;]+;?', '', style)
            
            # Remove background: ...;
            style = re.sub(r'(?i)\bbackground\s*:[^;]+;?', '', style)
            
            if style != original_style:
                tag['style'] = style.strip()
                changed = True

        # 3. Clean up wsite-theme-dark class if present
        body = soup.find('body')
        if body and 'class' in body.attrs:
            classes = body['class']
            if 'wsite-theme-dark' in classes:
                classes.remove('wsite-theme-dark')
                body['class'] = classes
                changed = True
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned colors from {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
