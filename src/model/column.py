#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Optional, Union

from src.hql.hql_type import HQLType


class Column:
    """
    This class is used to model the representation of a column on a Hive table.
    """

    def __init__(
        self,
        name: str,
        type: Union[str, List[List[str]]],
        length: Optional[str],
        comment: Optional[str],
    ) -> None:
        self.name: str = name
        self.type: Union[str, List[List[str]]] = type
        self.length: Optional[str] = length
        self.comment: Optional[str] = comment

    def __eq__(self, other: Optional[Column]) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other Column objects.

        :returns: The boolean result of the comparison to the other object
        """
        if other is None or not isinstance(other, Column):
            return False

        return (self.name, self.type, self.length, self.comment) == (
            other.name,
            other.type,
            other.length,
            other.comment,
        )

    def __hash__(self) -> int:
        """
        This function implements the magic method to make this object hashable.

        :returns: The integer hash output for this object
        """
        return hash((self.name, self.type_def, self.length, self.comment))

    def __ne__(self, other: Column) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other Column objects.

        :returns: The boolean result of the comparison to the other object
        """

        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best we can do here is the HQL from which this object could be
        recreated, so this returns the HQL representation of the column.

        :returns: The HQL-string column representation of the column
        """

        return self.hql

    @property
    def comment_def(self) -> str:
        """
        This function acts as a property that returns the comment definition for the
        column in HQL-string format.

        :returns: The HQL-string column comment definition
        """

        return f"COMMENT {self.comment}" if self.comment else ""

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format
        representation of this column.

        :returns: The HQL-string representation of this column
        """
        return f"`{self.name}` {self.type_def} {self.comment_def}"

    @property
    def length_def(self) -> str:
        """
        This function acts as a property that returns the length definition for the
        column in HQL-string format.

        :returns: The HQL-string column length definition
        """

        return f"({self.length})" if self.length else ""

    @property
    def type_def(self) -> str:
        """
        This function acts as a property that returns the column's type definition in
        HQL-string format.

        :returns: The HQL-string representation of this column's type
        """

        if isinstance(self.type, list):
            return HQLType.generate(self.type)
        else:
            return f"{self.type}{self.length_def}"
