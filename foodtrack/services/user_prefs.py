import datetime
from typing import Type

from django.db.models import Model
from django.forms import Form, DateField, DateTimeField

from foodtrack.models import UserPreference


def json_simplify(obj):
    if isinstance(obj, Model):
        return obj.pk
    if isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    return obj


def save_form_preference(form: Type[Form], data: dict, user_id: Type[int]):
    # TODO: Implement a model cache for user preferences in the future
    user_pref, created = UserPreference.objects.get_or_create(pk=user_id)
    form_name = form.__name__.lower()
    if "forms" not in user_pref.prefs:
        user_pref.prefs["forms"] = {}
    if form_name not in user_pref.prefs["forms"]:
        user_pref.prefs["forms"][form_name] = {}
    if hasattr(form, "prefs"):
        field_set = [(k,v) for k,v in form.base_fields.items() if k in form.prefs.fields]
    else:
        field_set = [(k,v) for k,v in form.base_fields.items()]
    for field_name, field in field_set:
        user_pref.prefs["forms"][form_name][field_name] = json_simplify(data[field_name])
    user_pref.save()


def load_form_preference(form: Type[Form], user_id: Type[int]):
    user_pref, created = UserPreference.objects.get_or_create(pk=user_id)
    form_name = form.__name__.lower()
    if "forms" not in user_pref.prefs:
        return {}
    if form_name not in user_pref.prefs["forms"]:
        return {}
    result = {}
    if hasattr(form, "prefs"):
        field_set = [(k,v) for k,v in form.base_fields.items() if k in form.prefs.fields]
    else:
        field_set = [(k,v) for k,v in form.base_fields.items()]
    for field_name, field in field_set:
        if field_name in user_pref.prefs["forms"][form_name]:
            if type(field) is DateField:
                result[field_name] = datetime.datetime.strptime(user_pref.prefs["forms"][form_name][field_name], "%Y-%m-%d").date()
            elif type(field) is DateTimeField:
                result[field_name] = datetime.datetime.strptime(user_pref.prefs["forms"][form_name][field_name],
                                                          "%Y-%m-%d %H:%M:%S")
            else:
                result[field_name] = user_pref.prefs["forms"][form_name][field_name]
    return result
