# Generated by Django 2.2.6 on 2019-12-28 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_library', '0010_auto_20191228_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='book_avatars/%Y/%m/%d'),
        ),
    ]
