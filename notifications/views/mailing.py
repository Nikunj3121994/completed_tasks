# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from datetime import date
from post_office import mail
from post_office.models import EmailTemplate
from django.views.generic import TemplateView, FormView, ListView
from django.core.urlresolvers import reverse
from django.conf import settings
from ..models import Mailinglist, EmailMeta
from ..form import MailingImportForm

try:
    from .mixins import AccessMixin
except ImportError:
    AccessMixin = object


logger = logging.getLogger(__name__)


class SimpleStaticView(AccessMixin, TemplateView):

    def get_template_names(self):
        return [self.kwargs.get('template_name') + '.html']


class AuthTemplateView(AccessMixin, TemplateView):
    pass

class ImportMailingView(FormView):
    template_name = 'notifications/import_mailing.html'
    form_class = MailingImportForm

    # def post(self, request, *args, **kwargs):
    #     logger.debug(request.POST)
    #     return super(ImportMailingView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(ImportMailingView, self).form_valid(form)

    def get_success_url(self):
        return reverse('notifications:import_mailing')


    # def form_invalid(self, form):
    #     logger.debug(form.errors)
    #     return super(ImportMailingView, self).form_invalid(form)
    # def get_form_kwargs(self):
    #     """
    #     Возвращает словарь аргументов для экземпляра формы
    #     """
    #     kwargs = {'initial': self.get_initial()}
    #     if self.request.method in ('POST', 'PUT'):
    #         kwargs.update({
    #             'data': self.request.POST,
    #             'files': self.request.FILES,
    #         })
    #     return kwargs
    #
    def get_context_data(self, **kwargs):
        context = super(ImportMailingView, self).get_context_data(**kwargs)

        context['mailing_list'] = Mailinglist.objects.filter(user=self.request.user)
        return context


class MailingStatusView(ListView):
    model = EmailMeta
    context_object_name = 'emails_meta'
    template_name = 'notifications/mailing_status.html'
    paginate_by = 10
    queryset = EmailMeta.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MailingStatusView, self).get_context_data(**kwargs)
        #logger.debug(context)

        context['mailing_list'] = Mailinglist.objects.get(user=self.request.user, pk=self.kwargs.get('pk'))
        return context

    def filter_queryset(self,  queryset):
        return queryset.filter(mailing_list__pk=self.kwargs.get('pk'), mailing_list__user=self.request.user).order_by('-created_at')
        # if not self.request.user.is_authenticated():
        #     return qs.exclude(is_private=True)
        # return qs


"""
#создаем задачу
class InputTaskCreate(AccessMixin, FormView):
    template_name = 'prototype/input/input_task_create.html'
    allow_operator = True
    form_dict = {
        'raster_input': RasterInputForm,
        'sxf_input': SxfInputForm,
        's57_input': S57InputForm,
        'vector_input': VectorInputForm,
        'dem_input': DemInputForm,
        'osm_input': OsmInputForm,
        'external_input': TmsInputForm
    }

    def get_context_data(self, **kwargs):
        context = super(InputTaskCreate, self).get_context_data(**kwargs)
        try:
            context['type_source'] = SourceType.objects.get(code=self.kwargs['type_source'].replace('_input',''))
            context['file_extensions'] = json.dumps(list(SOURCE_FILE_EXTENSIONS.REVERTED_CHOICES_DICT[self.kwargs['type_source'].replace('_input','')]))
        except (KeyError, SourceType.DoesNotExist):
            raise Http404
        return context

    def get(self, request, *args, **kwargs):
        try:
            form = self.form_dict[self.kwargs['type_source']]
        except:
            raise Http404
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form = self.form_dict[self.kwargs['type_source']]
        form = form(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, obj):
        return reverse('protocol:tasks:detail', kwargs={'task_pk': obj.pk})

    def form_valid(self, form, **kwargs):
        task = self.save_task_info(form)
        task.start()
        return redirect(self.get_success_url(task))

    @transaction.atomic
    def save_task_info(self, form, **kwargs):
        #TODO: как-то много хардкодинга

        code_oper = self.kwargs['type_source']
        code_source = code_oper.replace('_input', '')

        source = SourceType.objects.get(code=code_source)
        task = Task(description=form.cleaned_data['description'], user=self.request.user, operation_type = OperationType.objects.get(code=code_oper), src_type_code=source)
        task.save()
        form.save(task=task)
        files = form.cleaned_data['files']
        for f in files:
            sub_task = Subtask(task=task, aux_file_path=f)
            sub_task.save()
        return task




def sending_mail(*args, **kwargs):
    mail.send(
        'chaotism@mail.ru', # List of email addresses also accepted
        'chaotism@mail.ru',
        subject='My email',
        message='Hi there!',
        html_message='Hi <strong>there</strong>!',
    )

    mail.send(
        ['recipient1@example.com'],
        'from@example.com',
        subject='Welcome!',
        message='Welcome home, {{ name }}!',
        html_message='Welcome home, <b>{{ name }}</b>!',
        headers={'Reply-to': 'reply@example.com'},
        scheduled_time=date(2014, 1, 1),
        context={'name': 'Alice'},
    )

    EmailTemplate.objects.create(
        name='morning_greeting',
        subject='Morning, {{ name|capfirst }}',
        content='Hi {{ name }}, how are you feeling today?',
        html_content='Hi <strong>{{ name }}</strong>, how are you feeling today?',
    )

    mail.send(
        ['recipient@example.com'],
        'from@example.com',
        template='morning_greeting',
        context={'name': 'alice'},
    )

    # This will create an email with the following content:
    subject = 'Morning, Alice',
    content = 'Hi alice, how are you feeling today?'
    content = 'Hi <strong>alice</strong>, how are you feeling today?'# Create your views here.
"""