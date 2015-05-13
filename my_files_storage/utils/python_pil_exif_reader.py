#coding: utf-8
from __future__ import unicode_literals
import logging
from PIL import Image, ExifTags


logger = logging.getLogger(__name__)


def get_exif_dict(filename):
    result = {}
    try:
        im = Image.open(filename)
        im.verify()
        exif = im._getexif()
    except (IOError, AttributeError), err:
        logger.error(err)
        return result
    if exif and exif.items():
        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            # print decoded, '->', value
            result[decoded] = value
    return result

