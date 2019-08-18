from django import template
from django.core.paginator import Page, Paginator

register = template.Library()


@register.inclusion_tag("ranged_paginator.html", takes_context=True)
def ranged_paginator(context: dict, adjacent_pages=2):
    page: Page = context["page_obj"]
    paginator_: Paginator = context["paginator"]
    page_numbers = [n for n in range(page.number - adjacent_pages, page.number + adjacent_pages + 1)
                    if 0 < n <= paginator_.num_pages]
    context.update({
        "page_numbers": page_numbers,
        "show_first": 1 not in page_numbers,
        "show_last": paginator_.num_pages not in page_numbers,
    })
    return context
