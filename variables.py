"""Manage variables."""
from dataclasses import dataclass
from enum import Enum, auto

class PrimitiveTypes(Enum):
    """Primitive types."""
    INT = auto()

@dataclass
class Variable:
    """Representation of a variable."""
    variable_id:    int
    is_primitive:   bool
    primitive_type: PrimitiveTypes | None

primitive_keywords = {
    "int": PrimitiveTypes.INT,
}

current_variable_id = 0
# Mapping of <variable name, Variable>
variables: dict[str, Variable] = {}
