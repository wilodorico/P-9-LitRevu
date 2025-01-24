from django import template


register = template.Library()


@register.filter
def stars_count(rating):
    try:
        return range(min(int(rating), 5))
    except (ValueError, TypeError):
        return range(0)
