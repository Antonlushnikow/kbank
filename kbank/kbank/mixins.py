"""
Mixin Classes
"""
from django.urls import reverse_lazy


class RedirectToPreviousMixin:
    """
    Возврат на предыдущую страницу
    """

    def get(self, request, *args, **kwargs):
        request.session["previous_page"] = request.META.get("HTTP_REFERER", "/")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if 'login' not in self.request.session["previous_page"]:
            return self.request.session["previous_page"]
        else:
            return reverse_lazy("index")
