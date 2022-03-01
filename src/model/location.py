#!/usr/bin/env python3
from __future__ import annotations


class Location:
    def __init__(self, location: str) -> None:
        """
        Initialize a location object with a specified location

        :param location: The location string to which to set the location field
        """

        self.location = location

    def __eq__(self, other: Location) -> bool:
        """
        This function implements the magic method for the equal operator so that this
        object may be easily compared to other Location objects.

        :returns: The boolean result of the comparison to the other object
        """

        return self.location == other.location

    def __hash__(self) -> int:
        """
        This function implements the magic method to make this object hashable.

        :returns: The integer hash output for this object
        """
        return hash(self.location)

    def __ne__(self, other: Location) -> bool:
        """
        This function implements the magic method for the not equals operator so that
        this object may be easily compared to other Location objects.

        :returns: The boolean result of the comparison to the other object
        """
        if other is None or not isinstance(other, Location):
            return False

        return self.location != other.location

    def __repr__(self) -> str:
        """
        This function implements the magic method to define the representation of this
        object. The best representation for this object is the HQL from which this
        object could be recreated, so this returns the HQL representation of this
        location.

        :returns: The HQL-string column representation of the location.
        """

        return self.hql

    @property
    def hql(self) -> str:
        """
        This function acts as a property that returns the HQL-string format for the
        table location.

        :returns: The HQL-string format for the table location
        """

        return f"LOCATION {self.location}"
