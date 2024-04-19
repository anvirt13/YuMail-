from django.shortcuts import render
from django.core.mail import EmailMessage
from .forms import EmailForm
from django.conf import settings

def send_email(request):
    form = EmailForm(request.POST or None, request.FILES or None)
    message = None  # initialzing with none to ensure it's always defined
    if request.method == 'POST' and form.is_valid():
        from_email = form.cleaned_data['from_email']
        
        if from_email != settings.EMAIL_HOST_USER:
            message = f"Error: The 'From' email must be the same as the account email: {settings.EMAIL_HOST_USER}"
        else:
            to_emails = form.cleaned_data['to_emails'].split(',')
            cc_emails = form.cleaned_data['cc_emails'].split(',') if form.cleaned_data['cc_emails'] else []
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = EmailMessage(subject, message, from_email, to_emails, cc_emails)
            
            for f in request.FILES.getlist('attachment'):
                email.attach(f.name, f.read(), f.content_type)
            
            email.send()
            message = 'Email sent successfully'
            form = EmailForm()  # resets the form after sending

    return render(request, 'email_app/send_email.html', {'form': form, 'message': message})
