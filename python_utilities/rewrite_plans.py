from bs4 import BeautifulSoup
import re

with open('plans/plans-page.html', 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

files = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'pdf' in href or 'zip' in href:
        filename = href.split('/')[-1]
        if filename not in [x['filename'] for x in files]:
            files.append({
                'filename': filename,
                'link': f'../plans_doc/{filename}'
            })

main_container = soup.select_one('.wsite-body-section .wsite-section-elements')

table_html = """
<div style="margin: 20px auto; width: 100%;">
<table style="width: 100%; border-collapse: collapse; text-align: left; font-family: tahoma, sans-serif;">
    <thead>
        <tr style="background-color: #f2f2f2; border-bottom: 2px solid #ddd;">
            <th style="padding: 10px; border: 1px solid #ddd;">File</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Download</th>
            <th style="padding: 10px; border: 1px solid #ddd;">Description / Thumbnail</th>
        </tr>
    </thead>
    <tbody>
"""

for f in files:
    table_html += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 10px; border: 1px solid #ddd;"><b>{f['filename']}</b></td>
            <td style="padding: 10px; border: 1px solid #ddd;"><a href="{f['link']}" style="color: #0066cc; font-weight: bold; text-decoration: none;">Download</a></td>
            <td style="padding: 10px; border: 1px solid #ddd;"><i>Add description or thumbnail here</i></td>
        </tr>
    """

table_html += """
    </tbody>
</table>
</div>
"""

to_decompose = set()

for a in soup.find_all('a', href=True):
    href = a.get('href')
    if href and ('pdf' in href or 'zip' in href):
        parent = a.find_parent('div', class_='wsite-multicol') 
        if parent:
            to_decompose.add(parent)
        else:
            p = a.parent
            while p and p.parent != main_container:
                p = p.parent
            if p and p != soup:
                to_decompose.add(p)

for el in to_decompose:
    el.decompose()

for hr in soup.find_all('hr', style=lambda value: value and 'visibility: hidden' in value):
    hr.decompose()

table_soup = BeautifulSoup(table_html, 'html.parser')
if main_container:
    main_container.append(table_soup)

with open('plans/plans-page.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Rewrite successful")
