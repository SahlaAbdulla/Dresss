# Generated by Django 5.1.6 on 2025-03-08 14:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Maria', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Maria.basemodel')),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('payment_method', models.CharField(choices=[('COD', 'COD'), ('ONLINE', 'ONLINE')], default='COD', max_length=15)),
                ('rzp_order_id', models.CharField(max_length=100, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('Maria.basemodel',),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Maria.basemodel')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.FloatField()),
                ('dress_varient_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Maria.dressvarient')),
                ('order_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='Maria.order')),
            ],
            bases=('Maria.basemodel',),
        ),
    ]
