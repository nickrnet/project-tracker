# Development Practices

We have a concept of not deleting information or updating it in-place.

The `core/models/user.py` classes demonstrate this by referencing `CoreModel` as the base class for all models.

Each model should have a corresponding `Data` class with a `current` on the object, in order to prevent live updates or deletes. This means instead of performing `record.objects.update(**data)`, we create a new `Data`, and link it to the related record.
