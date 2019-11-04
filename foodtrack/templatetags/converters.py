from django import template

register = template.Library()


@register.filter(name="convert_currency")
def convert_currency(value, currency):
    return value / currency.rate
