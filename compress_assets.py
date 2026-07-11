import os
from PIL import Image

def compress_image(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    size_before = os.path.getsize(file_path)
    
    # Don't compress already small files (under 100KB)
    if size_before < 100000:
        return
        
    print(f"Compressing {file_path} ({size_before / 1024 / 1024:.2f} MB)...")
    
    try:
        img = Image.open(file_path)
        
        # If it's a JPEG
        if ext in ['.jpg', '.jpeg']:
            img.save(file_path, 'JPEG', quality=70, optimize=True)
        # If it's a PNG
        elif ext == '.png':
            # If PNG is very large, we can save it with optimization, or convert RGBA to RGB and save
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                # Keep PNG format for transparency
                img.save(file_path, 'PNG', optimize=True)
            else:
                # Convert to RGB and compress as optimized JPEG/PNG
                img = img.convert('RGB')
                img.save(file_path, 'PNG', optimize=True)
                
        size_after = os.path.getsize(file_path)
        print(f"-> Compressed to {size_after / 1024 / 1024:.2f} MB (Saved {(size_before - size_after) / 1024 / 1024:.2f} MB)")
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

def main():
    paths_to_check = [
        "c:/Users/ADMIN/Pictures/Jwel/media/images",
        "c:/Users/ADMIN/Pictures/Jwel/static/images"
    ]
    
    for folder in paths_to_check:
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    compress_image(os.path.join(root, file))

if __name__ == '__main__':
    main()
