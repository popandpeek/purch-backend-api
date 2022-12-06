"""Api extension initialization
Override base classes here to allow painless customization in the future.
"""
from flask_smorest import Api as ApiOrig, Blueprint as BlueprintOrig, Page
from marshmallow import post_dump, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from extensions.database import ma


class Blueprint(BlueprintOrig):
    """Blueprint override"""


class Api(ApiOrig):
    """Api override"""

    def __init__(self, app=None, *, spec_kwargs=None):
        super().__init__(app, spec_kwargs=spec_kwargs)


class Schema(ma.Schema):
    """Schema override"""


class AutoSchema(SQLAlchemyAutoSchema):
    """SQLAlchemyAutoSchema override"""

    class Meta:
        include_fk = True
    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            # work-around to skip fields with None value
            if data.get(name) is not None:
                setattr(obj, name, data.get(name))

    # FIXME: This does not respect allow_none fields
    @post_dump
    def remove_none_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if value is not None
        }


class SQLCursorPage(Page):
    """SQL cursor pager"""
    @property
    def item_count(self):
        return self.collection.count()
