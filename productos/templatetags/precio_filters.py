from django import template

register = template.Library()

@register.filter
def moneda_co(value):
    """Formatea un número como pesos colombianos: 250000 -> 250.000"""
    try:
        valor = int(float(value))
    except (TypeError, ValueError):
        return value
    return f"{valor:,}".replace(",", ".")