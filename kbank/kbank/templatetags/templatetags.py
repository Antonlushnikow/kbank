from django import template
from django.db.models import Count

register = template.Library()


@register.filter
def sort_by(queryset, order):
    if order == 'likes':
        return queryset.annotate(count=Count('likes')).order_by('-count')
    return queryset.order_by(order)
