# -*- coding: utf-8 -*-

try:
    # Try to import floppyforms
    import floppyforms as forms
except ImportError:
    # If django floppyforms is not installed we use django forms.
    from django import forms


class MailForm(forms.Form):
    """Prepopulated the form using mail params."""

    def __init__(self, *args, **kwargs):
        self._meta = self.Meta

        if hasattr(self._meta, 'initial'):
            kwargs['initial'] = self._meta.initial

        super(MailForm, self).__init__(*args, **kwargs)

        if hasattr(self._meta, 'mail_class'):
            self.mail = self._meta.mail_class
        if 'mail_class' in kwargs:
            self.mail = kwargs.pop('mail_class')

        if hasattr(self, 'mail'):
            # Automatic param creation for not already defined fields
            for param in self.mail.params:
                if param not in self.fields:
                    self.fields[param] = self.get_field_for_param(param)

            self.fields.keyOrder = self.mail.params

    def get_field_for_param(self, param):
        """By default always return a CharField for a param."""
        return forms.CharField()


def mailform_factory(mail_class, form=MailForm):
    """Build a default mail_form from a mail_class."""
    meta = type('Meta', (), {"mail_class": mail_class})
    mailform_class = type('%sMailForm' % mail_class.__name__, (form,),
                          {'Meta': meta})

    return mailform_class
