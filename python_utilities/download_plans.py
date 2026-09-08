import urllib.request
import os

files = [
    "letter_to_go_with_eagle_one_plans.pdf",
    "eagle_one_billofmaterials.pdf",
    "eagle_one_rev_3__1_.pdf",
    "tough_baby.pdf",
    "corplast_wing.pdf",
    "mouse_racer_2.pdf",
    "2016-12.pdf",
    "se5a_mass_fly.pdf",
    "yankeenipper.pdf",
    "0482plan.pdf",
    "general_mills_quick___project_spitfire.pdf",
    "general_mills_quick_project_zero.pdf",
    "fieldstandplans.zip",
    "samurai_2.pdf",
    "gee_bee_cl_sht_1__tiled.pdf",
    "gee_bee_cl_sht_3_tiled.pdf",
    "gee_bee_cl_sht_2_tiled.pdf"
]

base_url = "https://www.circlemasters.com/uploads/9/0/9/8/9098310/"

for f in files:
    url = base_url + f
    dest = os.path.join("plans_doc", f)
    print(f"Downloading {f}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Success: {f}")
    except Exception as e:
        print(f"Failed to download {f}: {e}")

