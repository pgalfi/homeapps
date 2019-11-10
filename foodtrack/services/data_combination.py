import typing

from django.core.exceptions import FieldError, FieldDoesNotExist
from django.db.models import QuerySet, Q, Model
from django.db.models.options import Options
from django.db.models.sql import Query
from django.http import Http404
from django.utils.tree import Node


class CombinedMeta:
    meta_set: typing.List[Options] = []

    def __init__(self, *args):
        self.meta_set = list(args)

    @property
    def fields(self):
        return [meta.get_fields() for meta in self.meta_set]

    def get_field(self, part):
        for meta in self.meta_set:
            try:
                result = meta.get_field(part)
                return result
            except FieldDoesNotExist:
                continue


class CombinedModel:
    models: typing.List[Model] = []

    def __init__(self, *args):
        self.models = list(args)
        self._meta = CombinedMeta(*[model._meta for model in self.models])


class CombinedQuery:
    queries: typing.List[Query] = []

    def __init__(self, *args):
        self.queries = list(args)

    @property
    def annotations(self):
        annot_dict = {}
        for query in self.queries:
            annot_dict.update(query.annotations)
        return annot_dict


class CombinedQuerySet:
    queries: typing.List[QuerySet] = []
    # Cache count of each queryset
    counts: typing.List[typing.Optional[int]] = []

    def __init__(self, *args):
        self.queries = list(args)
        self.counts = [None] * len(self.queries)
        if len(self.queries) == 0:
            raise NotImplementedError("Combined query must be initialized with at least one query.")

        self.query = CombinedQuery(*[query.query for query in self.queries])
        self.model = CombinedModel(*[query.model for query in self.queries])
        self.model_name = "combined"

        for query in self.queries:
            self.model_name += "_" + query.model._meta.object_name

    def get_queries(self) -> typing.Iterable[QuerySet]:
        return iter(self.queries)

    def __getitem__(self, k):
        """Implements slicing on a combined queryset.
        """
        if not isinstance(k, (int, slice)):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        if isinstance(k, slice):
            data_set = []
            start = k.start
            stop = k.stop
            stop = self.count() if stop is None else stop
            start = 0 if start is None else start

            for query_index in range(len(self.queries)):
                if stop < self.query_count(query_index):
                    data_set += self.queries[query_index][start:stop]
                    break
                if start < self.query_count(query_index):
                    data_set += self.queries[query_index][start:]
                start -= self.query_count(query_index)
                if start < 0:
                    start = 0
                stop -= self.query_count(query_index)

            return data_set[::k.step] if k.step else data_set
        else:
            relative_item_count = k
            for query_index in range(len(self.queries)):
                if relative_item_count < self.query_count(query_index):
                    return self.queries[query_index][relative_item_count]
                relative_item_count -= self.query_count(query_index)

    def query_count(self, query_index):
        if self.counts[query_index] is None:
            self.counts[query_index] = self.queries[query_index].count()
        return self.counts[query_index]

    def count(self):
        return sum((self.query_count(query_index) for query_index in range(len(self.queries))))

    def filter(self, *args, **kwargs):
        for i in range(len(self.queries)):
            filter_args = [*args, *sorted(kwargs.items())]
            self.clean_filter_args(filter_args, self.queries[i])
            self.queries[i] = self.queries[i].filter(*filter_args)
        return self

    def order_by(self, *field_names):
        for i in range(len(self.queries)):
            # collect valid fields of each model being queried and filter out any order by fields that don't exist
            model_field_names = [field.name for field in self.queries[i].model._meta.fields]
            order_field_names = filter(lambda name: name.lstrip("-") in model_field_names, [*field_names])
            self.queries[i] = self.queries[i].order_by(*order_field_names)
        return self

    def distinct(self, *field_names):
        for i in range(len(self.queries)):
            self.queries[i] = self.queries[i].distinct(*field_names)
        return self

    def get(self, *args, **kwargs):
        obj = None
        for query in self.queries:
            try:
                obj = query.get(*args, **kwargs)
            except query.model.DoesNotExist:
                obj = None
            if obj: break
        if obj is None:
            raise Http404('No %s matches the given query.' % self.model_name)
        return obj

    def clean_filter_args(self, children, query, parent: Node = None):
        """Clean queryset filter arguments of any field reference that can not be solved for that specific query.
        """
        for i in range(len(children)):
            if isinstance(children[i], Node):
                self.clean_filter_args(children[i].children, query, parent=children[i])
            else:
                arg, value = children[i]
                if not arg:
                    children[i] = ("pk__isnull", True) if parent.connector == Q.OR else ("pk__isnull", False)
                try:
                    query.query.solve_lookup_type(arg)
                except FieldError:
                    children[i] = ("pk__isnull", True) if parent.connector == Q.OR else ("pk__isnull", False)
