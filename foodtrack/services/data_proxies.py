import typing

from django.apps import apps
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Model

from foodtrack.models import UsageCounter


def create_usage_proxy(owner_id: int, base_model: typing.Type[Model]) -> typing.Type[Model]:
    """
    Creates a Proxy Model based on the base model provided that includes a usage field. The relevant usage counter
    object is then joined in including the owner_id provided.
    Args:
        owner_id (int): ID of the owner that the usage is to be included for
        base_model (): actual model that usage data is being attached to

    Returns:
        Model class that is a proxy of the original base Model with an additional usage field that is UsageCounter
    """

    # Remove proxy model from the registry to avoid runtime warning
    model_name = "proxymodel"
    app_name = "foodtrack"
    if model_name in apps.all_models[app_name]:
        del apps.all_models[app_name][model_name]

    class GenericRelationOwnerRelated(GenericRelation):

        def get_extra_restriction(self, where_class, alias, remote_alias):
            cond = super().get_extra_restriction(where_class, alias, remote_alias)
            field = self.remote_field.model._meta.get_field("owner")
            lookup = field.get_lookup('exact')(field.get_col(remote_alias), owner_id)
            cond.add(lookup, "AND")
            return cond

    class ProxyModel(base_model):
        usage = GenericRelationOwnerRelated(UsageCounter)

        class Meta:
            proxy = True

    return ProxyModel