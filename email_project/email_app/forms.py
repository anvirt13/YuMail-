from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings 

# sending eail form 
class EmailForm(forms.Form):
    from_email = forms.EmailField(label='From', required=True)
    to_emails = forms.CharField(label='To', required=True)
    cc_emails = forms.CharField(label='CC', required=False, help_text='Separate multiple emails with commas')
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    attachment = forms.FileField(label='Attachment', required=False, widget=forms.ClearableFileInput())

    def clean_from_email(self):
        from_email = self.cleaned_data['from_email']
        if from_email != settings.EMAIL_HOST_USER:
            raise ValidationError(f"The 'From' email is invalid, please try again.")
        return from_email
