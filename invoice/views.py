from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class InvoiceListView(LoginRequiredMixin, TemplateView):
    template_name = "invoice/invoicelist.html"