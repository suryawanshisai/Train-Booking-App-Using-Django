from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing),
    path("login/", views.login),
    path("register/", views.register),

    path("load-bookTrain/<str:trainId>", views.loadBookTrain),
    path("bookTrain/<str:trainId>/<str:userId>", views.bookTrain),
    
    path("load-bookings/", views.loadBookings),
    path("bookings/<str:id>", views.bookings),

    path("cancel-user-booking/<str:id>", views.cancelUserTicket),
    path("cancel-booking/<str:id>", views.cancelTicket),

    path("admin/", views.admin),
    path("allBookings/", views.allBookings),
    path("allUsers/", views.allUsers),
    path("allTrains/", views.allTrains),
    path("newTrain/", views.newTrain),
    path("editTrain/<str:id>", views.editTrain),

]
