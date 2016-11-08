import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings


class TimeStamp(models.Model):
    """An Abstract class which takes care of these 2 time stamp fields in child classes"""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Seller(TimeStamp):
    user = models.ForeignKey(User, related_name='seller')
    phone = models.IntegerField(default=0)

    def __unicode__(self):
        return u"{}".format(self.user)


class Customer(TimeStamp):
    user = models.ForeignKey(User, related_name='customer')
    phone = models.IntegerField(default=0)

    def __unicode__(self):
        return u"{}".format(self.user)


class Item(TimeStamp):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='Slug (Auto Fill)')
    price = models.FloatField(default=0.0)
    inventory = models.IntegerField(default=0)
    seller = models.ForeignKey(Seller, related_name='item')
    image = models.ImageField()  # only single image support

    def __unicode__(self):
        return "{} - {}".format(self.slug, self.price)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
        try:
            super(Item, self).save(*args, **kwargs)
        except:
            self.slug = "{}-{}".format(self.slug, str(self.id))
            super(Item, self).save(*args, **kwargs)


class Order(TimeStamp):
    """Order info"""

    oid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name="Order ID")
    customer = models.ForeignKey(Customer, related_name='order')
    discount = models.FloatField(default=0.0)
    final_price = models.FloatField(default=0.0)  # price after disscount/tax if there is any
    shipping_detail = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "{}".format(self.oid)


class OrderItem(TimeStamp):
    item = models.ForeignKey(Item, related_name='order')
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, related_name='order_item')

    def __unicode__(self):
        return "{} - {}".format(self.item, self.quantity)
