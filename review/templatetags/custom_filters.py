from django import template


register = template.Library()


@register.filter
def stars_count(rating):
    try:
        return range(min(int(rating), 5))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def model_name(obj):
    """Retourne le nom du modèle d'un objet Django"""
    return obj.__class__.__name__.lower()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, False)
