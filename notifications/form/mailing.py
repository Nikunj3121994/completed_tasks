# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.admin import widgets
from ..models import Mailinglist
from ..choices import SOURCE_FILE_EXTENSIONS

logger = logging.getLogger(__name__)


class MailingImportForm(forms.ModelForm):

    # def clean_file(self):
    #     file = self.cleaned_data.get('file')
    #     return file
    #
    # def clean(self):
    #     cleaned_data = super(MailingImportForm, self).clean()
    #     raise cleaned_data

    class Meta:
        model = Mailinglist
        exclude = ('shop', 'user')
'''
class InputForm(forms.Form):
    type_files = ()
    ignored_files_for_folders = ()
    files = forms.CharField(label=_('Файлы данных'),
                            widget=Textarea)  #(attrs={'placeholder':'Поддерживаемые форматы файлов для этого типа задачи: %s.'%(','.join(self.type_files))}))
    description = forms.CharField(label=_('Наименование задачи'), widget=Textarea(attrs={
    'placeholder': 'Наименование задачи не более %s знаков' % Task._meta.get_field_by_name('description')[0].max_length,
    'maxlenght': Task._meta.get_field_by_name('description')[0].max_length}), max_length=100)

    # file_folders = ElfinderFormField(optionset='usermaps', start_path=settings.GEODB_INPUT_ZONE_PATH, label='папка с файлами', required=False)


    def clean_files(self):
        error_files = []
        clean_file_list = []
        files = self.cleaned_data.get('files')
        """если кому-то потом придеться это править, то в files я бью строку по , и убираю заведомо стремные строчки
           потом я сталкиваюсь с проблемой раз, что первая часть пути к файлу дублирует, последнию часть корневой папки
           после проблема два загрузка папок, ну и в конце проверка на повторы.
        """
        # files = (os.path.abspath(os.path.join(ROOT_DIR, ('/').join(f.split('/')[1:]))) for f in files.split(',') if len(f.strip()) > 3)
        files = (f.strip() for f in files.split(',') if len(f.strip()) > 3)

        for f in files:
            file_name = ('/').join(f.split('/')[1:])
            if not file_name:
                error_files.append(('Не найден путь "%s".' % f))
                continue
            file_path = os.path.abspath(os.path.join(ROOT_DIR, file_name))
            if not os.path.exists(file_path):
                error_files.append(('Не найден путь "%s".' % f))
                continue
            if not os.path.isfile(file_path) and not os.path.isdir(file_path):
                error_files.append(('Не найден файл данных или папка "%s".' % f.split('/')[-1]))
                continue
            if os.path.isdir(file_path):
                # for file in os.listdir(file_path):
                # if not os.path.isfile(os.path.abspath(os.path.join(os.path.abspath(file_path), file))):
                #     continue
                # if file.split('.')[-1].lower() in self.ignored_files_for_folders:
                #     continue
                # if not file.split('.')[-1].lower() in self.type_files:
                #     continue
                # clean_file_list.append(os.path.abspath(os.path.join(os.path.abspath(file_path), file)))
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        if file.split('.')[-1].lower() in self.ignored_files_for_folders:
                            continue
                        if file.split('.')[-1].lower() in self.type_files:
                            clean_file_list.append(os.path.abspath(os.path.join(root, file)))
                continue

            if self.type_files:
                if f.split('.')[-1].lower() not in self.type_files:
                    error_files.append('Тип файлов "%s" не поддерживается, выберите файл формата %s.' % (
                    f.split('/')[-1], ','.join(self.type_files)))
                    continue
            clean_file_list.append(file_path)
        if error_files:
            raise forms.ValidationError('\n'.join(error_files))
        #TODO: тоже может тормозить
        clean_file_list = list(set(clean_file_list))
        return clean_file_list

    def save(self, commit=True, task=None):
        pass


class RasterInputForm(InputForm):
    check_files = forms.BooleanField(label=_('Проверять наличие изображения в банке данных'), required=False)
    image_type = forms.ChoiceField(label=_('Тип изображения'),
                                   choices=Attribute.objects.get(code='raster_type').get_choices_from_pattern_values,
                                   required=False)
    # type_storage = forms.ChoiceField(label=_('Тип носителя по умолчанию'), choices=Attribute.objects.get(
    #     code='raster_src_type_def').get_choices_from_pattern_values, required=False)
    # type_sensor = forms.ChoiceField(initial='none', label=_('Тип датчика по умолчанию'), choices=Attribute.objects.get(
    #     code='raster_dev_type_def').get_choices_from_pattern_values, required=False)
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_RASTR_FILES
    ignored_files_for_folders = IGNORED_FILES_IN_FOLDERS

    def __init__(self, *args, **kwargs):
        super(RasterInputForm, self).__init__(*args, **kwargs)
        try:
            gdb_mode = settings.GDB_MODE
        except AttributeError:
            gdb_mode = False
        if gdb_mode:
            try:
                del self.fields['check_files']
                del self.fields['image_type']
                del self.fields['type_storage']
                del self.fields['type_sensor']
            except KeyError, err:
                logger.error(err)
                # print 'wrong field %s'%str(err)

    def save(self, commit=True, task=None):
        if self.cleaned_data.get('check_files', ''):
            check_files = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='check_exist'),
                                        value=self.cleaned_data['check_files'])
            check_files.save()
        if self.cleaned_data.get('type_storage', ''):
            type_storage = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_src_type_def'),
                                         value=self.cleaned_data['type_storage'])
            type_storage.save()
        else:
            type_storage = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_src_type_def'),
                                         value=OperationAttribute.objects.get(operation_type='raster_input',
                                                                              code__code='raster_src_type_def').default_value)
            type_storage.save()
        if self.cleaned_data.get('type_sensor', ''):
            type_sensor = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_dev_type_def'),
                                        value=self.cleaned_data['type_sensor'])
            type_sensor.save()
        else:
            type_sensor = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_dev_type_def'),
                                        value=OperationAttribute.objects.get(operation_type='raster_input',
                                                                             code__code='raster_dev_type_def').default_value)
            type_sensor.save()
        if self.cleaned_data.get('image_type', ''):
            type_image = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_type'),
                                       value=self.cleaned_data['image_type'])
            type_image.save()
        else:
            type_image = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='raster_type'),
                                       value=OperationAttribute.objects.get(operation_type='raster_input',
                                                                            code__code='raster_type').default_value)
            type_image.save()



class DemInputForm(InputForm):
    check_files = forms.BooleanField(label=_('Проверять наличие изображения в банке данных'), required=False)
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_DEM_FILES
    image_type = forms.ChoiceField(label=_('Формат'),
                                   choices=Attribute.objects.get(code='dem_format').get_choices_from_pattern_values,
                                   required=False)

    def save(self, commit=True, task=None):
        if self.cleaned_data.get('check_files', ''):
            check_files = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='check_exist'),
                                        value=self.cleaned_data['check_files'])
            check_files.save()
        if self.cleaned_data.get('image_type', ''):
            type_image = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='dem_format'),
                                       value=self.cleaned_data['image_type'])
            type_image.save()
        else:
            type_image = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='dem_format'),
                                       value=OperationAttribute.objects.get(operation_type='dem_input',
                                                                            code__code='dem_format').default_value)
            type_image.save()


class OsmInputForm(InputForm):
    version_time = forms.DateField(label=_('Дата версии'), required=False, initial=datetime.datetime.now())
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_OSM_FILES

    def save(self, commit=True, task=None):
        if self.cleaned_data['version_time']:
            version_time = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='osm_type'),
                                         value=self.cleaned_data['version_time'])
            version_time.save()
        else:
            version_time = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='osm_type'),
                                         value=datetime.datetime.now())
            version_time.save()


class SxfInputForm(InputForm):
    check_files = forms.BooleanField(label=_('Проверять наличие изображения в банке данных'), required=False)
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_SXF_FILES

    def save(self, commit=True, task=None):
        if self.cleaned_data.get('check_files', ''):
            check_files = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='check_exist'),
                                        value=self.cleaned_data['check_files'])
            check_files.save()

class S57InputForm(InputForm):
    check_files = forms.BooleanField(label=_('Проверять наличие изображения в банке данных'), required=False)
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_S57_FILES

    def save(self, commit=True, task=None):
        if self.cleaned_data.get('check_files', ''):
            check_files = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='check_exist'),
                                        value=self.cleaned_data['check_files'])
            check_files.save()

class VectorInputForm(InputForm):
    check_files = forms.BooleanField(label=_('Проверять наличие изображения в банке данных'), required=False)
    type_files = SOURCE_FILE_EXTENSIONS.TYPE_VECTOR_FILES

    def save(self, commit=True, task=None):
        if self.cleaned_data.get('check_files', ''):
            check_files = TaskAttribute(task=task, attr_code=Attribute.objects.get(code='check_exist'),
                                        value=self.cleaned_data['check_files'])
            check_files.save()

class TmsInputForm(InputForm):
    #вынесено пока что в baselayer во вьюху
    pass

'''