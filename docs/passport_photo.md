# Passport/Visa Photo Generator

Generate standard passport and visa photos from existing photos, with automatic background removal and print layout creation. Supports Chinese passport, US passport, and US visa formats.

## Features

- Automatic background removal using AI
- Face detection and positioning
- Standard format support:
  - Chinese passport (33x48mm / 390x567px)
  - US passport / visa (2x2 inches / 600x600px)
- Background color options (defaults match standard requirements)
- Printable 4x6 inch layout with grid of photos for easy splitting

## Requirements

```bash
pip install rembg opencv-python numpy Pillow
```

## Usage

### Generate a single photo (default: Chinese passport):

```bash
python passport_photo.py input.jpg output.jpg
```

### Specify photo type (US passport/visa):

```bash
python passport_photo.py input.jpg output.jpg --type us_passport
python passport_photo.py input.jpg output.jpg --type us_visa
python passport_photo.py input.jpg output.jpg --type cn_passport
```

### With different background colors:

```bash
python passport_photo.py input.jpg output.jpg --color white
python passport_photo.py input.jpg output.jpg --color blue
python passport_photo.py input.jpg output.jpg --color red
```

### Create a printable 4x6 layout:

```bash
python passport_photo.py input.jpg output.jpg --type us_passport --layout
```

This creates a 4x6 inch page at 300 DPI with a grid of passport photos, separated by thin black lines for easy cutting. Size of grid depends on the photo type (6 photos for US, 9 photos for Chinese).

## Output

The photo is generated with:
- Standard dimensions and proportions for the chosen country
- Face positioned according to official requirements
- Appropriate standard background colors

The layout option generates a 1200x1800 pixel image (4x6 inches at 300 DPI) containing as many photos as will fit in a grid.
