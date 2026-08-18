from bs4 import BeautifulSoup
import glob
import os

with open('videos.html', 'r', encoding='utf-8') as f:
    soup_vid = BeautifulSoup(f, 'html.parser')

with open('pictures-videos.html', 'r', encoding='utf-8') as f:
    soup_pic = BeautifulSoup(f, 'html.parser')

vid_elements = soup_vid.select_one('.wsite-body-section .wsite-section-elements')
pic_elements = soup_pic.select_one('.wsite-body-section .wsite-section-elements')

if vid_elements and pic_elements:
    pic_elements.append(BeautifulSoup("<div><div style='height: 30px; overflow: hidden; width: 100%;'></div><hr class='styled-hr' style='width:100%;'/><div style='height: 20px; overflow: hidden; width: 100%;'></div></div><h2 class='wsite-content-title' style='text-align:center;'>Videos</h2>", 'html.parser'))
    for child in vid_elements.contents:
        pic_elements.append(child)

with open('pictures-videos.html', 'w', encoding='utf-8') as f:
    f.write(str(soup_pic))

# Remove videos.html from nav menus in all html files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            changed = False
            
            for a in soup.find_all('a', href=True):
                href = a['href']
                if 'videos.html' in href and 'pictures-videos.html' not in href:
                    li = a.find_parent('li')
                    if li:
                        li.decompose()
                        changed = True
                        
            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

print("Done merging")
