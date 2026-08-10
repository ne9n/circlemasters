import glob

html_files = glob.glob('**/*.html', recursive=True)
for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add CSS for banners and image galleries
    css_to_add = """
<style>
.wsite-header-section { min-height: 400px; display: flex; flex-direction: column; justify-content: flex-end; }
.wsite-section-bg-image { background-size: cover; background-position: center; }
.imageGallery { display: flex; flex-wrap: wrap; justify-content: center; width: 100%; gap: 10px; }
.galleryImageHolder { height: auto !important; padding: 0 !important; width: 100% !important; }
.galleryInnerImageHolder { position: relative !important; }
.galleryImage { position: relative !important; top: auto !important; left: auto !important; width: 100% !important; max-width: 100%; display: block; margin: 0 auto; }
</style>
</head>
"""
    new_content = content.replace('</head>', css_to_add)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print(f"Updated {len(html_files)} files with new CSS.")
