from PIL import Image

def save_photo(in_photo, file_name, size):
    with Image.open(in_photo) as im:
        im.thumbnail(size)
        im.save(file_name)