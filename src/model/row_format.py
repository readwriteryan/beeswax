#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Optional


class RowFormat:
    def __init__(
        self,
        row_format: str,
        fields_terminated_by: Optional[str] = None,
        escaped_by: Optional[str] = None,
        collection_items_terminated_by: Optional[str] = None,
        map_keys_terminated_by: Optional[str] = None,
        lines_terminated_by: Optional[str] = None,
        null_defined_as: Optional[str] = None,
        serde: Optional[str] = None,
        serde_properties: Optional[List[List[str]]] = None,
    ) -> None:
        """
        Initialize a RowFormat object with the supplied settings

        :param row_format: The row format string identifier
        :param fields_terminated_by: The field termination delimiter
        :param escaped_by: The field escape delimiter
        :param collection_items_terminated_by: The collection item delimiter
        :param map_keys_terminated_by: The map key delimiter
        :param lines_terminated_by: The line terminated delimiter
        :param null_defined_as: The null definition character
        :param serde_properties: Serdeproperties supplied as a list of [key, val] pairs
        """

        self.row_format = row_format
        self.fields_terminated_by = fields_terminated_by
        self.escaped_by = escaped_by
        self.collection_items_terminated_by = collection_items_terminated_by
        self.map_keys_terminated_by = map_keys_terminated_by
        self.lines_terminated_by = lines_terminated_by
        self.null_defined_as = null_defined_as
        self.serde = serde
        self.serde_properties = serde_properties

    def __eq__(self, other: RowFormat) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other RowFormat objects.

        :returns: The boolean result of the comparison to the other object
        """

        return (
            self.row_format,
            self.fields_terminated_by,
            self.escaped_by,
            self.collection_items_terminated_by,
            self.map_keys_terminated_by,
            self.lines_terminated_by,
            self.null_defined_as,
            self.serde,
            self.serde_properties,
        ) == (
            other.row_format,
            other.fields_terminated_by,
            other.escaped_by,
            other.collection_items_terminated_by,
            other.map_keys_terminated_by,
            other.lines_terminated_by,
            other.null_defined_as,
            other.serde,
            other.serde_properties,
        )

    def __ne__(self, other: RowFormat) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other RowFormat objects.

        :returns: The boolean result of the comparison to the other object
        """

        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of this
        storage format.

        :returns: The HQL-string column representation of the row format.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table row format.

        :returns: The HQL-string format for the row format
        """
        if self.row_format == "DELIMITED":
            fields_terminated_by = (
                (f"FIELDS TERMINATED BY {self.fields_terminated_by} ")
                if self.fields_terminated_by
                else ""
            )
            escaped_by = f"ESCAPED BY {self.escaped_by} " if self.escaped_by else ""
            collection_items_terminated_by = (
                (
                    f"COLLECTION ITEMS TERMINATED BY "
                    f"{self.collection_items_terminated_by}"
                )
                if self.collection_items_terminated_by
                else ""
            )
            map_keys_terminated_by = (
                (f"MAP KEYS TERMINATED BY {self.map_keys_terminated_by} ")
                if self.map_keys_terminated_by
                else ""
            )
            lines_terminated_by = (
                (f"LINES TERMINATED BY {self.lines_terminated_by} ")
                if self.lines_terminated_by
                else ""
            )
            null_defined_as = (
                (f"NULL DEFINED AS {self.null_defined_as} ")
                if self.null_defined_as
                else ""
            )

            return (
                f"ROW FORMAT {self.row_format} {fields_terminated_by}{escaped_by}"
                f"{collection_items_terminated_by}{map_keys_terminated_by}"
                f"{lines_terminated_by}{null_defined_as}"
            )

        elif self.row_format == "SERDE":
            with_properties = ""
            if self.serde_properties:
                properties = ", ".join(
                    [f"{key}={value}" for key, value in self.serde_properties]
                )
                with_properties = f" WITH SERDEPROPERTIES({properties})"

            return f"ROW FORMAT {self.row_format} {self.serde}{with_properties}"
