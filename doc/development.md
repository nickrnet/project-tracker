# Development Practices

We have a concept of not deleting information or updating it in-place.

The `core/models/user.py` classes demonstrate this by referencing `CoreModel` as the base class for all models, which contains a foreign key to a `Deleted` object.

To comply with not deleting data, each model should have a corresponding `Data` class with a `current` on the object, in order to prevent live updates or deletes. This means instead of performing `record.objects.update(**data)`, we create a new `Data`, and link it to the related record. See `frontend/views/core/user/user_view.py` where a POST is handled for an example.

See the [Project Structure](project_structure.md) documentation for filesystem layout.

## Python Modules

If additional Python modules are required, use pipenv to install them:

```shell
cd <path to checkout>
pipenv install <module(s)>
```

This places the module in the Pipfile and Pipfile.lock to be included during a `pipenv install` command. These files should be committed to source control.

### TODO

Provide an environment file containing variables for cloud storage, database connection, etc. Document as we get there.
