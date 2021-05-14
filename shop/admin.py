from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import Product, Color, Size, CareInstructions
from django.utils.html import format_html, mark_safe
from django.shortcuts import redirect
from django_tabbed_changeform_admin.admin import DjangoTabbedChangeformAdmin


class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color_name', 'color_published',
                    'patent_color_published',)
    list_display_links = ('id', 'color_name')


class CareInstructionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'instruction_name', 'cares_details',)
    list_display_links = ('id', 'instruction_name')


class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size', 'active')
    list_display_links = ('id', 'size')

    ordering = ['-id']


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class SizeInline(admin.TabularInline):
    model = Product.size_ids.through
    extra = 1


class ColorInline(admin.TabularInline):
    model = Product.color_ids.through
    extra = 1


class CareInstructionInline(admin.TabularInline):
    model = Product.instruction_ids.through
    extra = 1


class ProductAdmin(DjangoTabbedChangeformAdmin, admin.ModelAdmin):
    list_display = (
        'id', 'product_name', 'slug', 'price', 'discount_price', 'active')
    list_display_links = ('id', 'product_name')
    list_filter = ['price', 'active']
    prepopulated_fields = {'slug': ('product_name',)}
    ordering = ['-id']
    readonly_fields = ["id", "image_thumbnail", ]
    inlines = (SizeInline, ColorInline, CareInstructionInline)

    def changelist_view(self, request, extra_context=None):
        if len(request.GET) == 0:
            get_param = "active=True"
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(ProductAdmin, self).changelist_view(request, extra_context=extra_context)

    def size_ids(self, obj):
        return ",".join([str(p.size) for p in obj.size.all()])

    def colors(self, obj):
        color_name = ([str(p.color_name) for p in obj.color.all()])
        color_rgb = ([str(p.color) for p in obj.color.all()])
        new_dict = dict(zip(color_name, color_rgb))

        res = format_html("\n ".join((
                                     "{} <div style='background:{};width:12px;height:12px;border-radius:100%;display:inline-block;border:1px solid #999999;'>&nbsp;</div>,".format(
                                         *i) for i in new_dict.items())))
        return res

    def image_thumbnail(self, obj):

        return mark_safe('<img src="{url}" width="75px" height="auto" style="border:1px solid #cccccc;" />'.format(
            url=obj.productimage.url,
        )
        )

    fieldsets = [
        (None, {
            "fields": ["product_name", "slug", "expected_delivery_date",
                       "price", "discount_price", "productimage", "image_thumbnail"],
            "classes": ["tab-first"],
        }),

    ]


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(CareInstructions, CareInstructionsAdmin)
admin.site.register(Product, ProductAdmin)
