from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from colorfield.fields import ColorField
from django.utils.html import format_html, mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Size(models.Model):
    size = models.CharField(max_length=20, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="size_changed_by", editable=False,
                                   null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.size)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.size

    class Meta:
        verbose_name_plural = "size"


class Color(models.Model):
    color_name = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    color = ColorField(default='#FF0000', unique=True)
    parent_color = models.ForeignKey(
        'self', on_delete=models.PROTECT, null=True, blank=True, related_name='pcolor')
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="color_changed_by", editable=False,
                                   null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.color

    def __repr__(self):
        return self.__str__()

    def color_published(self):
        if self.color:
            return format_html(
                '<div style="background:{}; width:80px; border-radius:10px; text-align:center;">{}</div>', self.color,
                self.color)

    def patent_color_published(self):
        if self.parent_color:
            return format_html(
                '<div style="background:{}; width:80px; border-radius:10px; text-align:center;">{}</div>',
                self.parent_color, self.parent_color)

    class Meta:
        verbose_name_plural = "color"


class CareInstructions(models.Model):
    instruction_name = models.CharField(max_length=255, unique=True)
    cares_details = RichTextUploadingField()
    details = models.CharField(
        max_length=250, default="CI")
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="care_changed_by", editable=False,
                                   null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.instruction_name

    def __repr__(self):
        return self.__str__()

    def care_instructions_details(self):
        from django.utils.html import strip_tags
        print('entered')
        if self.cares_details:
            return strip_tags(self.cares_details)

    class Meta:
        verbose_name_plural = "care instructions"


class UserCart(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    product_id = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    size_id = models.ForeignKey(
        Size, on_delete=models.PROTECT, null=True, blank=True)
    color_id = models.ForeignKey(Color, verbose_name="Color of Product", on_delete=models.PROTECT, null=True,
                                 blank=True)
    product_color = ColorField()
    quantity = models.IntegerField(
        'Quantity', default=1,  blank=True, null=True)
    total_price = models.FloatField("Total Price", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,  related_name="cart_created_by",
                                   editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="cart_changed_by", editable=False,
                                   null=True, blank=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super(UserCart, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_id.product_name

    def color(self):
        if self.color_id:
            return mark_safe('<div style="width:15px; height:15px; background:%s;"></div>' % (self.color_id))
        else:
            return 'No'

    def image(self):
        from django.utils.html import mark_safe
        if self.product_id.productimage:
            return mark_safe('<img src="%s" width="50px" height="auto" style="border:1px solid #cccccc;"/>' % (
                self.product_id.productimage.url))
        else:
            return 'No Image Found'

    class Meta:
        verbose_name_plural = "Customer Cart"


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    size_ids = models.ManyToManyField(Size)
    color_ids = models.ManyToManyField(Color, blank=True)
    instruction_ids = models.ManyToManyField(CareInstructions, blank=True)
    relative_product_ids = models.ManyToManyField(
        'self', blank=True, verbose_name="Related Product", )
    item_detail = models.TextField(
        verbose_name="Product Details", null=True, blank=True)
    price = models.FloatField()
    discount_price = models.FloatField()
    productimage = models.ImageField(upload_to="images/product/")
    expected_delivery_date = models.IntegerField(
        verbose_name="Expected Delivery Days", blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, editable=False, null=True, blank=True)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="age_changed_by", editable=False,
                                   null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        self.discount_price = round(self.discount_price, 2)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "product"
