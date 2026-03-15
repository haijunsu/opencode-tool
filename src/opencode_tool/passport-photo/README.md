# Passport Photo Generator

Generate Chinese passport photos (33x48mm / 390x567px) from existing photos, with automatic background removal and print layout creation.

## Features

- Automatic background removal using AI
- Face detection and positioning
- Standard Chinese passport photo dimensions (390x567 pixels)
- Background color options: blue (default), white, or red
- Printable 4x6 inch layout with 9 photos for easy splitting

## Requirements

```bash
pip install rembg opencv-python numpy Pillow
```

## Usage

### Generate a single passport photo:

```bash
python passport_photo.py input.jpg output.jpg
```

### With different background colors:

```bash
python passport_photo.py input.jpg output.jpg --color blue
python passport_photo.py input.jpg output.jpg --color white
python passport_photo.py input.jpg output.jpg --color red
```

### Create a printable 4x6 layout (9 photos):

```bash
python passport_photo.py input.jpg output.jpg --layout
```

This creates a 4x6 inch page at 300 DPI with a 3x3 grid of passport photos, separated by thin black lines for easy cutting.

## Output

 passport photo is generated with:
- Dimensions: 390x567 pixels (33x48mm at 300 DPI)
- Face positioned according to Chinese passport requirements
- Optional background colors

The layout option generates a 1200x1800 pixel image (4x6 inches at 300 DPI) containing 9 passport photos in a 3x3 grid.
