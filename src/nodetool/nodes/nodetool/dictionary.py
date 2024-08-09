import json
from typing import Any, Literal
import pandas as pd
from nodetool.workflows.processing_context import ProcessingContext
from nodetool.metadata.types import DataframeRef
from nodetool.workflows.base_node import BaseNode


class GetValue(BaseNode):
    """
    Retrieves a value from a dictionary using a specified key.
    dictionary, get, value, key

    Use cases:
    - Access a specific item in a configuration dictionary
    - Retrieve a value from a parsed JSON object
    - Extract a particular field from a data structure
    """

    _layout = "small"

    dictionary: dict[(str, Any)] = {}
    key: str = ""

    async def process(self, context: ProcessingContext) -> Any:
        return self.dictionary[self.key]


class Update(BaseNode):
    """
    Updates a dictionary with new key-value pairs.
    dictionary, add, update

    Use cases:
    - Extend a configuration with additional settings
    - Add new entries to a cache or lookup table
    - Merge user input with existing data
    """

    _layout = "small"
    _ = "new_pairs"

    dictionary: dict[(str, Any)] = {}
    new_pairs: dict[(str, Any)] = {}

    async def process(self, context: ProcessingContext) -> dict[(str, Any)]:
        self.dictionary.update(self.new_pairs)
        return self.dictionary


class Remove(BaseNode):
    """
    Removes a key-value pair from a dictionary.
    dictionary, remove, delete

    Use cases:
    - Delete a specific configuration option
    - Remove sensitive information before processing
    - Clean up temporary entries in a data structure
    """

    _layout = "small"

    dictionary: dict[(str, Any)] = {}
    key: str = ""

    async def process(self, context: ProcessingContext) -> dict[(str, Any)]:
        del self.dictionary[self.key]
        return self.dictionary


class ParseJSON(BaseNode):
    """
    Parses a JSON string into a Python dictionary.
    json, parse, dictionary

    Use cases:
    - Process API responses
    - Load configuration files
    - Deserialize stored data
    """

    _layout = "small"

    json_string: str = ""

    async def process(self, context: ProcessingContext) -> dict[(str, Any)]:
        res = json.loads(self.json_string)
        if not isinstance(res, dict):
            raise ValueError("Input JSON is not a dictionary")
        return res


class Zip(BaseNode):
    """
    Creates a dictionary from parallel lists of keys and values.
    dictionary, create, zip

    Use cases:
    - Convert separate data columns into key-value pairs
    - Create lookups from parallel data structures
    - Transform list data into associative arrays
    """

    _layout = "small"

    keys: list[Any] = []
    values: list[Any] = []

    async def process(self, context: ProcessingContext) -> dict[Any, Any]:
        return dict(zip(self.keys, self.values))


class Combine(BaseNode):
    """
    Merges two dictionaries, with second dictionary values taking precedence.
    dictionary, merge, update

    Use cases:
    - Combine default and custom configurations
    - Merge partial updates with existing data
    - Create aggregate data structures
    """

    _layout = "small"

    dict_a: dict[(str, Any)] = {}
    dict_b: dict[(str, Any)] = {}

    async def process(self, context: ProcessingContext) -> dict[(str, Any)]:
        return {**self.dict_a, **self.dict_b}


class Filter(BaseNode):
    """
    Creates a new dictionary with only specified keys from the input.
    dictionary, filter, select

    Use cases:
    - Extract relevant fields from a larger data structure
    - Implement data access controls
    - Prepare specific data subsets for processing
    """

    dictionary: dict[(str, Any)] = {}
    keys: list[str] = []

    async def process(self, context: ProcessingContext) -> dict[(str, Any)]:
        return {key: self.dictionary[key] for key in self.keys}


class ConvertToDataframe(BaseNode):
    """
    Transforms a single dictionary into a one-row pandas DataFrame.
    dictionary, dataframe, convert

    Use cases:
    - Prepare dictionary data for tabular analysis
    - Convert configuration to a data record
    - Initiate a DataFrame from a single data point
    """

    _layout = "small"

    dictionary: dict[(str, Any)] = {}

    async def process(self, context: ProcessingContext) -> DataframeRef:
        df = pd.DataFrame([self.model_dump()])
        return await context.dataframe_from_pandas(df)
