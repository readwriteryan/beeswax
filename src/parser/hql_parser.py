#!/usr/bin/env python3

from pyparsing import ParserElement, ParseResults


from src.model.model_factory import ModelFactory
from src.parser.definitions import Definitions


class HQLParser:
    """
    This class implements the parsing logic for HQL.
    """

    def get_create_table_parser(self) -> ParserElement:
        """
        This function returns the create table parser composed of the definitions
        making up the HQL components.

        :return The ParserElement object composed of the create table definitions
        """
        return (
            Definitions.CREATE_TABLE_STATEMENT
            + Definitions.COLUMN_LIST
            + Definitions.TABLE_COMMENT
            + Definitions.PARTITION
            + Definitions.TABLE_SETTINGS
            + Definitions.SEMICOLON
        )

    def parse_create_table(self, hql: str) -> ParseResults:
        """
        This function acts as a helper function that supplies the appropriate
        parser to the parse function for parsing "CREATE TABLE" statmenets.

        :return The Table object generated from the parse results.
        """

        r = self.parse(self.get_create_table_parser(), hql)

        table = ModelFactory.get_table(r)
        table.columns = ModelFactory.get_columns(r)
        table.location = ModelFactory.get_location(r)
        table.clustered_by = ModelFactory.get_clustered_by(r)
        table.skewed_by = ModelFactory.get_skewed_by(r)
        table.row_format = ModelFactory.get_row_format(r)
        table.storage = ModelFactory.get_storage(r)
        table.table_properties = ModelFactory.get_table_properties(r)

        return table

    def parse(
        self, parser: ParserElement, hql: str, parse_all: bool = True
    ) -> ParseResults:
        """
        This function accepts a parser and an HQL string to parse and returns the
        parse results.

        :raises: ParseException on failure to parse supplied HQL
        :return The ParseResults object generated
        """

        return parser.parseString(hql, parseAll=parse_all)
