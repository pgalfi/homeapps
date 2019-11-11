from django.db import connection
from rest_framework.views import APIView


class PerformanceCheckMixin(APIView):

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        for query in connection.queries:
            print(query)
        print(len(connection.queries))
        return response