import glob
from bs4 import BeautifulSoup
import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

html_files = glob.glob('**/*.html', recursive=True)
count = 0
for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'weebly' in content.lower():
            soup = BeautifulSoup(content, 'html.parser')
            # Let's find any tags that contain "powered by weebly"
            for tag in soup.find_all(string=lambda text: 'powered by' in str(text).lower() and 'weebly' in str(text).lower()):
                print(f"Found in {file_path}: {tag}")
            # Or any divs with class containing weebly
            for div in soup.find_all(class_=lambda c: c and 'weebly' in str(c).lower()):
                print(f"Found class in {file_path}: {div.get('class')}")
            count += 1
            if count > 5:
                break
            
    except Exception as e:
        pass
