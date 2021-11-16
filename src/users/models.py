from typing import Tuple
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager
from address.models import AddressField
from timezone_field import TimeZoneField

class TermsChoices(models.TextChoices):
	DUE_ON_RECIEPT = "DOR","DUE ON RECIEPT"
	NET_15 = "NET15", "NET 15"
	NET_30 = "NET30", "NET 30"
	NET_45 = "NET45", "NET 45"
	NET_60 = "NET60", "NET 60"
	CUSTOM = "CUST", "CUSTOM"


class User(AbstractUser):
	""" custom user model extends from abstract user """

	email = models.EmailField(_('email address'), unique=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	# profile_image = models.ImageField(upload_to='users/profile_images')

	# objects = CustomUserManager()

class Customer(models.Model):
	customer_name = models.CharField(max_length=999)
	customer_email = models.EmailField()
	additional_info = models.JSONField()


class Organization(models.Model):
	# when admin is deleted delete the org
	admin = models.ForeignKey('users.User', on_delete=models.CASCADE)
	staffs = models.ManyToManyField('users.User', related_name="staffs", blank=True)
	logo = models.ImageField(upload_to="org/images")
	address = models.TextField()
	company_id = models.PositiveBigIntegerField(null=True, blank=True)
	buisness_location = models.CharField(max_length=500)
	timezone = TimeZoneField(choices_display='WITH_GMT_OFFSET')
	additional_info = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)


class Invoice(models.Model):
	organization = models.ForeignKey('users.Organization', on_delete=models.CASCADE)
	customer =  models.ForeignKey('users.Customer', on_delete=models.CASCADE)
	# items are reverse related to invoice
	# items = models.ManyToManyField('users.OrderItem')
	invoice_id = models.PositiveIntegerField()
	order_number = models.PositiveIntegerField(null=True, blank=True)
	terms = models.CharField(max_length=400, choices=TermsChoices.choices)# Terms choiceS
	# due_date =  
	subject = models.TextField(null=True, blank=True)
	is_sent = models.BooleanField(default=False)
	is_paid = models.BooleanField(default=False)
	customer_notes = models.TextField(default="Thanks for the buisness", null=True, blank=True)
	terms_and_conditions= models.TextField(null=True, blank=True)

	created_by = models.ForeignKey('users.User', related_name='created_invoices', on_delete=models.CASCADE)
	modified_by = models.ForeignKey('users.User', related_name='modified_invoices', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, editable=False)

	@property
	def get_due_date(self):
		pass

	@property
	def get_subtotal(self):
		# return (self.items.)
		pass

	@property
	def get_tax_total(self) -> Tuple[dict, float]:
		#tax_dict = {item.tax.tax_name:(self.get_subtotal*item.tax.tax_percent) for item in self.items }
		#tax_dict = {tax.tax_name:(self.get_subtotal*tax.tax_percent) for tax in self.items.tax.all() }
		#totaltaxamt = sum(tax_dict.values())
		#return (tax_dict:{'VAT':21, 'GST':33, 'OTHER_TAX':8}, totaltaxamt:62)
		pass

	@property
	def get_total_amount(self):
		pass


class Item(models.Model):
	organization = models.ForeignKey('users.Organization', on_delete=models.CASCADE)
	tax = models.ForeignKey('users.Tax', on_delete=models.CASCADE) 
	title = models.CharField(max_length=255)
	unit_price = models.DecimalField(max_digits=6, decimal_places=2)
	description = models.TextField(null=True, blank=True)
	vat_rate = models.IntegerField(default=0, null=True, blank=True)

class OrderItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='order_items', on_delete=models.CASCADE)
    item =  models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # default will be taken from item, can be updated by the user
    tax = models.ForeignKey('users.Tax', on_delete=models.CASCADE) 
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    vat_rate = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0)
    # excluding vat rate
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)

class Tax(models.Model):
	tax_name = models.CharField(max_length=255)
	tax_percentage = models.PositiveIntegerField(default=0)
	registration_number = models.PositiveIntegerField(default=0)
