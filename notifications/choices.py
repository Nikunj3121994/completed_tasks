# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from extended_choices import Choices


KEY_TYPES = Choices(
    #('AUTH_KEY', 'key_auth', 'Ключ аутентификации'),
    #('SIGN_KEY', 'key_sign', 'Электронная подпись')

    ('AUTH_KEY', 'auth_key', 'Ключ аутентификации'),
    ('SIGN_KEY', 'sign_key', 'Электронная подпись')
)

IGNORED_FILES_IN_FOLDERS = ('shp')
# TYPE_RASTR_FILES = ('tif', 'tiff', 'shp', 'rsw', 'img', 'jpeg', 'jpg', 'bmp', 'png', 'tab', 'j2k', 'jp2')
# TYPE_SXF_FILES = ('sxf', )
# TYPE_OSM_FILES = ('osm', )
# TYPE_S57_FILES = ('000', )
# TYPE_DEM_FILES = ('tif', 'mtw',  'sxf', '000',)
# TYPE_VECTOR_FILES = ('gdem', 'srtm', 'sxf', 's57')




SOURCE_FILE_EXTENSIONS = Choices(
    ('TYPE_RASTR_FILES', ('tif', 'tiff', 'shp', 'img', 'jp2', 'jpeg', 'jpe', 'jpg', 'bmp', 'png', ), 'raster'),
    ('TYPE_SXF_FILES', ('sxf', ), 'sxf'),
    ('TYPE_S57_FILES', ('000', ), 's57'),
    ('TYPE_OSM_FILES', ('osm', ), 'osm'),
    ('TYPE_DEM_FILES', ('tif', 'tiff', 'mtw', ), 'dem'),
    ('TYPE_VECTOR_FILES', ('gdem', 'srtm', 'sxf', 's57'), 'vector'),
)

