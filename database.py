from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


# Serializador de modelos SQLAlchemy
def add_schema(**kwgs):
    def decorator(cls):
        class Meta:
            model = cls
        schema = type("Schema", (ma.SQLAlchemyAutoSchema,), {"Meta": Meta, **kwgs})
        cls.Schema = schema
        return cls
    return decorator
