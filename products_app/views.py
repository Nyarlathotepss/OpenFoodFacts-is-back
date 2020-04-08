from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from products_app.models import Product
from products_app import search


nutri_list = ["a", "b", "c", "d", "e"]


def home(request):
    return render(request, 'products_app/home.html')


def search_products(request):
    product, message, substitute_products, context = None, None, None, None
    my_search = search.Search()
    query = request.GET.get('query')
    if not query:
        message = "Votre saisie est vide !"
    else:
        product = Product.objects.filter(name__icontains=query)  # Insensible a la casse

        if not product.exists():
            message = "Votre produit n'existe pas dans notre base de donnée !"
        else:
            product = product.all()[0]
            substitute_products = my_search.search_products_better(product.category, product.name, product.nutriscore)
            message = "Voici des produits de substitution:"
    context = {
        'product': product,
        'alternativ_products': substitute_products,
        'message_to_display': message,
        'nutricode_list': nutri_list
          }
    return render(request, 'products_app/result.html', context)


def product_page(request, product_number):
    my_search = search.Search()
    product = my_search.search_product_by_id(product_number)
    context = {
                'product': product
               }
    return render(request, 'products_app/product_page.html', context)


def product_save(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product_query = Product.objects.get(id=product_id)
        product_query.save()
        current_user = request.user
        user_id = current_user.id
        user_query = User.objects.get(id=user_id)
        user_query.save()
        product_query.favorite_of.add(user_query)
        return render(request, 'products_app/product_saved.html')
    else:
        return redirect('login')


def favorites(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        products = Product.objects.all().filter(favorite_of=user_id)
        context = {
            'products': products,
            'nutricode_list': nutri_list,
        }
        return render(request, 'products_app/favorites.html', context)
    else:
        return redirect('login')


def favorite_deleted(request):
    if request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product_query = Product.objects.get(id=product_id)
        product_query.save()
        current_user = request.user
        user_id = current_user.id
        user_query = User.objects.get(id=user_id)
        user_query.save()
        product_query.favorite_of.remove(user_query)
        return render(request, 'products_app/home.html')


def law_mention(request):
    return render(request, 'products_app/law_mention.html')

