from django.shortcuts import render
from store.models import Product
from store.models import ReviewRating
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    products = Product.objects.all().filter(product_is_available=True).order_by('product_created_date')
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id,status=True)

    context = {
        'products':products,
        'reviews':reviews,
    }

    return render(request,'index.html',context)

# # change language


# from django.http import HttpResponse
# from django.shortcuts import redirect

# def change_language(request, language_code):
#     available_languages = ['en', 'pl']  # List of available languages

#     # Check if the selected language is in the available languages list
#     if language_code in available_languages:
#         request.session['selected_language'] = language_code

#     # Print some debug information
#     print(f"Selected Language: {language_code}")

#     # Redirect the user back to the referring page (or a default page)
#     return redirect(request.META.get('HTTP_REFERER', '/'))

