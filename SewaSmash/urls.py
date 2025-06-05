from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public URLs
    path('', views.homepage, name='homepage'),
    path('booking/create/', views.booking_create, name='booking_create'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('schedule/', views.schedule_view, name='schedule'),

    # Admin URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('booking/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('booking/admin/create/', views.AdminBookingCreateView.as_view(), name='admin_booking_create'),
    path('booking/<int:pk>/edit/', views.AdminBookingUpdateView.as_view(), name='admin_booking_edit'),
    path('booking/<int:pk>/delete/', views.AdminBookingDeleteView.as_view(), name='admin_booking_delete'),
    path('booking/<int:pk>/update-status/', views.update_booking_status, name='update_booking_status'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='SewaSmash/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homepage', template_name=None), name='logout'),
] 