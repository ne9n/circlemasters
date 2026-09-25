import glob, re
import sys

def fix_quotes():
    files = glob.glob('c:/circlemasters/cm_web/html/**/*.html', recursive=True)
    count = 0
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace occurrences like .jpg"" with .jpg"
        new_content = re.sub(r'(\.(jpg|png|svg|pdf|gif|jpeg))\"\"', r'\1"', content, flags=re.IGNORECASE)
        
        if new_content != content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Fixed quotes in {f}')
            count += 1
    
    print(f'Fixed {count} files in total.')

if __name__ == "__main__":
    fix_quotes()
