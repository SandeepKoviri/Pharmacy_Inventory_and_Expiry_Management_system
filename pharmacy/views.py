from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Manufacturer, Medicine, Purchase, Sale


def home(request):
    return render(request, "pharmacy/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "staff")
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password.")
        elif role == "admin" and not user.is_superuser:
            messages.error(request, "This account does not have admin access.")
        elif role == "staff" and user.is_superuser:
            messages.error(request, "Please select Admin for this account.")
        else:
            login(request, user)
            return redirect("dashboard")
    return render(request, "pharmacy/login.html")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm = request.POST.get("confirm_password", "")
        if not username or not password:
            messages.error(request, "Username and password are required.")
        elif password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            parts = full_name.split(maxsplit=1)
            user.first_name = parts[0] if parts else ""
            user.last_name = parts[1] if len(parts) > 1 else ""
            user.save()
            messages.success(request, "Staff account created. You can now log in.")
            return redirect("login")
    return render(request, "pharmacy/signup.html")


def staff_check(user):
    return user.is_authenticated and not user.is_superuser


def admin_check(user):
    return user.is_authenticated and user.is_superuser


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect("admin_dashboard" if request.user.is_superuser else "staff_dashboard")


def dashboard_context():
    today = timezone.localdate()
    near = today + timedelta(days=30)
    return {
        "medicine_count": Medicine.objects.count(),
        "total_stock": Medicine.objects.aggregate(total=Sum("stock"))["total"] or 0,
        "low_stock_count": Medicine.objects.filter(stock__lte=F("reorder_level")).count(),
        "expired_count": Medicine.objects.filter(expiry_date__lt=today).count(),
        "near_expiry_count": Medicine.objects.filter(expiry_date__gte=today, expiry_date__lte=near).count(),
        "purchase_count": Purchase.objects.count(),
        "sale_count": Sale.objects.count(),
        "recent_purchases": Purchase.objects.select_related("medicine").all()[:5],
        "recent_sales": Sale.objects.select_related("medicine").all()[:5],
    }


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("staff_dashboard")
    return render(request, "pharmacy/admin_dashboard.html", dashboard_context())


@login_required
def staff_dashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    return render(request, "pharmacy/staff_dashboard.html", dashboard_context())


@login_required
def medicines(request):
    q = request.GET.get("q", "").strip()
    qs = Medicine.objects.select_related("manufacturer")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(generic_name__icontains=q) | Q(batch_number__icontains=q) | Q(manufacturer__name__icontains=q))
    return render(request, "pharmacy/medicines.html", {"medicines": qs, "q": q})


@login_required
@user_passes_test(admin_check, login_url="login")
def medicine_create(request):
    manufacturers = Manufacturer.objects.all()
    if request.method == "POST":
        try:
            Medicine.objects.create(
                name=request.POST.get("name", "").strip(),
                generic_name=request.POST.get("generic_name", "").strip(),
                manufacturer_id=request.POST.get("manufacturer"),
                batch_number=request.POST.get("batch_number", "").strip(),
                manufacturing_date=request.POST.get("manufacturing_date"),
                expiry_date=request.POST.get("expiry_date"),
                price=Decimal(request.POST.get("price", "0")),
                stock=int(request.POST.get("stock", "0")),
                reorder_level=int(request.POST.get("reorder_level", "10")),
                description=request.POST.get("description", "").strip(),
            )
            messages.success(request, "Medicine added successfully.")
            return redirect("medicines")
        except (ValueError, InvalidOperation, TypeError):
            messages.error(request, "Please enter valid medicine details.")
    return render(request, "pharmacy/medicine_form.html", {"manufacturers": manufacturers})


@login_required
@user_passes_test(admin_check, login_url="login")
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    manufacturers = Manufacturer.objects.all()
    if request.method == "POST":
        try:
            medicine.name = request.POST.get("name", "").strip()
            medicine.generic_name = request.POST.get("generic_name", "").strip()
            medicine.manufacturer_id = request.POST.get("manufacturer")
            medicine.batch_number = request.POST.get("batch_number", "").strip()
            medicine.manufacturing_date = request.POST.get("manufacturing_date")
            medicine.expiry_date = request.POST.get("expiry_date")
            medicine.price = Decimal(request.POST.get("price", "0"))
            medicine.stock = int(request.POST.get("stock", "0"))
            medicine.reorder_level = int(request.POST.get("reorder_level", "10"))
            medicine.description = request.POST.get("description", "").strip()
            medicine.save()
            messages.success(request, "Medicine updated successfully.")
            return redirect("medicines")
        except (ValueError, InvalidOperation, TypeError):
            messages.error(request, "Please enter valid medicine details.")
    return render(request, "pharmacy/medicine_form.html", {"medicine": medicine, "manufacturers": manufacturers})


@login_required
@user_passes_test(admin_check, login_url="login")
def medicine_delete(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        medicine.delete()
        messages.success(request, "Medicine deleted.")
    return redirect("medicines")


@login_required
def manufacturers(request):
    qs = Manufacturer.objects.all()
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(contact__icontains=q))
    return render(request, "pharmacy/manufacturers.html", {"manufacturers": qs, "q": q})


@login_required
@user_passes_test(admin_check, login_url="login")
def manufacturer_create(request):
    if request.method == "POST":
        Manufacturer.objects.create(
            name=request.POST.get("name", "").strip(),
            contact=request.POST.get("contact", "").strip(),
            email=request.POST.get("email", "").strip(),
            address=request.POST.get("address", "").strip(),
        )
        messages.success(request, "Manufacturer added successfully.")
    return redirect("manufacturers")


@login_required
@user_passes_test(admin_check, login_url="login")
def manufacturer_delete(request, pk):
    if request.method == "POST":
        manufacturer = get_object_or_404(Manufacturer, pk=pk)
        manufacturer.delete()
        messages.success(request, "Manufacturer deleted.")
    return redirect("manufacturers")


@login_required
def batches(request):
    qs = Medicine.objects.select_related("manufacturer")
    return render(request, "pharmacy/batches.html", {"batches": qs})


@login_required
def purchases(request):
    if request.method == "POST":
        medicine = get_object_or_404(Medicine, pk=request.POST.get("medicine"))
        try:
            qty = int(request.POST.get("quantity", "0"))
            price = Decimal(request.POST.get("purchase_price", "0"))
            if qty <= 0 or price < 0:
                raise ValueError
            with transaction.atomic():
                Purchase.objects.create(
                    medicine=medicine,
                    batch_number=request.POST.get("batch_number", "").strip() or medicine.batch_number,
                    supplier=request.POST.get("supplier", "").strip(),
                    quantity=qty,
                    purchase_price=price,
                    expiry_date=request.POST.get("expiry_date") or None,
                    created_by=request.user,
                )
                Medicine.objects.filter(pk=medicine.pk).update(stock=F("stock") + qty)
            messages.success(request, f"Purchase recorded. {qty} units added to stock.")
        except (ValueError, InvalidOperation, TypeError):
            messages.error(request, "Enter valid purchase details.")
        return redirect("purchases")
    return render(request, "pharmacy/purchases.html", {"medicines": Medicine.objects.all(), "purchases": Purchase.objects.select_related("medicine")[:100]})


@login_required
def sales(request):
    if request.method == "POST":
        medicine = get_object_or_404(Medicine.objects.select_for_update(), pk=request.POST.get("medicine"))
        try:
            qty = int(request.POST.get("quantity", "0"))
            price = Decimal(request.POST.get("selling_price", "0"))
            if qty <= 0 or price < 0:
                raise ValueError
            with transaction.atomic():
                medicine = Medicine.objects.select_for_update().get(pk=medicine.pk)
                if medicine.expiry_date < timezone.localdate():
                    messages.error(request, "Cannot sell an expired medicine.")
                    return redirect("sales")
                if qty > medicine.stock:
                    messages.error(request, f"Insufficient stock. Available: {medicine.stock}.")
                    return redirect("sales")
                Sale.objects.create(
                    medicine=medicine,
                    batch_number=request.POST.get("batch_number", "").strip() or medicine.batch_number,
                    quantity=qty,
                    customer_name=request.POST.get("customer_name", "").strip(),
                    selling_price=price,
                    created_by=request.user,
                )
                medicine.stock -= qty
                medicine.save(update_fields=["stock"])
            messages.success(request, f"Sale recorded. {qty} units removed from stock.")
        except (ValueError, InvalidOperation, TypeError):
            messages.error(request, "Enter valid sale details.")
        return redirect("sales")
    return render(request, "pharmacy/sales.html", {"medicines": Medicine.objects.all(), "sales": Sale.objects.select_related("medicine")[:100]})


@login_required
def alerts(request):
    today = timezone.localdate()
    near = today + timedelta(days=30)
    context = {
        "expired": Medicine.objects.filter(expiry_date__lt=today).select_related("manufacturer"),
        "near_expiry": Medicine.objects.filter(expiry_date__gte=today, expiry_date__lte=near).select_related("manufacturer"),
        "low_stock": Medicine.objects.filter(stock__lte=F("reorder_level")).select_related("manufacturer"),
    }
    return render(request, "pharmacy/alerts.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")
