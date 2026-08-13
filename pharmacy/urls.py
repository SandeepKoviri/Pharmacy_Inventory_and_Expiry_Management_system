from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff-dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("medicines/", views.medicines, name="medicines"),
    path("medicines/add/", views.medicine_create, name="medicine_create"),
    path("medicines/<int:pk>/edit/", views.medicine_edit, name="medicine_edit"),
    path("medicines/<int:pk>/delete/", views.medicine_delete, name="medicine_delete"),
    path("manufacturers/", views.manufacturers, name="manufacturers"),
    path("manufacturers/add/", views.manufacturer_create, name="manufacturer_create"),
    path("manufacturers/<int:pk>/delete/", views.manufacturer_delete, name="manufacturer_delete"),
    path("batches/", views.batches, name="batches"),
    path("purchases/", views.purchases, name="purchases"),
    path("sales/", views.sales, name="sales"),
    path("alerts/", views.alerts, name="alerts"),
]
