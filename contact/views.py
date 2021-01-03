from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm
# from .service import send
from .tasks import send_spam_email


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super(ContactView, self).form_valid(form)

