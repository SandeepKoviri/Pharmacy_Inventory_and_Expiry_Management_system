from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="medicines")
    batch_number = models.CharField(max_length=100)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name", "expiry_date"]

    def __str__(self):
        return f"{self.name} ({self.batch_number})"

    @property
    def is_low_stock(self):
        return self.stock <= self.reorder_level

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.expiry_date < timezone.localdate()

    @property
    def is_near_expiry(self):
        from datetime import timedelta
        from django.utils import timezone
        today = timezone.localdate()
        return today <= self.expiry_date <= today + timedelta(days=30)


class Purchase(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name="purchases")
    batch_number = models.CharField(max_length=100)
    supplier = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-purchase_date", "-id"]

    def __str__(self):
        return f"Purchase #{self.pk} - {self.medicine.name}"


class Sale(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name="sales")
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=200, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-sale_date", "-id"]

    def __str__(self):
        return f"Sale #{self.pk} - {self.medicine.name}"
