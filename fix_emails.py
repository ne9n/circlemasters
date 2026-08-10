import glob
import re
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def decode_cfemail(cfemail):
    email = ""
    k = int(cfemail[:2], 16)
    for i in range(2, len(cfemail)-1, 2):
        email += chr(int(cfemail[i:i+2], 16) ^ k)
    return email

html_files = glob.glob('**/*.html', recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        # Find all a tags with class __cf_email__
        for a in soup.find_all('a', class_='__cf_email__'):
            cfemail = a.get('data-cfemail')
            if cfemail:
                email = decode_cfemail(cfemail)
                # Create a new regular mailto link
                new_a = soup.new_tag('a', href=f"mailto:{email}")
                new_a.string = email
                a.replace_with(new_a)
                changed = True
                print(f"Decoded {email} in {file_path}")
                
        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
