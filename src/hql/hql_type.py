#!/usr/bin/env python3

from pyparsing import ParseException
from typing import Callable, Dict, List, Optional, Union

from src.parser.definitions import Definitions


class HQLType:
    """
    This class is used as a helper function for generating complex HQL type definitions
    for a column.
    """

    @classmethod
    def default_generator_map(cls) -> Dict[str, Callable]:
        """
        This method returns the default generator function mapping for complex
        HQL types.

        :returns: A dictionary mapping complex types to generator functions
        """
        return {
            "ARRAY": cls.generate_array,
            "MAP": cls.generate_map,
            "STRUCT": cls.generate_struct,
            "UNION": cls.generate_union,
        }

    @classmethod
    def generate(
        cls,
        type_definition: List[Union[List[str], str]],
        generator_map: Optional[Dict[str, Callable]] = None,
    ) -> str:
        """
        This is the entry function for generating complex HQL types. We expect a type
        input of the form: ["MAP", [["key", "value"], ...]]. The first list element
        should always be our complex type token followed by a list containing the
        definition of that complex type.

        :param complex_type: The complex type definition to parse
        :returns: The HQL-format string representing the complex type.
        """
        if generator_map is None:
            generator_map = cls.default_generator_map()

        try:
            return generator_map[type_definition[0]](type_definition[1])
        except (KeyError, IndexError):
            raise ParseException(
                f"Error while parsing type definition: {type_definition}"
            )

    @classmethod
    def generate_array(cls, array_def: List[Union[List[str], str]]) -> str:
        """
        This function generates an array definition from the column type information
        for complex type definitions.

        :param array_def: The array definition in the form of parser results
        :returns: The HQL-string array definition generated
        :raises ParseException: on failure to generate a valid array from the type def
        """
        try:
            definition = "ARRAY<"
            token = array_def[0]

            if isinstance(token, list):
                definition += cls.generate(token)
            elif len(array_def) > 1:
                length = array_def[1]
                definition += f"{token}({length})"
            else:
                definition += token

            definition += ">"

            return definition
        except IndexError:
            raise ParseException(f"Error while parsing array definition: {array_def}")

    @classmethod
    def generate_map(cls, map_def: List[Union[List[str], str]]) -> str:
        """
        This function generates a map definition from the column type information
        for complex type definitions.

        :param map_def: The map definition in the form of parser results
        :returns: The HQL-string map definition generated
        :raises ParseException: on failure to generate a valid map from the type def
        """

        try:
            token = map_def[0]
            if token in Definitions.CHAR_TYPES:
                length = map_def[1]
                key = f"{token}({length})"
                value_type = map_def[2:]
            elif token in Definitions.DECIMAL_TYPES:
                # If the token is a float type, we must check for optional length
                length = map_def[1]
                if length.isnumeric or "," in length:
                    key = f"{token}({length})"
                    value_type = map_def[2:]
                else:
                    key = token
                    value_type = map_def[1:]
            else:
                key = token
                value_type = map_def[1:]

            if isinstance(value_type[0], list):
                value = cls.generate(value_type[0])
            elif len(value_type) > 1:
                value = f"{value_type[0]}({value_type[1]})"
            else:
                value = value_type[0]

            return f"MAP<{key}, {value}>"
        except IndexError:
            raise ParseException(f"Error while parsing map definition: {map_def}")

    @classmethod
    def generate_struct(cls, struct_def: List[Union[List[str], str]]) -> str:
        """
        This function generates a struct definition from the column type information
        for complex type definitions.

        :param struct_def: The struct definition in the form of parser results
        :returns: The HQL-string struct definition generated
        :raises ParseException: on failure to generate a valid struct from the type def
        """

        definition = "STRUCT<"
        try:
            index = 0
            while index < len(struct_def):
                comma = ", " if index > 0 else ""

                col_name = struct_def[index]
                col_type = struct_def[index + 1]

                if isinstance(col_type, list):
                    result = cls.generate(col_type)
                    definition += f"{comma}{col_name}:{result}"
                    index += 2
                elif col_type in Definitions.CHAR_TYPES:
                    length = struct_def[index + 2]
                    definition += f"{comma}{col_name}:{col_type}({length})"
                    index += 3
                elif col_type in Definitions.DECIMAL_TYPES:
                    # If the token is a float type, we must check for optional length
                    length = struct_def[index + 2]
                    if length.isnumeric or "," in length:
                        definition += f"{comma}{col_name}:{col_type}({length})"
                        index += 3
                    else:
                        definition += f"{comma}{col_name}:{col_type}"
                        index += 2
                else:
                    definition += f"{comma}{col_name}:{col_type}"
                    index += 2

                # After each col_name:col_type definition is an optional comment
                # definition for which we must check

                if len(struct_def) > index and (
                    "'" in struct_def[index] or '"' in struct_def[index]
                ):
                    comment = struct_def[index]
                    definition += f" COMMENT {comment}"
                    index += 1

            definition += ">"

            return definition

        except IndexError:
            raise ParseException(f"Error while parsing struct type {struct_def}")

    @classmethod
    def generate_union(cls, union_def: List[Union[List[str], str]]) -> str:
        """
        This function generates a union definition from the column type information
        for complex type definitions.

        :param union_def: The union definition in the form of parser results
        :returns: The HQL-string union definition generated
        :raises ParseException: on failure to generate a valid union from the type def
        """

        definition = "UNION<"
        try:
            index = 0
            while index < len(union_def):
                comma = ", " if index > 0 else ""

                token = union_def[index]
                if isinstance(token, list):
                    result = cls.generate(token)
                    definition += f"{comma}{result}"
                    index += 1
                elif token in Definitions.CHAR_TYPES:
                    length = union_def[index + 1]
                    definition += f"{comma}{token}({length})"
                    index += 2
                elif token in Definitions.DECIMAL_TYPES:
                    # If the token is a float type, we must check for optional length
                    length = union_def[index + 1]
                    if length.isnumeric or "," in length:
                        definition += f"{comma}{token}({length})"
                        index += 2
                    else:
                        definition += f"{comma}{token}"
                        index += 1
                else:
                    definition += f"{comma}{token}"
                    index += 1

            definition += ">"

            return definition

        except IndexError:
            raise ParseException(f"Error while parsing union definition: {union_def}")
