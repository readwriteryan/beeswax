#!/usr/bin/env python3
from __future__ import annotations

from typing import List, Optional


class Storage:
    def __init__(
        self,
        storage: str,
        storage_qualifier: str,
        serde_properties: Optional[List[List[str]]],
    ) -> None:
        """
        Initialize a Storage object with the supplied settings

        :param storage: The storage format associated with this object
        :param storage_qualifier: "AS" or "BY"
        :param serdeproperties: Serdeproperties supplied as a list of [key, val] pairs
        """

        self.storage = storage
        self.storage_qualifier = storage_qualifier
        self.serde_properties = serde_properties

    def __eq__(self, other: Storage) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other Storage objects.

        :returns: The boolean result of the comparison to the other object
        """

        return (self.storage, self.storage_qualifier, self.serde_properties) == (
            other.storage,
            other.storage_qualifier,
            other.serde_properties,
        )

    def __hash__(self) -> int:
        """
        This function implements the magic method to make this object hashable.

        :returns: The integer hash output for this object
        """
        return hash((self.storage, self.storage_qualifier, self.serde_properties))

    def __ne__(self, other: Storage) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other Storage objects.

        :returns: The boolean result of the comparison to the other object
        """

        return not (self == other)

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of this
        storage format.

        :returns: The HQL-string column representation of the storage format.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table storage format.

        :returns: The HQL-string format for the storage format
        """
        with_properties = ""
        if self.serde_properties:
            properties = ", ".join(
                [f"{key}={value}" for key, value in self.serde_properties]
            )
            with_properties = f" WITH SERDEPROPERTIES({properties})"

        return f"STORED {self.storage_qualifier} {self.storage}{with_properties}"
