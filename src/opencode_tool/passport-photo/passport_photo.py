import argparse
import sys
import os
import io

import typing

try:
    import cv2
    import numpy as np
    from PIL import Image
    from rembg import remove
except ImportError:
    cv2 = typing.cast(typing.Any, None)
    np = typing.cast(typing.Any, None)
    Image = typing.cast(typing.Any, None)
    remove = typing.cast(typing.Any, None)

def check_dependencies():
    if None in (cv2, np, Image, remove):
        print("Missing required libraries. Please install them by running:")
        print("pip install rembg opencv-python numpy Pillow")
        sys.exit(1)

def generate_passport_photo(input_path, output_path, bg_color='blue'):
    """Generate a Chinese passport photo (33x48mm / 390x567px) from an input photo."""
    check_dependencies()
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find '{input_path}'")
        sys.exit(1)

    print("1/4 Removing background...")
    with open(input_path, 'rb') as i:
        input_data = i.read()
    subject_data = remove(input_data)
    
    print("2/4 Detecting face...")
    subject_img = Image.open(io.BytesIO(subject_data)).convert("RGBA")
    
    # Convert RGBA to grayscale for face detection
    cv_img = cv2.cvtColor(np.array(subject_img), cv2.COLOR_RGBA2BGRA)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGRA2GRAY)
    
    # Load OpenCV default Haar cascade for face
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        print("Error: Could not detect any faces in the image. Please try a photo with a clearer face.")
        sys.exit(1)
        
    # Get the largest face
    faces = list(faces)
    faces.sort(key=lambda x: float(x[2]) * float(x[3]), reverse=True)
    x, y, w, h = faces[0]
    
    # Approximate top of head (Haar cascade usually bounds the face from forehead to chin)
    top_of_head = max(0, int(y - h * 0.2))
    
    print("3/4 Resizing and cropping...")
    # Chinese Passport Photo standard pixel dimensions
    target_width = 390
    target_height = 567
    
    # Target face width is around 220 pixels
    target_face_width = 220
    scale = target_face_width / float(w)
    
    # Resize the subject according to the scale
    new_size = (int(subject_img.width * scale), int(subject_img.height * scale))
    # Note: Use Image.Resampling.LANCZOS for modern Pillow, Image.LANCZOS for older compatibility
    resample_method = getattr(Image, 'Resampling', Image).LANCZOS
    resized_subject = subject_img.resize(new_size, resample_method)
    
    # Scaled coordinates
    new_x = int(x * scale)
    new_w = int(w * scale)
    new_top_of_head = int(float(top_of_head) * scale)  # type: ignore
    
    # Chinese passport requires about 10-70px from top of image to crown of head (we aim for 40px)
    top_margin = 40
    
    # Calculate crop area relative to the resized subject
    center_x = new_x + new_w // 2
    crop_x1 = center_x - target_width // 2
    crop_y1 = new_top_of_head - top_margin
    
    print("4/4 Generating final image...")
    # Map colors to RGB tuples
    bg_colors = {
        'blue': (67, 142, 219, 255),  # Chinese passport blue #438EDB
        'white': (255, 255, 255, 255),
        'red': (255, 0, 0, 255)
    }
    bg_rgba = bg_colors.get(bg_color.lower(), (255, 255, 255, 255))
    
    # Create final background canvas
    final_img = Image.new("RGBA", (target_width, target_height), bg_rgba)
    
    # Compute the paste coordinates (where to put the resized subject on the background canvas)
    # If crop_x1 is positive, we start pasting from the left edge of the crop box, meaning subject moves left (negative x)
    paste_x = -crop_x1
    paste_y = -crop_y1
    
    # Paste subject onto background (using subject itself as the alpha mask)
    final_img.paste(resized_subject, (paste_x, paste_y), resized_subject)
    
    # Save output
    final_img = final_img.convert("RGB")
    final_img.save(output_path, quality=95)
    print(f"Success! Passport photo saved to {output_path}")


def _draw_horizontal_line(img, y, line_width, line_color, width):
    """Draw a horizontal line on the image."""
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, y, width, y + line_width], fill=line_color)
    return img

def _draw_vertical_line(img, x, line_width, line_color, height):
    """Draw a vertical line on the image."""
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([x, 0, x + line_width, height], fill=line_color)
    return img

def create_print_layout(input_path, output_path):
    """Create a 4x6 inch print layout with multiple passport photos."""
    check_dependencies()
    
    if not os.path.exists(input_path):
        print(f"Error: Could not find '{input_path}'")
        sys.exit(1)
    
    print("Creating print layout...")
    
    # 4x6 inches at 300 DPI
    dpi = 300
    layout_width = int(4 * dpi)  # 1200 pixels
    layout_height = int(6 * dpi)  # 1800 pixels
    
    # Chinese passport photo dimensions (390x567 pixels)
    photo_width = 390
    photo_height = 567
    
    # Calculate how many photos fit
    photos_across = layout_width // photo_width
    photos_down = layout_height // photo_height
    
    total_photos = photos_across * photos_down
    
    # Create blank layout canvas (white background)
    layout_img = Image.new("RGB", (layout_width, layout_height), (255, 255, 255))
    
    # Load the passport photo
    passport_img = Image.open(input_path).convert("RGB")
    
    print(f"Placing {total_photos} passport photos on 4x6 layout...")
    
    # Draw black lines for easy splitting
    line_width = 2
    line_color = (0, 0, 0)
    
    for row in range(photos_down + 1):
        y = row * photo_height
        layout_img = _draw_horizontal_line(layout_img, y, line_width, line_color, layout_width)
    
    for col in range(photos_across + 1):
        x = col * photo_width
        layout_img = _draw_vertical_line(layout_img, x, line_width, line_color, layout_height)
    
    # Place photos in a grid (leaving line_width margin to keep lines visible)
    for row in range(photos_down):
        for col in range(photos_across):
            x = col * photo_width
            y = row * photo_height
            layout_img.paste(passport_img, (x + line_width, y + line_width))
    
    # Redraw lines on top of photos
    for row in range(photos_down + 1):
        y = row * photo_height
        layout_img = _draw_horizontal_line(layout_img, y, line_width, line_color, layout_width)
    
    for col in range(photos_across + 1):
        x = col * photo_width
        layout_img = _draw_vertical_line(layout_img, x, line_width, line_color, layout_height)
    
    # Save layout
    layout_img.save(output_path, quality=95, dpi=(300, 300))
    print(f"Success! Print layout saved to {output_path} ({photos_across}x{photos_down} = {total_photos} photos)")


def main():
    parser = argparse.ArgumentParser(description="Generate a 33x48mm Chinese passport photo from an existing photo.")
    parser.add_argument("input", help="Path to input photo")
    parser.add_argument("output", help="Path to output photo (e.g., output.jpg)")
    parser.add_argument(
        "--color", 
        choices=['blue', 'white', 'red'], 
        default='blue', 
        help="Background color (default: blue)"
    )
    parser.add_argument(
        "--layout",
        action="store_true",
        help="Create a printable 4x6 layout with multiple passport photos"
    )
    
    args = parser.parse_args()
    
    if args.layout:
        create_print_layout(args.input, args.output)
    else:
        generate_passport_photo(args.input, args.output, args.color)

if __name__ == "__main__":
    main()
