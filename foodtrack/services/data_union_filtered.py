import typing

from django.core.exceptions import FieldError
from django.db.models import QuerySet, Model, Q
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql import Query
from django.utils.tree import Node


class QuerySetUnion:
    queries: typing.List[QuerySet] = []
    union_query: typing.Optional[QuerySet] = None

    def __init__(self, *args):
        """
        Union of querysets that can be filtered. Expects queryset objects that have matching field sets that have been
        set up with .values_list(...).
        Args:
            *args (List[QuerySet]): queryset objects.
        """
        self.queries = list(args)
        field_count = None
        for _query in self.queries:
            if field_count is None:
                field_count = len(_query._fields)
            elif field_count != len(_query._fields):
                raise FieldError("Inconsistent field count on query arguments. Set the exact same number and type of "
                                 "fields on the querysets to be joined using .values_list(...)")
        self.union_query = None
        if len(self.queries) == 0:
            raise NotImplementedError("Combined query must be initialized with at least one query.")

    def get_queries(self) -> typing.Iterable[QuerySet]:
        return iter(self.queries)

    def get_union(self) -> QuerySet:
        if self.union_query is None:
            for _query in self.queries:
                if self.union_query is None:
                    self.union_query = _query
                else:
                    self.union_query = self.union_query.union(_query)
        return self.union_query

    @property
    def query(self) -> Query:
        return self.get_union().query

    @property
    def model(self) -> Model:
        return self.get_union().model

    def __getitem__(self, k):
        return self.get_union().__getitem__(k)

    def count(self):
        return self.get_union().count()

    def filter(self, *args, **kwargs):
        for i in range(len(self.queries)):
            filter_args = [*args, *sorted(kwargs.items())]
            self.clean_filter_args(filter_args, self.queries[i])
            self.queries[i] = self.queries[i].filter(*filter_args)
        # Reset union so it gets redone now that the member querysets are filtered
        self.union_query = None
        return self

    def order_by(self, *field_names):
        self.union_query = self.get_union().order_by(*field_names)
        return self

    def distinct(self, *field_names):
        self.union_query = self.get_union().distinct(*field_names)
        return self

    def clean_filter_args(self, children, _query, parent: Node = None):
        """
        Clean queryset filter arguments of any field reference that can not be solved for that specific query.
        Args:
            children (List): list of parameters for the filter. Tuple with lookup, value or Q objects
            _query (QuerySet): actual query that is supposed to receive the parameters for filtering
            parent (Node): Q object node that refers back to the parent Q object when traversing recursively

        Returns:
            None (modifies the list of children passed in as reference)
        """
        for i in range(len(children)):
            if isinstance(children[i], Node):
                self.clean_filter_args(children[i].children, _query, parent=children[i])
            else:
                arg, value = children[i]
                if not arg:
                    children[i] = ("pk__isnull", True) if parent.connector == Q.OR else ("pk__isnull", False)
                field_name = arg.split(LOOKUP_SEP)[0]
                if field_name not in _query._fields:
                    field_index = self._get_field_index(field_name)
                    field_name = _query._fields[field_index]
                    arg = LOOKUP_SEP.join([field_name] + arg.split(LOOKUP_SEP)[1:])
                    children[i] = arg, value

    def _get_field_index(self, field_name):
        for _query in self.queries:
            if field_name in _query._fields:
                return _query._fields.index(field_name)
        return None
