#!/usr/bin/env python3

from collections import OrderedDict
from pyparsing import ParseResults
from typing import Dict, List, Optional

from src.model.clustered_by import ClusteredBy
from src.model.column import Column
from src.model.location import Location
from src.model.row_format import RowFormat
from src.model.skewed_by import SkewedBy
from src.model.storage import Storage
from src.model.table import Table
from src.model.table_properties import TableProperties


class ModelFactory:
    """
    This class is responsible for generating valid model objects from the results
    generated by the HQL parser.
    """

    @staticmethod
    def get_clustered_by(parse_results: ParseResults) -> Optional[ClusteredBy]:
        """
        This factory method accepts the parser results for a column and returns a
        ClusteredBy object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The ClusteredBy object if clustered by is set, else None
        """
        if not parse_results.clustered_by:
            return None

        clustered_by_cols = parse_results.clustered_by_cols.pop().asList()
        buckets = int(parse_results.buckets.pop())
        sorted_by = (
            parse_results.sorted_by.pop().asList() if parse_results.sorted_by else None
        )

        return ClusteredBy(clustered_by_cols, buckets, sorted_by)

    @staticmethod
    def get_columns(parse_results: ParseResults) -> Dict[str, Column]:
        """
        This factory method accepts the parser results for a column and returns an
        OrderedDict of Column objects generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The OrderedDict of Column objects generated from the parser results
        """
        return OrderedDict(
            [
                (c.column_name, ModelFactory.get_column(c))
                for c in parse_results.column_list
            ]
        )

    @staticmethod
    def get_column(parse_results: ParseResults) -> Column:
        """
        This factory method accepts the parser results for a column and returns a
        Column object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The Column object generated from the parser results
        """

        name: str = parse_results.column_name
        type: str = (
            parse_results.column_type.asList()
            if isinstance(parse_results.column_type, ParseResults)
            else parse_results.column_type
        )
        length: Optional[str] = (parse_results.length if parse_results.length else None)
        comment: Optional[str] = (
            parse_results.comment if parse_results.comment else None
        )

        return Column(name, type, length, comment)

    @staticmethod
    def get_location(parse_results: ParseResults) -> Optional[Location]:
        """
        This factory method accepts the parser results for location and returns a
        Location object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The Location object if location is set, else None
        """

        return Location(parse_results.location) if parse_results.location else None

    @staticmethod
    def get_row_format(parse_results: ParseResults) -> Optional[RowFormat]:
        """
        This factory method accepts the parser results for row format and returns a
        RowFormat object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The RowFormat object if row format is set, else None
        """
        if not parse_results.row_format:
            return None

        if parse_results.row_format_delimited:
            row_format: str = "DELIMITED"
            fields_terminated_by: Optional[str] = (
                parse_results.fields_terminated_by[0]
                if parse_results.fields_terminated_by
                else None
            )
            escaped_by: Optional[str] = (
                parse_results.escaped_by[0] if parse_results.escaped_by else None
            )
            collection_items_terminated_by: Optional[str] = (
                parse_results.collection_items_terminated_by[0]
                if parse_results.collection_items_terminated_by
                else None
            )
            map_keys_terminated_by: Optional[str] = (
                parse_results.map_keys_terminated_by[0]
                if parse_results.map_keys_terminated_by
                else None
            )
            lines_terminated_by: Optional[str] = (
                parse_results.lines_terminated_by[0]
                if parse_results.lines_terminated_by
                else None
            )
            null_defined_as: Optional[str] = (
                parse_results.null_defined_as[0]
                if parse_results.null_defined_as
                else None
            )

            return RowFormat(
                row_format,
                fields_terminated_by=fields_terminated_by,
                escaped_by=escaped_by,
                collection_items_terminated_by=collection_items_terminated_by,
                map_keys_terminated_by=map_keys_terminated_by,
                lines_terminated_by=lines_terminated_by,
                null_defined_as=null_defined_as,
            )

        elif parse_results.row_format_serde:
            row_format: str = "SERDE"
            serde: str = parse_results.row_format_serde[0]
            serde_properties: Optional[List[List[str]]] = (
                parse_results.row_format_serde[1].asList()
                if len(parse_results.row_format_serde) > 1
                else None
            )

            return RowFormat(row_format, serde=serde, serde_properties=serde_properties)

    @staticmethod
    def get_skewed_by(parse_results: ParseResults) -> Optional[SkewedBy]:
        """
        This factory method accepts the parser results for skewed_by and returns
        a SkewedBy object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The SkewedBy object if skewed by is set, else None
        """
        if not parse_results.skewed_by:
            return None

        columns = parse_results.skewed_by_columns.asList()
        values = parse_results.skewed_by_values.asList()
        stored_as_directories = parse_results.stored_as_directories != ""

        return SkewedBy(columns, values, stored_as_directories)

    @staticmethod
    def get_storage(parse_results: ParseResults) -> Optional[Storage]:
        """
        This factory method accepts the parser results for storage and returns a
        Storage object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The Storage object if storage is set, else None
        """
        if not parse_results.storage:
            return None

        if parse_results.stored_as:
            storage = parse_results.stored_as.pop()
            storage_qualifier = "AS"
            serde_properties = None
        elif parse_results.stored_by:
            storage_qualifier = "BY"
            if len(parse_results.stored_by) > 1:
                storage, serde_properties = parse_results.stored_by
            else:
                storage = parse_results.stored_by.pop()
                serde_properties = None

        return Storage(storage, storage_qualifier, serde_properties.asList())

    @staticmethod
    def get_table(parse_results: ParseResults) -> Table:
        """
        This factory method accepts the parser results for a table and returns a
        Table object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The Table object generated from the parser results
        """

        name: str = parse_results.table_name
        modifier: Optional[str] = (
            parse_results.table_modifier if parse_results.table_modifier else None
        )
        comment: Optional[str] = (
            parse_results.comment if parse_results.comment else None
        )
        partition: Optional[List[List[str]]] = (
            parse_results.partition.asList() if parse_results.partition else None
        )

        return Table(name, modifier, comment, partition)

    @staticmethod
    def get_table_properties(parse_results: ParseResults) -> Optional[TableProperties]:
        """
        This factory method accepts the parser results for table properties and returns
        TableProperties object generated from the results.

        :param parse_results: The results object generated by the HQL parser
        :returns: The TableProperties object if location is set, else None
        """

        return (
            TableProperties(parse_results.properties.asList())
            if parse_results.properties
            else None
        )
