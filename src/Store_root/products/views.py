from django.shortcuts import render, HttpResponseRedirect
from products.models import ProductCotegory, Product, Basket
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context = {
        'title': "store"
    }
    return render(request, 'products/index.html', context=context)

# def products(request, category_id=None):
#     context = {'title': "store - Каталог", 'categories': ProductCotegory.objects.all()}
#     if category_id:
#         context.update({'products': Product.objects.filter(category_id=category_id)})
#     else:
#         context.update({'products': Product.objects.all()})
#     return render(request, 'products/products.html', context=context)

def products(request):
    context = {'title': "store - Каталог",
               'categories': ProductCotegory.objects.all(),
               'products': Product.objects.all()
               }
    return render(request, 'products/products.html', context=context)


@login_required()
def basket_add(request, product_id):
    current_page = request.META.get('HTTP_REFERER')
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quontity=1)
        return HttpResponseRedirect(current_page)
    else:
        basket = baskets.first()
        basket.quontity += 1
        basket.save()
        return HttpResponseRedirect(current_page)


@login_required()
def basket_delete(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))