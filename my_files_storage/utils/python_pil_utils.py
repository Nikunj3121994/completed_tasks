# coding: utf-8
from __future__ import unicode_literals
import logging
from copy import deepcopy
from cStringIO import StringIO
from PIL import Image, ExifTags
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


logger = logging.getLogger(__name__)


def get_exif_dict(filename):
    result = {}
    try:
        im = Image.open(filename)
        #im.verify()
        exif = im._getexif()

    except (IOError, AttributeError), err:
        logger.error(err)
        return result
    if exif and exif.items():
        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            # print decoded, '->', value
            result[decoded] = value
            #im.close()
    logger.debug(result)
    return result


def rescale(data, width, height, force=True):
    """Rescale the given image, optionally cropping it to make sure the result image has the specified width and height."""

    max_width = width
    max_height = height
    input_file = StringIO(data)
    img = Image.open(input_file)

    if not force:
        logger.debug('not force')
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    else:
        logger.debug('force')
        src_width, src_height = img.size
        src_ratio = float(src_width) / float(src_height)
        dst_width, dst_height = max_width, max_height
        dst_ratio = float(dst_width) / float(dst_height)

        if dst_ratio < src_ratio:
            crop_height = src_height
            crop_width = crop_height * dst_ratio
            x_offset = float(src_width - crop_width) / 2
            y_offset = 0
        else:
            crop_width = src_width
            crop_height = crop_width / dst_ratio
            x_offset = 0
            y_offset = float(src_height - crop_height) / 3
        logger.debug('ready to crop')
        img = img.crop((x_offset, y_offset, x_offset + int(crop_width), y_offset + int(crop_height)))
        logger.debug('croped')
        logger.debug(int(dst_width))
        logger.debug(int(dst_height))
        img = img.resize(100, Image.ANTIALIAS)
        logger.debug('resized')
    logger.debug('tmp')
    tmp = StringIO()
    logger.debug('save')
    img.save(tmp, 'JPEG')
    logger.debug('saved')
    tmp.seek(0)
    logger.debug('seek')
    output_data = tmp.getvalue()
    logger.debug('output_data')
    input_file.close()
    tmp.close()

    return output_data


def get_thumb(instance, source_field, target_field, width, height):
    source = getattr(instance, source_field)
    target = getattr(instance, target_field)
    source.file.seek(0,0)
    img = rescale(source.file.read(), width, height, force=False)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(img)
    img_temp.flush()
    source_image_name = source.file.name.split('/')[-1]
    target_image_name = 'crop_%s'%source_image_name
    target.save(target_image_name, File(img_temp), save=True)
    instance.save()
    return instance