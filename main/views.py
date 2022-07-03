from django.shortcuts import render, redirect
from main.models import Ways, Bookings, Parcels, Stores
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from random import randint
import smtplib


emails = {
    "Germany": "arex.de.post@gmail.com",
    "Armenia": "arex.am.post@gmail.com",
    "Greece": "arex.gr.post@gmail.com"
}


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# Create your views here.

def index(request):
    ways = Ways.objects.all().order_by('dep_date')
    booking_info = None
    found = None

    print(request.GET)
    if request.method == "GET" and "successBooking" in request.GET:
        booking_info = "successBooking"

    if request.method == "GET" and "notFound" in request.GET:
        found = "notFound"

    data = {
        "found": found,
        "booking_info": booking_info,
        "ways": ways
    }



    if request.method == "POST":
        print(request.POST.get('to'))
        if request.user.is_authenticated:
            Bookings.objects.create(user_id = request.user.id, name = "Name", username = request.user.username, phone = request.POST.get('phone'),
                                    city_from = request.POST.get('from'), city_to = request.POST.get('to'),
                                    kg = request.POST.get('kg'))
            print(request.user.email)

            s = smtplib.SMTP('smtp.gmail.com', 587)

            s.starttls()

            s.login("arex.gr.sender@gmail.com", "Arex.123")

            message = f"New book!\n" \
                      f"From - {request.POST.get('from')}\n" \
                      f"To - {request.POST.get('to')}\n" \
                      f"Phone - {request.POST.get('phone')}\n"

            s.sendmail("arex.gr.sender@gmail.com", emails[request.user.last_name], message)

            s.quit

            return redirect('http://195.161.68.148:49282/?successBooking', data)
        else:
            Bookings.objects.create(name = request.POST.get('fname'), username=" ", phone= request.POST.get('phone'),
                                    city_from=request.POST.get('from'), city_to=request.POST.get('to'),
                                    kg=request.POST.get('kg'))

            s = smtplib.SMTP('smtp.gmail.com', 587)

            s.starttls()

            s.login("arex.gr.sender@gmail.com", "Arex.123")

            message = f"New book!\n" \
                      f"From - {request.POST.get('from')}\n" \
                      f"To - {request.POST.get('to')}\n" \
                      f"Phone - {request.POST.get('phone')}\n"

            s.sendmail("arex.gr.sender@gmail.com", emails[request.POST.get('country')], message)

            s.quit


            return redirect('http://195.161.68.148:49282/?successBooking', data)

    return render(request, 'main/index.html', data)

def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("../accounts/profile")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponseRedirect("http://195.161.68.148:49282/")


    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    orders = 0
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            current_user = request.user
            orders = Bookings.objects.all().filter(user_id = current_user.id)

            return HttpResponseRedirect('profile') # Redirect back to profile page
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'orders' : orders,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'main/profile.html', context)



def pagelogout(request):
    try:
        logout(request)

        return redirect('index')
    except Exception as e:
        print(e)
        return redirect('index')



def contacts(request):
    return render(request, 'main/contacts.html')


def add_parcel(request):
    track_number = " "
    if request.method == "GET" and "city_f" in request.GET and "city_t" in request.GET and "kg" in request.GET:
        track_number = f"{request.GET.get('city_f')[:2].upper()}{random_with_N_digits(9)}{request.GET.get('city_t')[:2].upper()}"
        Parcels.objects.create(city_from=request.GET.get('city_f'),
                                city_to=request.GET.get('city_t'),
                                kg=request.GET.get('kg'),
                                track_number=track_number)
    data = {
        "track_number": track_number
    }

    return render(request, 'main/add_parcel.html', data)


def track_result(request):
    ways = Ways.objects.all()
    status = " "
    if request.method == "GET" and "track_number" in request.GET:
        for way in ways:
            print(way.city_from[:2].upper())
            if way.city_from[:2].upper() == request.GET.get('track_number')[:2] and way.city_to[:2].upper() == request.GET.get('track_number')[-2:]:
                status = way.status

    data = {
        'status': status,
        'track_number': request.GET.get('track_number')
    }
    print(status)
    return render(request, 'main/track_result.html', data)


@login_required
def stores(request):
    stores = Stores.objects.all()

    data = {
        'stores': stores
    }
    return render(request, "main/stores.html", data)