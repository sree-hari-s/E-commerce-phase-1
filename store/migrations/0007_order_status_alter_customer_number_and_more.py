# Generated by Django 4.1.3 on 2022-12-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Placed', 'Placed'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Shoes', 'Shoes'), ('Watches', 'Watches')], default=None, max_length=200, null=True),
        ),
    ]
