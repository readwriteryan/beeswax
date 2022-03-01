#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Union


class SkewedBy:
    def __init__(
        self,
        columns: List[str],
        values: Union[List[str], List[List[str]]],
        stored_as_directories: bool,
    ) -> None:
        """
        Initialize a SkewedBy object with a specified properties

        :param columns: The list of columns on which the tables is skewed
        :param values: The list of values on which each column is skewed
        :param stored_as_directories: Boolean representing stored as directories opt
        """

        self.columns: List[str] = columns
        self.values: Union[List[str], List[List[str]]] = values
        self.stored_as_directories: bool = stored_as_directories

    def __eq__(self, other: SkewedBy) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other SkewedBy objects.

        :returns: The boolean result of the comparison to the other object
        """
        return (self.columns, self.values, self.stored_as_directories) == (
            other.columns,
            other.values,
            other.stored_as_directories,
        )

    def __hash__(self) -> int:
        """
        This function implements the magic method to make this object hashable.

        :returns: The integer hash output for this object
        """
        return hash((self.columns, self.values, self.stored_as_directories))

    def __ne__(self, other: SkewedBy) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other SkewedBy objects.

        :returns: The boolean result of the comparison to the other object
        """
        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of the
        table's skewed by clause.

        :returns: The HQL-string column representation of the skewed by clause.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table skewed by clause.

        :returns: The HQL-string format for the table skewed by clause
        """

        columns = "(" + ", ".join([f"`{col}`" for col in self.columns]) + ")"
        stored_as_directories = (
            " STORED AS DIRECTORIES" if self.stored_as_directories else ""
        )

        if isinstance(self.values[0], list):
            values = ", ".join(
                [("(" + ", ".join([str(v) for v in l]) + ")") for l in self.values]
            )
        else:
            values = ", ".join([str(v) for v in self.values])

        return f"SKEWED BY {columns} ON ({values}){stored_as_directories}"
