import os
from PIL import Image, ImageOps, ImageFilter

def process_logo(input_path, output_dir):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} does not exist.")
        return

    # Load image
    img = Image.open(input_path).convert("RGBA")
    
    # Convert to grayscale to analyze brightness
    gray = img.convert("L")
    
    # We want to threshold the image to isolate the handwriting (dark pixels)
    # The background is white (255) and the shadow is light gray (e.g. 200-240)
    # The handwriting is black (0-50)
    # Let's apply a threshold to make it sharp
    threshold = 140
    binary_mask = gray.point(lambda p: 255 if p < threshold else 0)
    
    # Smooth the mask slightly to reduce pixelation, then threshold again for sharpness
    binary_mask = binary_mask.filter(ImageFilter.SMOOTH)
    binary_mask = binary_mask.point(lambda p: 255 if p > 127 else 0)
    
    # Create Dark Version (black text, transparent background)
    dark_img = Image.new("RGBA", img.size, (15, 18, 24, 0)) # Very dark blue-gray (matching portfolio dark mode text, or black)
    # Fill with active color
    for x in range(img.width):
        for y in range(img.height):
            mask_val = binary_mask.getpixel((x, y))
            if mask_val == 255:
                # Set color to dark gray/black #0f172a
                dark_img.putpixel((x, y), (15, 23, 42, 255))
                
    # Create Light/White Version (white text, transparent background)
    light_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    for x in range(img.width):
        for y in range(img.height):
            mask_val = binary_mask.getpixel((x, y))
            if mask_val == 255:
                # Set color to white/light gray #e8eaf0
                light_img.putpixel((x, y), (232, 234, 240, 255))

    # Auto-crop to content bounding box
    bbox = binary_mask.getbbox()
    if bbox:
        dark_cropped = dark_img.crop(bbox)
        light_cropped = light_img.crop(bbox)
        
        # Save images
        os.makedirs(output_dir, exist_ok=True)
        dark_cropped.save(os.path.join(output_dir, "rainysoul_logo_dark.png"), "PNG")
        light_cropped.save(os.path.join(output_dir, "rainysoul_logo_light.png"), "PNG")
        print("Success! Saved cropped transparent logos:")
        print(f"  Dark logo: {os.path.join(output_dir, 'rainysoul_logo_dark.png')}")
        print(f"  Light logo: {os.path.join(output_dir, 'rainysoul_logo_light.png')}")
    else:
        print("Error: Could not detect logo bounding box.")

if __name__ == "__main__":
    input_file = r"C:\Users\PC\.gemini\antigravity-ide\brain\35092537-fde6-477a-9840-52ffd3db53c2\media__1781653767709.jpg"
    output_directory = r"c:\Users\PC\claude-workspace\portfolio\images"
    process_logo(input_file, output_directory)
