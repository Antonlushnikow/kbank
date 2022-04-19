"""
Mixin Classes
"""


class RedirectToPreviousMixin:
    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', '/')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']
