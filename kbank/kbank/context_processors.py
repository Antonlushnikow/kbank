from mainapp.models import Category, Notification


def add_categories(request):
    categories = Category.objects.all()

    return {
        'categories': categories,
    }


def add_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_date')[:5]
        return {
            'notifications': notifications,
        }
    return {}
