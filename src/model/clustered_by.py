#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Optional


class ClusteredBy:
    def __init__(
        self, columns: List[str], buckets: int, sorted_by: Optional[List[List[str]]]
    ) -> None:
        """
        Initialize a ClusteredBy object with a specified location

        :param columns: The list of columns on which the tables is clustered
        :param buckets: The number of buckets into which the table is bucketed
        :param sorted_by: The columns on which the clustering is sorted by
        """

        self.columns = columns
        self.buckets = buckets
        self.sorted_by = sorted_by

    def __eq__(self, other: ClusteredBy) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other ClusteredBy objects.

        :returns: The boolean result of the comparison to the other object
        """

        return (self.columns, self.buckets, self.sorted_by) == (
            other.columns,
            other.buckets,
            other.sorted_by,
        )

    def __ne__(self, other: ClusteredBy) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other ClusteredBy objects.

        :returns: The boolean result of the comparison to the other object
        """

        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of this
        clustered by clause.

        :returns: The HQL-string column representation of the location.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table clustered by clause.

        :returns: The HQL-string format for the table clustered by clause
        """

        column_def = "(" + ", ".join([f"`{col}`" for col in self.columns]) + ")"
        bucket_def = f"INTO {self.buckets} BUCKETS"
        sorted_def = ""
        if self.sorted_by:
            sorted_def = " SORTED BY ("
            for idx, sort in enumerate(self.sorted_by):
                comma = ", " if idx > 0 else ""

                if len(sort) == 2:
                    col, order = sort
                    sorted_def += f"{comma}`{col}` {order}"
                elif len(sort) == 1:
                    col = sort[0]
                    sorted_def += f"{comma}`{col}`"
            sorted_def += ")"

        return f"CLUSTERED BY {column_def}{sorted_def} {bucket_def}"
