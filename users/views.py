# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from .forms import PaymentForm
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile, Payment
from .forms import CustomUserCreationForm, ProfileForm, MessageForm
from tickets.models import Ticket
from hotels.models import Booking
from .utils import searchProfiles, paginateProfiles

def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

@login_required(login_url='login')
def make_payment(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    if request.method == "POST":
            ##TODO: provide necessary info to create the payment
            payment = Payment.objects.create(amount=ticket.total_price,
                                             status = 'completed',
                                             user = request.user
                                             )
            ticket.payment = payment
            ticket.save()
            # Redirect to a success page or any other appropriate view
            return redirect('users:payment_success', payment.transaction_id )

    return render(request, 'users/make_payment.html', {'ticket': ticket})

@login_required(login_url='login')
def make_payment_booking(request, booking_id):
    ticket = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == "POST":
            ##TODO: provide necessary info to create the payment
            payment = Payment.objects.create(amount=ticket.total_price,
                                             status = 'completed',
                                             user = request.user
                                             )
            ticket.payment = payment
            ticket.save()
            # Redirect to a success page or any other appropriate view
            return redirect('users:payment_success', payment.transaction_id )

    return render(request, 'users/make_payment.html', {'ticket': ticket})

def payment_success(request,transaction_id):
    from .models import Payment
    payment_obj = Payment.objects.get(transaction_id=transaction_id)

    return render(request, 'users/payment_success.html', {'payment': payment_obj})

def custom(request):
    return render(request, 'users/custom-index.html')

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('tickets:home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('tickets:home')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('tickets:home')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('users:edit-account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

@login_required(login_url='login')
def userProfile(request):
    profile = Profile.objects.get(user=request.user)

    tickets = Ticket.objects.filter(user=request.user)
    bookings = Booking.objects.filter(user=request.user)
    payments = Payment.objects.filter(user=request.user)

    context = {'profile': profile, 'tickets': tickets,
               "bookings": bookings,'payments':payments  }
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('tickets:home')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)

# XXX: test
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)

def discount(request):
    return render(request, 'users/discount.html')
def tour_packages(request):
    return render(request, 'users/tour_packages.html')
def complain(request):
    return render(request, 'users/complain.html')