import os
import random


def photo_path(instance, filename: str) -> str:
    base_filename, file_extension = os.path.splitext(filename)
    chars: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    random_str: str = ''.join((random.choice(chars)) for x in range(10))
    return 'images/{basename}_{randomstring}{ext}'.format(
        basename=base_filename,
        randomstring=random_str,
        ext=file_extension)
