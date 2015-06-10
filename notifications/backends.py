#coding: utf-8
from __future__ import unicode_literals, division
from djrill.mail.backends.djrill import DjrillBackend
from models import EmailMeta
from post_office.models import Email


class DjrillBackend_with_save_meta(DjrillBackend):
    def _send(self, message):
        response = super(DjrillBackend_with_save_meta, self)._send(message)
        mandril_response = message.mandrill_response[0]
        post_office_email = Email.objects.filter(to=mandril_response.get('email')).order_by('-last_updated').first()
        #TODO: добавить или if или проверку  post_office_email, сделать более правильную проверку
        email_meta = EmailMeta.objects.create(email=post_office_email,          #TODO: добавить или if или проверку
                               mandrill_id=mandril_response.get('_id'),
                               mandrill_status=mandril_response.get('status'),
                               mandrill_reject_reason=mandril_response.get('reject_reason'))
