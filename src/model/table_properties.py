#!/usr/bin/env python3
from __future__ import annotations

from typing import List


class TableProperties:
    def __init__(self, table_properties: List[List[str]]) -> None:
        """
        Initialize a TableProperties object with the supplied properties

        :param table_properties: The table properties to set
        """

        self.table_properties = table_properties

    def __eq__(self, other: TableProperties) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other TableProperties objects.

        :returns: The boolean result of the comparison to the other object
        """

        return self.table_properties == other.table_properties

    def __ne__(self, other: TableProperties) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other TableProperties objects.

        :returns: The boolean result of the comparison to the other object
        """

        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of the
        table properties.

        :returns: The HQL-string column representation of the table properties.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table properties.

        :returns: The HQL-string format for the table properties
        """

        properties = ", ".join(
            [f"{key}={value}" for key, value in self.table_properties]
        )

        return f"TBLPROPERTIES({properties})"
