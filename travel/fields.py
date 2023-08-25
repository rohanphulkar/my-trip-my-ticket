from django.db import models

class DurationField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # Adjust max length as needed
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return tuple(map(int, value.split(',')))

    def to_python(self, value):
        if isinstance(value, tuple):
            return value
        if value is None:
            return None
        return tuple(map(int, value.split(',')))

    def get_prep_value(self, value):
        if value is None:
            return None
        return f"{value[0]},{value[1]}"

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)