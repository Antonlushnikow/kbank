from mainapp.models import Category, Notification, SiteSettings


def add_categories(request):
    categories = Category.objects.all()

    return {
        "categories": categories,
    }


def add_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by(
            "-created_date"
        )[:5]
        return {
            "dropdown_notifications": notifications,
        }
    return {}


def get_site_logo(request):
    if SiteSettings.objects.exists():
        obj = SiteSettings.objects.all()[0]
        return {
            "site_logo": obj.logo_pic,
        }
    return {}
