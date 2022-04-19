from mainapp.models import Category


def add_categories(request):
    categories = Category.objects.all()

    return {
        'categories': categories,
    }
