from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacy', '0002_alter_manufacturer_id_alter_medicine_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine', name='generic_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='medicine', name='reorder_level',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=100)),
                ('supplier', models.CharField(max_length=200)),
                ('quantity', models.PositiveIntegerField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='pharmacy.medicine')),
            ],
            options={'ordering': ['-purchase_date', '-id']},
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('customer_name', models.CharField(blank=True, max_length=200)),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_date', models.DateField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', to='pharmacy.medicine')),
            ],
            options={'ordering': ['-sale_date', '-id']},
        ),
    ]
