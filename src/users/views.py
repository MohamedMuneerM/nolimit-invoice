import json
from typing import List
from django.shortcuts import render
from django.views.generic import FormView, ListView, DetailView
from . import models
from . import forms

class CreateInvoice(FormView):
	""" Create a new invoice under an organization """
	template_name = "create_invoice.html"
	model = models.Invoice
	success_url = "."
	form_class = forms.InvoiceForm

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		"""Insert the form into the context dict."""
		kwargs['customer_form'] = forms.CustomerForm
		return super().get_context_data(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""Handle GET requests: instantiate a blank version of the form."""
		is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
		if is_ajax:
			return render(request, 'create_invoice_form.html', self.get_context_data())
		return super().get(request, *args, **kwargs)


class ListInvoice(ListView):
	""" List all the invoices under an organization """
	template_name = "list_invoice.html"
	model = models.Invoice
	context_object_name = "invoices"


class ViewInvoice(DetailView):
	""" View an invoice under an organization """
	template_name = "view_invoice.html"
	model = models.Invoice
	context_object_name = "invoice"


class CreateCustomer(FormView):
	""" Create a new Customer under an organization """
	template_name = "create_customer.html"
	model = models.Customer
	success_url = "."
	form_class = forms.CustomerForm

	def get_context_data(self, **kwargs):
		"""Insert the form into the context dict."""
		kwargs['customer_form'] = forms.CustomerForm
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		print("form", form)
		print("error")
		return super().form_valid(form)

