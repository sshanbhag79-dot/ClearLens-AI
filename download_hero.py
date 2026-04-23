import requests
import os

def download_image():
    url = "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?q=80&w=1200"
    target_path = "d:/LeedsHack2026/Bio Filter 2.0/frontend/bio_guide_hero.png"
    
    print(f"Downloading image from {url}...")
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded to {target_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")

if __name__ == "__main__":
    download_image()
