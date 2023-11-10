# Generated by Django 4.2.5 on 2023-11-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participaciones',
            options={'verbose_name_plural': 'Participaciones'},
        ),
        migrations.RenameField(
            model_name='categoriacolaboraciones',
            old_name='baja',
            new_name='estado',
        ),
        migrations.RenameField(
            model_name='categoriaproyectos',
            old_name='baja',
            new_name='estado',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='estado',
            field=models.BooleanField(default=False, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='personas',
            name='foto_perfil',
            field=models.ImageField(blank=True, default='', null=True, upload_to='imagenes/', verbose_name='foto_perfil'),
        ),
    ]
