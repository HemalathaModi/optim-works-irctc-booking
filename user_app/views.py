from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Train, Station, Booking, Passenger, Payment, UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from django.http import JsonResponse
from .forms import SignupForm, LoginForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            UserProfile.objects.create(
                user=user,
                full_name=user.username,
                phone="",
                address=""
            )

            messages.success(request, "Signup Successful! Please Login.")
            return redirect('login')

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid Credentials")

    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.POST.get("full_name")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.save()
        return render(request, "profile.html", {"profile": profile})

    return render(request, "edit_profile.html", {"profile": profile})


def search_trains(request):
    if request.method == 'GET':
        from_station = request.GET.get('from')
        to_station = request.GET.get('to')
        date = request.GET.get('date')
        trains = []
        if from_station and to_station:
            trains = Train.objects.filter(from_station__code__iexact=from_station, to_station__code__iexact=to_station)
        return render(request, 'search_results.html', {'trains': trains, 'date': date})

def check_availability(request):
    train_id = request.GET.get('train_id')
    travel_date = request.GET.get('date')
    train = get_object_or_404(Train, id=train_id)
    booked_count = Booking.objects.filter(train=train, travel_date=travel_date, status='CONFIRMED').count() * 1 
    available = max(train.total_seats - booked_count, 0)
    return JsonResponse({'available_seats': available})

@login_required
def book_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    if request.method == 'POST':
        travel_date = request.POST['date']
        booking = Booking.objects.create(user=request.user, train=train, travel_date=travel_date, status='PENDING', total_amount=100.00)
        Passenger.objects.create(booking=booking, name=request.POST['p_name'], age=int(request.POST['p_age']), gender=request.POST['p_gender'], berth_preference=request.POST.get('p_berth',''))
        Payment.objects.create(booking=booking, method=request.POST.get('payment_method','mock'), amount=booking.total_amount)
        return redirect('confirm_booking', booking_id=booking.id)
    return render(request, 'book_train.html', {'train': train})

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'CONFIRMED'
    booking.save()
    p = booking.passengers.all()
    return render(request, 'confirmation.html', {'booking': booking, 'passengers': p})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'CANCELLED'
    booking.save()
    return redirect('profile')

