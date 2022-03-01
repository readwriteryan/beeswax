#!/usr/bin/env python3

from functools import reduce
from pyparsing import (
    alphanums,
    CaselessKeyword,
    CaselessLiteral,
    Combine,
    Forward,
    Group,
    Literal,
    nums,
    Optional,
    pyparsing_common,
    QuotedString,
    Word,
    ZeroOrMore,
)


class Definitions:
    """
    This class defines a set of constants containing the BNF rule definitions for HQL's
    CREATE TABLE statement. These rules are translated from the grammar defined for Hive
    through version 1.1.0.

    TODO: Support for recent additions to HQL Create Table for newer versions of Hive.
    """

    INTEGER_TYPES = ["BIGINT", "INT", "INTEGER", "SMALLINT", "TINYINT"]
    FLOAT_TYPES = ["DOUBLE", "FLOAT"]
    DECIMAL_TYPES = ["DECIMAL", "NUMERIC"]
    SIMPLE_TYPES = ["BINARY", "BOOLEAN", "DATE", "INTERVAL", "STRING", "TIMESTAMP"]
    CHAR_TYPES = ["CHAR", "VARCHAR"]
    COMPLEX_TYPES = ["ARRAY", "MAP", "STRUCT", "UNION"]
    ALL_TYPES = (
        INTEGER_TYPES
        + FLOAT_TYPES
        + DECIMAL_TYPES
        + SIMPLE_TYPES
        + CHAR_TYPES
        + COMPLEX_TYPES
    )

    # Base grammer constructs
    WORD_CREATE = CaselessLiteral("CREATE").suppress()
    WORD_TEMPORARY = CaselessLiteral("TEMPORARY")
    WORD_EXTERNAL = CaselessLiteral("EXTERNAL")
    WORD_TABLE = CaselessLiteral("TABLE").suppress()
    COMMA = Literal(",").suppress()
    COLON = Literal(":").suppress()
    SEMICOLON = Optional(Literal(";").suppress())
    LEFT_PARENTHESIS = Literal("(").suppress()
    RIGHT_PARENTHESIS = Literal(")").suppress()
    LESS_THAN = Literal("<").suppress()
    GREATER_THAN = Literal(">").suppress()
    EQUALS = Literal("=").suppress()
    QUOTE = Literal("'") | Literal('"')
    BACK_QUOTE = Optional(Literal("`")).suppress()
    LENGTH = Word(nums)
    OBJECT_NAME = Word(alphanums + "_" + "-")
    QUOTED_STRING_WITH_QUOTE = QuotedString(
        quoteChar="'", escQuote="''", escChar="\\", multiline=True, unquoteResults=False
    ) | QuotedString(
        quoteChar='"', escQuote='""', escChar="\\", multiline=True, unquoteResults=False
    )
    QUOTED_STRING = QuotedString(
        quoteChar="'", escQuote="''", escChar="\\", multiline=True
    ) | QuotedString(quoteChar='"', escQuote='""', escChar="\\", multiline=True)

    KEY_VALUE_PAIR = Group(QUOTED_STRING_WITH_QUOTE + EQUALS + QUOTED_STRING_WITH_QUOTE)

    # ==== Create Table Statement ====
    # Matches:
    # CREATE [EXTERNAL|TEMPORARY] TABLE IF NOT EXISTS `x`
    TABLE_NAME = (
        QuotedString(quoteChar="`", escQuote="``", escChar="\\", unquoteResults=True)
        | OBJECT_NAME
    )("table_name")
    TABLE_MODIFIER = Optional(WORD_EXTERNAL | WORD_TEMPORARY)("table_modifier")
    IF_NOT_EXIST = Optional(
        CaselessLiteral("IF") + CaselessLiteral("NOT") + CaselessLiteral("EXISTS")
    ).suppress()
    CREATE_TABLE_STATEMENT = (
        WORD_CREATE + Optional(TABLE_MODIFIER) + WORD_TABLE + IF_NOT_EXIST + TABLE_NAME
    )

    # ==== Column Definitions ===
    # Matches:
    # (`id` int, `name` string, `json` map<string, string>)
    COLUMN_NAME = (
        QuotedString(quoteChar="`", escQuote="``", escChar="\\", unquoteResults=True)
        | OBJECT_NAME
    )("column_name")
    COLUMN_NAME_WITH_QUOTE = (
        QuotedString(quoteChar="`", escQuote="``", escChar="\\", unquoteResults=False)
        | OBJECT_NAME
    )("column_name")
    COL_LEN = Combine(LEFT_PARENTHESIS + LENGTH + RIGHT_PARENTHESIS, adjacent=False)(
        "length"
    )
    OPTIONAL_COL_LEN = Optional(COL_LEN)
    TYPE_DECL = Forward()
    COMMENT = Combine(
        CaselessLiteral("COMMENT").suppress() + QUOTED_STRING_WITH_QUOTE, adjacent=False
    )
    COLUMN_DEF = Group(COLUMN_NAME + TYPE_DECL + Optional(COMMENT("comment")))
    COLUMN_LIST = (
        LEFT_PARENTHESIS
        + Group(COLUMN_DEF + ZeroOrMore(COMMA + COLUMN_DEF))("column_list")
        + RIGHT_PARENTHESIS
    )

    # Simple type definitions:
    INT_DEF = reduce(lambda x, y: x | y, map(CaselessLiteral, INTEGER_TYPES))(
        "column_type"
    )
    FLOAT_DEF = reduce(lambda x, y: x | y, map(CaselessLiteral, FLOAT_TYPES))(
        "column_type"
    )
    DECIMAL_TYPE = reduce(lambda x, y: x | y, map(CaselessLiteral, DECIMAL_TYPES))(
        "column_type"
    )
    DECIMAL_LEN = Combine(
        LEFT_PARENTHESIS + LENGTH + Optional(COMMA + LENGTH) + RIGHT_PARENTHESIS,
        adjacent=False,
        joinString=",",
    )("length")
    DECIMAL_DEF = DECIMAL_TYPE + Optional(DECIMAL_LEN)
    SIMPLE_DEF = reduce(lambda x, y: x | y, map(CaselessLiteral, SIMPLE_TYPES))(
        "column_type"
    )
    CHAR_TYPE = reduce(lambda x, y: x | y, map(CaselessLiteral, CHAR_TYPES))(
        "column_type"
    )
    CHAR_DEF = CHAR_TYPE + COL_LEN
    PRIMITIVE_TYPE = INT_DEF | FLOAT_DEF | DECIMAL_DEF | SIMPLE_DEF | CHAR_DEF

    # Complex type deinitions:
    ARRAY, MAP, STRUCT, UNION = map(CaselessKeyword, COMPLEX_TYPES)
    ARRAY_TYPE = Group(ARRAY - LESS_THAN + Group(TYPE_DECL) + GREATER_THAN)
    ARRAY_DEF = ARRAY_TYPE("column_type")

    MAP_TYPE = Group(
        MAP - LESS_THAN + Group(PRIMITIVE_TYPE + COMMA + TYPE_DECL) + GREATER_THAN
    )
    MAP_DEF = MAP_TYPE("column_type")

    STRUCT_COLUMN_DEF = COLUMN_NAME + COLON + TYPE_DECL + Optional(COMMENT)
    STRUCT_TYPE = Group(
        STRUCT
        - LESS_THAN
        + Group(STRUCT_COLUMN_DEF + ZeroOrMore(COMMA + STRUCT_COLUMN_DEF))
        + GREATER_THAN
    )
    STRUCT_DEF = STRUCT_TYPE("column_type")

    UNION_TYPE = Group(
        UNION
        - LESS_THAN
        + Group(TYPE_DECL + ZeroOrMore(COMMA + TYPE_DECL))
        + GREATER_THAN
    )
    UNION_DEF = UNION_TYPE("column_type")

    # Master type declaration including both simple and complex type definitions
    TYPE_DECL <<= PRIMITIVE_TYPE | ARRAY_DEF | MAP_DEF | UNION_DEF | STRUCT_DEF

    # ==== Table Comment ====
    # Matches: COMMENT 'This is an example table comment'
    TABLE_COMMENT = Optional(
        CaselessLiteral("COMMENT").suppress()
        + QUOTED_STRING_WITH_QUOTE("table_comment")
    )
    # ==== Partitions ====
    # Matches: PARTITIONED BY (ds string, ts string)
    PARTITION_LIST = Group(COLUMN_DEF + ZeroOrMore(COMMA + COLUMN_DEF))(
        "partition_list"
    )
    PARTITION = Optional(
        CaselessLiteral("PARTITIONED")
        + CaselessLiteral("BY")
        + LEFT_PARENTHESIS
        + PARTITION_LIST
        + RIGHT_PARENTHESIS
    )("partition")

    # ==== Clustered By ====
    # Matches:
    # CLUSTERED BY (`col`, `col2`) [SORTED BY (`col1` ASC, `col2` DESC) INTO 10 BUCKETS
    CLUSTERED_BY_COLS = (
        CaselessLiteral("CLUSTERED").suppress()
        + CaselessLiteral("BY").suppress()
        + LEFT_PARENTHESIS
        + Group(COLUMN_NAME + ZeroOrMore(COMMA + COLUMN_NAME))
        + RIGHT_PARENTHESIS
    )("clustered_by_cols")
    SORT_ORDER = Optional(CaselessLiteral("ASC") | CaselessLiteral("DESC"))
    COLUMN_SORT_PAIR = Group(COLUMN_NAME + SORT_ORDER)
    SORTED_BY = Optional(
        Group(
            CaselessLiteral("SORTED").suppress()
            + CaselessLiteral("BY").suppress()
            + LEFT_PARENTHESIS
            + COLUMN_SORT_PAIR
            + ZeroOrMore(COMMA + COLUMN_SORT_PAIR)
            + RIGHT_PARENTHESIS
        )
    )("sorted_by")
    NUM_BUCKETS = (
        CaselessLiteral("INTO").suppress()
        + Word(nums)
        + CaselessLiteral("BUCKETS").suppress()
    )("buckets")
    CLUSTERED_BY = (CLUSTERED_BY_COLS + SORTED_BY + NUM_BUCKETS)("clustered_by")

    # ==== SKEWED BY ====
    # Matches:
    # SKEWED BY (`col1`, `col2`) ON (('col1_val'), ('col2_val', 'col2_val2'))
    # [STORED AS DIRECTORIES]
    STORED_AS_DIRECTORIES = Combine(
        CaselessLiteral("STORED")
        + CaselessLiteral("AS")
        + CaselessLiteral("DIRECTORIES"),
        adjacent=False,
    )("stored_as_directories")
    SKEWED_BY_COLUMNS = Group(
        LEFT_PARENTHESIS
        + COLUMN_NAME
        + ZeroOrMore(COMMA + COLUMN_NAME)
        + RIGHT_PARENTHESIS
    )("skewed_by_columns")
    ARBITRARY_VALUE = pyparsing_common.number | QUOTED_STRING_WITH_QUOTE
    SKEWED_BY_VALUES_LIST = ARBITRARY_VALUE + ZeroOrMore(COMMA + ARBITRARY_VALUE)
    SKEWED_BY_VALUES_TUPLES = (
        LEFT_PARENTHESIS
        + Group(ARBITRARY_VALUE + ZeroOrMore(COMMA + ARBITRARY_VALUE))
        + RIGHT_PARENTHESIS
        + ZeroOrMore(
            COMMA
            + LEFT_PARENTHESIS
            + Group(ARBITRARY_VALUE + ZeroOrMore(COMMA + ARBITRARY_VALUE))
            + RIGHT_PARENTHESIS
        )
    )
    SKEWED_BY_VALUES = Group(
        LEFT_PARENTHESIS
        + (SKEWED_BY_VALUES_LIST | SKEWED_BY_VALUES_TUPLES)
        + RIGHT_PARENTHESIS
    )("skewed_by_values")
    SKEWED_BY = (
        CaselessLiteral("SKEWED").suppress()
        + CaselessLiteral("BY").suppress()
        + SKEWED_BY_COLUMNS
        + CaselessLiteral("ON").suppress()
        + SKEWED_BY_VALUES
        + Optional(STORED_AS_DIRECTORIES)
    )("skewed_by")

    # ==== Row Format ====
    # Matches:
    # ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
    # ROW FORMAT SERDE 'org.com.serde' WITH SERDEPROPERTIES('key'='value')
    ESCAPED_BY = (
        CaselessLiteral("ESCAPED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
    )("escaped_by")
    FIELDS_TERMINATED_BY = (
        CaselessLiteral("FIELDS").suppress()
        + CaselessLiteral("TERMINATED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
        + Optional(ESCAPED_BY)
    )("fields_terminated_by")
    COLLECTION_ITEMS_TERMINATED_BY = (
        CaselessLiteral("COLLECTION").suppress()
        + CaselessLiteral("ITEMS").suppress()
        + CaselessLiteral("TERMINATED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
    )("collection_items_terminated_by")
    MAP_KEYS_TERMINATED_BY = (
        CaselessLiteral("MAP").suppress()
        + CaselessLiteral("KEYS").suppress()
        + CaselessLiteral("TERMINATED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
    )("map_keys_terminated_by")
    LINES_TERMINATED_BY = (
        CaselessLiteral("LINES").suppress()
        + CaselessLiteral("TERMINATED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
    )("lines_terminated_by")
    NULL_DEFINED_AS = (
        CaselessLiteral("NULL").suppress()
        + CaselessLiteral("DEFINED").suppress()
        + CaselessLiteral("AS").suppress()
        + QUOTED_STRING_WITH_QUOTE
    )("null_defined_as")
    ROW_FORMAT_DELIMITED = (
        CaselessLiteral("DELIMITED").suppress()
        + ZeroOrMore(
            FIELDS_TERMINATED_BY
            | COLLECTION_ITEMS_TERMINATED_BY
            | MAP_KEYS_TERMINATED_BY
            | LINES_TERMINATED_BY
            | NULL_DEFINED_AS
        )
    )("row_format_delimited")

    SERDEPROPERTIES = Group(
        CaselessLiteral("WITH").suppress()
        + CaselessLiteral("SERDEPROPERTIES").suppress()
        + LEFT_PARENTHESIS
        + KEY_VALUE_PAIR
        + ZeroOrMore(COMMA + KEY_VALUE_PAIR)
        + RIGHT_PARENTHESIS
    )("serdeproperties")
    ROW_FORMAT_SERDE = (
        CaselessLiteral("SERDE").suppress()
        + QUOTED_STRING_WITH_QUOTE
        + Optional(SERDEPROPERTIES)
    )("row_format_serde")

    ROW_FORMAT = (
        CaselessLiteral("ROW").suppress()
        + CaselessLiteral("FORMAT").suppress()
        + (ROW_FORMAT_DELIMITED | ROW_FORMAT_SERDE)
    )("row_format")

    # ==== Stored As ====
    # Matches:
    # STORED AS ORC
    # STORED BY 'org.com.serde' WITH SERDEPROPERTIES('key'='value')
    FILE_FORMAT = (
        CaselessLiteral("SEQUENCEFILE")
        | CaselessLiteral("TEXTFILE")
        | CaselessLiteral("RCFILE")
        | CaselessLiteral("ORC")
        | CaselessLiteral("PARQUET")
        | CaselessLiteral("AVRO")
        | CaselessLiteral("JSONFILE")
        | Group(
            CaselessLiteral("INPUTFORMAT")
            + QUOTED_STRING_WITH_QUOTE
            + CaselessLiteral("OUTPUTFORMAT")
            + QUOTED_STRING_WITH_QUOTE
        )
    )
    STORED_AS = (
        CaselessLiteral("STORED").suppress()
        + CaselessLiteral("AS").suppress()
        + FILE_FORMAT
    )("stored_as")
    STORED_BY = (
        CaselessLiteral("STORED").suppress()
        + CaselessLiteral("BY").suppress()
        + QUOTED_STRING_WITH_QUOTE
        + Optional(SERDEPROPERTIES)
    )("stored_by")
    STORAGE = (STORED_AS | STORED_BY)("storage")

    # ==== LOCATION ====
    # Matches:
    # LOCATION 'hdfs://some/location'
    LOCATION = (
        Combine(
            CaselessLiteral("LOCATION").suppress() + QUOTED_STRING_WITH_QUOTE,
            adjacent=False,
        )
    )("location")

    # ==== TBLPROPERTIES ====
    # Matches:
    # TBLPROPERTIES('key'='value', 'key2'='value2')
    TBLPROPERTIES = (
        CaselessLiteral("TBLPROPERTIES").suppress()
        + LEFT_PARENTHESIS
        + KEY_VALUE_PAIR
        + ZeroOrMore(COMMA + KEY_VALUE_PAIR)
        + RIGHT_PARENTHESIS
    )("properties")

    # Define a helper reference for all the extended table options grammar definitions
    TABLE_SETTINGS = ZeroOrMore(
        CLUSTERED_BY | SKEWED_BY | ROW_FORMAT | STORAGE | LOCATION | TBLPROPERTIES
    )
