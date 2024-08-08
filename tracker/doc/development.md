# Development Practices

We have a concept of not deleting information or updating it in-place.

The `core/models/user.py` classes demonstrate this by referencing `CoreModel` as the base class for all models.

Each model should have a corresponding `Data` class, and instead of performing `record.update(**data)`, we create a new `Data`, and link it to the related record.
