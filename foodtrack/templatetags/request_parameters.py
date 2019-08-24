from django import template

register = template.Library()


@register.simple_tag(name="set-param", takes_context=True)
def build_reference(context, **kwargs):
    get_params = context["request"].GET.copy()
    for k, v in kwargs.items():
        get_params[k] = v
    return get_params.urlencode()
