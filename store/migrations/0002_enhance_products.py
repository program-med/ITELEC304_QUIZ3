from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.text import slugify


def generate_unique_slugs(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for product in Product.objects.all():
        base_slug = slugify(product.name) or 'product'
        slug = base_slug
        count = 1
        while Product.objects.filter(slug=slug).exclude(pk=product.pk).exists():
            count += 1
            slug = f"{base_slug}-{count}"
        product.slug = slug
        product.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='store.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, default='', max_length=60),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=170),
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.RunPython(generate_unique_slugs, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=170, unique=True),
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
    ]
