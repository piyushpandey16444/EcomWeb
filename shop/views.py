import threading
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponseRedirect, response
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import UserAdminCreationForm, AuthenticateForm
from .models import CustomUser, Product, UserCart, Size, Color
from .utils import token_generator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def home_view(request):
    product_objs = get_list_or_404(Product)
    context = {
        "product_objs": product_objs,
    }
    return render(request, 'shop/home.html', context=context)


def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)  # object
    size_objs = product.size_ids.all()  # many2many related to obj
    color_objs = product.color_ids.all()  # many2many related to obj
    instruction_objs = product.instruction_ids.all()
    context = {
        "product": product,
        "size_objs": size_objs,
        "color_objs": color_objs,
        "instruction_objs": instruction_objs,
    }
    return render(request, 'shop/product-detail.html', context=context)


def product_detail_view(request):
    return render(request, 'shop/product-detail.html')


def signup_view(request):
    form = UserAdminCreationForm()
    if request.method == "GET":
        return render(request, 'shop/signup.html', {'form': form})

    elif request.method == 'POST':
        """
        takes data from user, validate it and send an activation mail if everything is fine.
        else returns the error to the user.
        """
        form = UserAdminCreationForm(request.POST)
        password1 = form.data['password1']
        password2 = form.data['password2']
        email = form.data['email']
        if not email or not password1 or not password2:
            messages.error(request, 'Please provide all the fields.')
            return redirect('signup')
        if form.is_valid():
            form.save()
            uid64 = urlsafe_base64_encode(force_bytes(form.instance.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                "uid64": uid64,
                "token": token_generator.make_token(form.instance),
            })
            activate_url = f'http://{domain}{link}'

            email_body = f"Hi {form.instance.email}, \nPlease use this link to verify your account.\n {activate_url}"
            email_subject = "Activate your account."
            from_email = "no_reply@botmail.com"
            to_email = [form.instance.email]
            email = EmailMessage(
                email_subject,
                email_body,
                from_email,
                to_email,
            )
            EmailThread(email).start()
            messages.success(
                request, 'Account is created, please verify your email.')
            return redirect('/signup/')
        else:
            for msg in form.errors.as_data():
                if msg == 'password2' and password1 == password2:
                    messages.error(
                        request, f"Selected password is not strong enough")
                elif msg == 'password2' and password1 != password2:
                    messages.error(request,
                                   f"Password and Confirmation Password do not match")
                if msg == 'email':
                    messages.error(
                        request, f"Declared email: {email} is not valid")
            return redirect('signup')


@receiver(post_save, sender=CustomUser)
def default_to_non_active(instance, created, **kwargs):
    if created and (not instance.is_superuser and not instance.is_staff):
        instance.is_active = False
        instance.save()


def login_view(request):
    form = AuthenticateForm()
    if request.method == "GET":
        return render(request, 'shop/login.html', {'form': form})

    elif request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                messages.success(
                    request, 'Account is not active, please check your email.')
                return redirect('login')
            messages.error(
                request, 'Invalid credentials or account is not active, please check your email.')
            return redirect('login')
        messages.success(request, 'Please provide both the fields.')
        return redirect('login')


def verification_view(request, uid64, token):
    """
    code for verification of token and activation of user based on token.
    """
    try:
        required_id = force_text(urlsafe_base64_decode(uid64))
        user = CustomUser.objects.get(id=required_id)

        if not token_generator.check_token(user, token):
            return redirect('login' + '?message=' + 'User already activated')
        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully.')
        return redirect('login')

    except Exception as E:
        print("Exception: ", E)
    return HttpResponseRedirect('/login/')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')


@csrf_exempt
@login_required
def delete_cart(request):
    if request.method == "DELETE":
        json_data = request.body
        py_dict = json.loads(json_data.decode())
        UserCart.objects.filter(id=py_dict['req_id']).delete()
        return JsonResponse(data={'response': 'deleted'}, safe=True)


@login_required
def cart_view(request):
    cart_items = get_list_or_404(UserCart, user_id=request.user)
    total_cart_items = len(cart_items)
    context = {
        "cart_items": cart_items,
        "total_cart_items": total_cart_items,
    }
    return render(request, 'shop/cart.html', context=context)


@csrf_exempt
# @login_required
def add_to_cart(request):
    if request.method == "POST" and request.is_ajax():
        json_data = request.body
        py_dict = json.loads(json_data.decode())
        product = py_dict.get('product')
        size = py_dict.get('size')
        color = py_dict.get('color')
        if not size or not color:
            return JsonResponse({"response": "NOK"})

        product_id = get_object_or_404(Product, id=product)
        size_id = get_object_or_404(Size, size=size)
        color_id = get_object_or_404(Color, color=color)
        cart_obj, created = UserCart.objects.get_or_create(user_id=request.user, product_id=product_id, size_id=size_id,
                                                           color_id=color_id)
        quantity = cart_obj.quantity
        if created:
            cart_obj.quantity = quantity
            cart_obj.total_price = product_id.price * cart_obj.quantity
            cart_obj.save()
            return JsonResponse({"response": "Item Added to cart !"})
        else:
            cart_obj.quantity += 1
            cart_obj.total_price = product_id.price * cart_obj.quantity
            cart_obj.save()
            return JsonResponse({"response": "Item qty incremented !"})
