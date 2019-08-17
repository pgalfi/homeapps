import datetime
from typing import Type

from django.db.models import Model, DateTimeField, DateField

from foodtrack.models import UserPreference


def set_preferences(source: dict, path: str = None, destination: dict = None):
    if destination is None:
        destination = {}
    if "user_preference" not in source or source["user_preference"] is None:
        return destination
    key_path = path.split("/")  # break down a key1/key2/key3 path
    src_dict = source.pop("user_preference").prefs
    for path_part in key_path:
        src_dict = src_dict[path_part]
    for k, v in src_dict.items():
        destination[k] = v
    return destination


def save_preference(model_instance: Model, user_id: Type[int]):
    # TODO: Implement a model cache for user preferences in the future
    user_pref, created = UserPreference.objects.get_or_create(pk=user_id)
    model_name = model_instance.__class__.__name__.lower()
    if "models" not in user_pref.prefs:
        user_pref.prefs["models"] = {}
    if model_name not in user_pref.prefs["models"]:
        user_pref.prefs["models"][model_name] = {}
    if hasattr(model_instance, "Prefs") and hasattr(model_instance.Prefs, "fields"):
        field_names = model_instance.Prefs.fields
    else:
        field_names = [field.name for field in model_instance._meta.get_fields()]
    for name in field_names:
        field = model_instance._meta.get_field(name)
        if type(field) is DateField:
            user_pref.prefs["models"][model_name][name] = datetime.date.strftime(getattr(model_instance, name),
                                                                                 "%Y-%m-%d")
        elif type(field) is DateTimeField:
            user_pref.prefs["models"][model_name][name] = datetime.date.strftime(getattr(model_instance, name),
                                                                                 "%Y-%m-%d %H:%M:%S")
        else:
            user_pref.prefs["models"][model_name][name] = getattr(model_instance, name)
    user_pref.save()


def load_preference(model_class: Model.__class__, user_id: Type[int]):
    user_pref, created = UserPreference.objects.get_or_create(pk=user_id)
    model_name = model_class.__name__.lower()
    if "models" not in user_pref.prefs:
        return {}
    if model_name not in user_pref.prefs["models"]:
        return {}
    result = {}
    if hasattr(model_class, "Prefs") and hasattr(model_class.Prefs, "fields"):
        field_names = model_class.Prefs.fields
    else:
        field_names = [field.name for field in model_class._meta.get_fields()]
    for name in field_names:
        if name in user_pref.prefs["models"][model_name]:
            field = model_class._meta.get_field(name)
            if type(field) is DateField:
                result[name] = datetime.datetime.strptime(user_pref.prefs["models"][model_name][name], "%Y-%m-%d")
            elif type(field) is DateTimeField:
                result[name] = datetime.datetime.strptime(user_pref.prefs["models"][model_name][name],
                                                          "%Y-%m-%d %H:%M:%S")
            else:
                result[name] = user_pref.prefs["models"][model_name][name]
    return result
