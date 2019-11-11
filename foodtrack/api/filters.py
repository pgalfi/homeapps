import operator
import typing
from functools import reduce

from django.db.models import QuerySet, Q
from django.db.models.constants import LOOKUP_SEP
from django.template import loader
from django.utils.encoding import force_text
from django.views import View
from rest_framework.compat import (
    coreapi, coreschema
)
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request


class FieldFiltering(BaseFilterBackend):
    filter_fields: typing.List[typing.Dict] = []
    template = 'filters/field-filter.html'

    def get_filter_fields(self, view: View):
        return getattr(view, "filter_fields", [])

    def get_field_names(self, view: View):
        return [one_field.name for one_field in self.get_filter_fields(view)]

    def get_filter_args(self, request: Request, view: View, to_queryset: bool = True):
        args = {}
        for filter_field in self.get_filter_fields(view):
            field_name = filter_field["name"]
            filter_value = request.query_params.get(field_name, "")
            if to_queryset and filter_value:
                args[self.construct_lookup(filter_field)] = filter_value.replace(',', ' ').split()
            elif not to_queryset:
                args[field_name] = {
                    "value": filter_value,
                    "label": filter_field["label"].rstrip(":") + ":" if "label" in filter_field
                                else field_name.title().rstrip(":") + ":"
                }
        return args

    def construct_lookup(self, field: typing.Dict):
        if "lookup" in field and field["lookup"]:
            return field["name"] + LOOKUP_SEP + field["lookup"]
        return field["name"]

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View):
        filter_args = self.get_filter_args(request, view)

        conditions: typing.List[Q] = []
        for filter_arg, filter_values in filter_args.items():
            conditions.append(reduce(operator.or_, [
                Q(**{filter_arg: filter_value})
                for filter_value in filter_values
            ]))
        if conditions:
            queryset = queryset.filter(reduce(operator.and_, conditions))
        return queryset

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
                    description=force_text("Provide value for field to filter or search on")
                )
            ) for field_name in self.get_field_names(view)
        ]

    def to_html(self, request: Request, queryset: QuerySet, view: View):
        if not getattr(view, 'filter_fields', None):
            return ''
        context = {
            'filter_args': self.get_filter_args(request, view, False)
        }
        template = loader.get_template(self.template)
        return template.render(context)
