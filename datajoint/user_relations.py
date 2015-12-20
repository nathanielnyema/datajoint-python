"""
Hosts the table tiers, user relations should be derived from.
"""

from .base_relation import BaseRelation
from .autopopulate import AutoPopulate
from .utils import from_camel_case
from . import DataJointError


class classproperty:

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


class UserRelation(BaseRelation):

    @classproperty
    def full_table_name(cls):
        return r"`{0:s}`.`{1:s}`".format(cls.database, cls.table_name)


class Part(UserRelation):
    """
    Inherit from this class if the table's values are details of an entry in another relation
    and if this table is populated by this relation. For example, the entries inheriting from
    dj.Part could be single entries of a matrix, while the parent table refers to the entire matrix.
    Part relations are implemented as classes inside classes.
    """
    _master = None

    @classproperty
    def master(cls):
        return cls._master

    @classproperty
    def table_name(cls):
        return cls.master.table_name + '__' + from_camel_case(cls.__name__)


class Manual(UserRelation):
    """
    Inherit from this class if the table's values are entered manually.
    """

    @classproperty
    def table_name(cls):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return from_camel_case(cls.__name__)


class Lookup(UserRelation):
    """
    Inherit from this class if the table's values are for lookup. This is
    currently equivalent to defining the table as Manual and serves semantic
    purposes only.
    """

    @classproperty
    def table_name(cls):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return '#' + from_camel_case(cls.__name__)

    def _prepare(self):
        """
        Checks whether the instance has a property called `contents` and inserts its elements.
        """
        if hasattr(self, 'contents'):
            self.insert(self.contents, skip_duplicates=True)


class Imported(UserRelation, AutoPopulate):
    """
    Inherit from this class if the table's values are imported from external data sources.
    The inherited class must at least provide the function `_make_tuples`.
    """

    @classproperty
    def table_name(cls):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return "_" + from_camel_case(cls.__name__)


class Computed(UserRelation, AutoPopulate):
    """
    Inherit from this class if the table's values are computed from other relations in the schema.
    The inherited class must at least provide the function `_make_tuples`.
    """

    @classproperty
    def table_name(cls):
        """
        :returns: the table name of the table formatted for mysql.
        """
        return "__" + from_camel_case(cls.__name__)
