import os
import glob
from bs4 import BeautifulSoup
import re

def main():
    if not os.path.exists('newsletters'):
        os.makedirs('newsletters')
    if not os.path.exists('plans'):
        os.makedirs('plans')
        
    newsletter_files = glob.glob('*newsletter*.html')
    plan_files = ['plans-page.html']
    
    # Ensure they are currently in the root
    newsletter_files = [f for f in newsletter_files if os.path.isfile(f)]
    plan_files = [f for f in plan_files if os.path.isfile(f)]
    
    print("Newsletters to move:", newsletter_files)
    print("Plans to move:", plan_files)
    
    all_html_files = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.html'):
                all_html_files.append(os.path.join(root, f))
                
    # 1. Update links in all HTML files
    for filepath in all_html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        changed = False
        
        for tag in soup.find_all(['a', 'link', 'img', 'script']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    val = tag[attr]
                    
                    for nf in newsletter_files:
                        if val.endswith(nf) and 'newsletters/' not in val:
                            new_val = val.replace(nf, 'newsletters/' + nf)
                            tag[attr] = new_val
                            changed = True
                            
                    for pf in plan_files:
                        if val.endswith(pf) and 'plans/' not in val:
                            new_val = val.replace(pf, 'plans/' + pf)
                            tag[attr] = new_val
                            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
                
    # 2. Process and Move the files
    for nf in newsletter_files:
        if os.path.exists(nf):
            with open(nf, 'r', encoding='utf-8') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all(['a', 'link', 'img', 'script']):
                for attr in ['href', 'src']:
                    if tag.has_attr(attr):
                        val = tag[attr]
                        
                        # Already starts with ../
                        if val.startswith('../'):
                            tag[attr] = '../' + val
                        # Starts with ./
                        elif val.startswith('./'):
                            tag[attr] = '.' + val
                        # Plain relative path without ./
                        elif not val.startswith(('http', '//', 'mailto:', 'tel:', '#')):
                            tag[attr] = '../' + val
            
            with open(os.path.join('newsletters', nf), 'w', encoding='utf-8') as f:
                f.write(str(soup))
            os.remove(nf)
            
    for pf in plan_files:
        if os.path.exists(pf):
            with open(pf, 'r', encoding='utf-8') as f:
                content = f.read()
                
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all(['a', 'link', 'img', 'script']):
                for attr in ['href', 'src']:
                    if tag.has_attr(attr):
                        val = tag[attr]
                        if val.startswith('../'):
                            tag[attr] = '../' + val
                        elif val.startswith('./'):
                            tag[attr] = '.' + val
                        elif not val.startswith(('http', '//', 'mailto:', 'tel:', '#')):
                            tag[attr] = '../' + val
                            
            with open(os.path.join('plans', pf), 'w', encoding='utf-8') as f:
                f.write(str(soup))
            os.remove(pf)
            
main()
