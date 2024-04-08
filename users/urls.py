# urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("ticket/<str:ticket_id>/make_payment/", views.make_payment, name="make_payment"),
    path("booking/<str:booking_id>/make_payment/", views.make_payment_booking, name="make_payment_booking"),
    path("payment_success/<str:transaction_id>/", views.payment_success, name='payment_success'),
    # Other URL patterns
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profile/', views.userProfile, name="user-profile"),
    path('edit-account/', views.editAccount, name="edit-account"),

    ##Experimental:
    path('tour_packages/', views.tour_packages, name='tour_packages'),
    path('discount/', views.discount, name='discount'),
    path('complain/', views.complain, name='complain'),

    ##Not included in Main
    path('profiles/', views.profiles, name="profiles"),
    path('account/', views.userAccount, name="account"),
    ## TODO
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:pk>/', views.createMessage, name="create-message"),


]
