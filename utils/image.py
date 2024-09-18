from PIL import Image, ImageFont, ImageDraw

def get_wrapped_text(text: str, font: ImageFont.ImageFont | ImageFont.FreeTypeFont,
                     line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)

def crop_circle(img: Image.Image):
    """Crops an Image to a circle."""
    h, w = img.size
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.pieslice(((0, 0), (w, h)), 0, 360, fill=255)
    transparency = Image.new('RGBA', (w, h), (0,0,0,0))
    return Image.composite(img, transparency, mask)
