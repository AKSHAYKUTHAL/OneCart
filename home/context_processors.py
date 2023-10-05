from .models import Categories

def category_links(request):
    categories = Categories.objects.all()
    return dict(categories=categories)