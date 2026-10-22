import os
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageFilter, ImageEnhance

FOLDER_MAPPING = {
    # Apple
    "Apple___Black_rot": "assets/apple_black_rot.jpg",
    "Apple___healthy": "assets/apple_healthy.jpg",
    # Blueberry
    "Blueberry___healthy": "assets/blueberry_healthy.jpg",
    # Cherry
    "Cherry_(including_sour)___healthy": "assets/cherry_healthy.jpg",
    # Corn
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "assets/corn_gray_leaf_spot.jpg",
    "Corn_(maize)___Northern_Leaf_Blight": "assets/corn_northern_blight.jpg",
    "Corn_(maize)___healthy": "assets/corn_healthy.jpg",
    # Grape
    "Grape___Black_rot": "assets/grape_black_rot.jpg",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "assets/grape_leaf_spot.jpg",
    "Grape___healthy": "assets/grape_healthy.jpg",
    # Peach
    "Peach___healthy": "assets/peach_healthy.jpg",
    # Pepper
    "Pepper,_bell___Bacterial_spot": "assets/pepper_bacterial_spot.jpg",
    "Pepper,_bell___healthy": "assets/pepper_healthy.jpg",
    # Potato
    "Potato___Early_blight": "assets/potato_early_blight.jpg",
    "Potato___Late_blight": "assets/potato_late_blight.jpg",
    "Potato___healthy": "assets/potato_healthy.jpg",
    # Raspberry
    "Raspberry___healthy": "assets/raspberry_healthy.jpg",
    # Soybean
    "Soybean___healthy": "assets/soybean_healthy.jpg",
    # Strawberry
    "Strawberry___healthy": "assets/strawberry_healthy.jpg",
    # Tomato
    "Tomato___Bacterial_spot": "assets/tomato_bacterial_spot.jpg",
    "Tomato___Leaf_Mold": "assets/tomato_leaf_mold.jpg",
    "Tomato___Septoria_leaf_spot": "assets/tomato_septoria.jpg",
    "Tomato___Spider_mites Two-spotted_spider_mite": "assets/tomato_spider_mites.jpg",
    "Tomato___Target_Spot": "assets/tomato_target_spot.jpg",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "assets/tomato_yellow_curl.jpg",
    "Tomato___Tomato_mosaic_virus": "assets/tomato_mosaic.jpg",
    "Tomato___healthy": "assets/tomato_healthy.jpg",
}

def enhance_and_save(src_path, dst_path):
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        # Upscale to 512x512 with Lanczos resampling
        up = img.resize((512, 512), Image.Resampling.LANCZOS)
        # Apply subtle sharpening and slight contrast pop
        sharpened = up.filter(ImageFilter.UnsharpMask(radius=1.2, percent=110, threshold=2))
        enhancer = ImageEnhance.Contrast(sharpened)
        enhanced = enhancer.enhance(1.05)
        enhanced.save(dst_path, "JPEG", quality=92)

def main():
    print(f"Starting download and processing for {len(FOLDER_MAPPING)} classes...")
    os.makedirs("assets", exist_ok=True)
    
    for folder, dest in FOLDER_MAPPING.items():
        if os.path.exists(dest):
            print(f"Already exists: {dest}")
            continue
            
        print(f"Fetching listing for {folder}...")
        encoded_folder = urllib.parse.quote(folder)
        api_url = f"https://api.github.com/repos/spMohanty/PlantVillage-Dataset/contents/raw/color/{encoded_folder}"
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        
        try:
            with urllib.request.urlopen(req) as response:
                items = json.loads(response.read())
                if not items:
                    print(f"No items in {folder}")
                    continue
                # Pick 2nd item if available for variety, else 1st
                pick = items[1] if len(items) > 1 else items[0]
                dl_url = pick["download_url"]
                
                temp_file = f"assets/temp_{os.path.basename(dest)}"
                urllib.request.urlretrieve(dl_url, temp_file)
                enhance_and_save(temp_file, dest)
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                print(f"Successfully processed -> {dest}")
        except Exception as e:
            print(f"Error processing {folder}: {e}")

if __name__ == "__main__":
    main()
