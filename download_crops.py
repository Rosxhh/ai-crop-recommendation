import os
import urllib.request

target_dir = r"c:\Users\acer\Desktop\CropYieldProject\crop_project\static\images\crops"
os.makedirs(target_dir, exist_ok=True)

images = {
    "potato.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Patates.jpg/800px-Patates.jpg",
    "groundnut.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Peanuts.jpg/800px-Peanuts.jpg",
    "radish.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Radish_3371103037_1333d102e3_o.jpg/800px-Radish_3371103037_1333d102e3_o.jpg",
    "cucumber.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Cucumber_slices_in_bowl.jpg/800px-Cucumber_slices_in_bowl.jpg"
}

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')]
urllib.request.install_opener(opener)

for name, url in images.items():
    path = os.path.join(target_dir, name)
    print(f"Downloading {name} from {url}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(f"Saved to {path}")
    except Exception as e:
        print(f"Failed to download {name}: {e}")
