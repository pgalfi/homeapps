from django.db.models import QuerySet
from django.template import loader
from django.utils.encoding import force_text
from django.views import View
from rest_framework.compat import (
    coreapi, coreschema
)
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request


class FieldFilter(BaseFilterBackend):
    field_names = []
    template = 'filters/field-filter.html'

    def get_field_names(self, view: View):
        return getattr(view, "field_names", [])

    def get_filter_args(self, request: Request, view: View, to_queryset: bool = True):
        filter_args = {}
        for field_name in self.get_field_names(view):
            filter_value = request.query_params.get(field_name, "")
            if filter_value or not to_queryset:
                filter_args[field_name] = filter_value
        return filter_args

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View):
        return queryset.filter(**self.get_filter_args(request, view))

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=field_name,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_text(field_name),
                    description=force_text("Provide value for field to filter on")
                )
            ) for field_name in self.get_field_names(view)
        ]

    def to_html(self, request: Request, queryset: QuerySet, view: View):
        if not getattr(view, 'field_names', None):
            return ''
        context = {
            'filter_args': self.get_filter_args(request, view, False)
        }
        template = loader.get_template(self.template)
        return template.render(context)
