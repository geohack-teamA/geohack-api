from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import INTEGER, TIMESTAMP

Base = declarative_base()


class BaseModel(Base):
    """base model"""

    __abstract__ = True

    id = Column(INTEGER, primary_key=True, autoincrement=True)

    created_at = Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment="created at",
    )

    updated_at = Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
        comment="updated at",
    )

    @declared_attr
    def __mapper_args__(cls):
        return {"order_by": "id"}
