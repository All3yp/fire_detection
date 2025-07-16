# remove corrupt exif data

from PIL import Image

def get_image_files(path):
    """
    Get all image files in the specified path.
    """
    from pathlib import Path
    return list(Path(path).rglob('*.jpg')) + list(Path(path).rglob('*.png'))

file_names = get_image_files(path="datasets4gb/images")

def remove_exif(image_name):
    image = Image.open(image_name)
    if not image.getexif():
        return
    print('removing EXIF from', image_name, '...')
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)

    image_without_exif.save(image_name)

for file in file_names:
    remove_exif(file)
print('done')