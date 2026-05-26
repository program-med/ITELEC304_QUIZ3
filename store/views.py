from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def product_list(request):
    query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '')
    products = Product.objects.filter(available=True)
    categories = Category.objects.order_by('name')

    if query:
        products = products.filter(name__icontains=query)

    if selected_category:
        products = products.filter(category__slug=selected_category)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': selected_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {
        'product': product,
    })