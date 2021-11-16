from django import forms
from .models import Invoice, Organization, Customer

class InvoiceForm(forms.ModelForm):
    # organization = forms.ModelMultipleChoiceField(
    # 	queryset=Or.objects.all())

    class Meta:
        model = Invoice
        exclude = ['organization']
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
