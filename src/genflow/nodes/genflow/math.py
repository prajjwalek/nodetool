import os
from typing import Literal, Tuple
import numpy as np
from pydantic import Field, validator
from genflow.workflows.processing_context import ProcessingContext
from genflow.workflows.genflow_node import GenflowNode
from genflow.metadata.types import to_numpy
from genflow.metadata.types import Tensor
from genflow.workflows.workflow_node import WorkflowNode


def pad_arrays(a: np.ndarray, b: np.ndarray) -> Tuple[(np.ndarray, np.ndarray)]:
    """
    If one of the arguments is a scalar, both arguments are returned as is.
    Pads the smaller array with zeros so that both arrays are the same size.
    This is useful for operations like addition and subtraction.
    """
    if a.size == 1 or b.size == 1:
        return (a, b)
    if len(a) != len(b):
        if len(a) > len(b):
            b = np.pad(b, (0, (len(a) - len(b))), "constant")
        else:
            a = np.pad(a, (0, (len(b) - len(a))), "constant")
    return (a, b)


async def convert_output(
    context: ProcessingContext, output: np.ndarray
) -> float | int | Tensor:
    if output.size == 1:
        return output.item()
    else:
        return Tensor.from_numpy(output)


class BinaryOperationNode(GenflowNode):
    a: int | float | Tensor = Field(title="A", default=0.0)
    b: int | float | Tensor = Field(title="B", default=0.0)

    async def process(self, context: ProcessingContext) -> int | float | Tensor:
        a = to_numpy(self.a)
        b = to_numpy(self.b)
        if a.size > 1 and b.size > 1:
            (a, b) = pad_arrays(a, b)
        res = self.operation(a, b)
        return await convert_output(context, res)

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


class AddNode(BinaryOperationNode):
    """
    Performs addition on two inputs.
    math, plus, add, addition, sum, +
    """

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.add(a, b)


class SubtractNode(BinaryOperationNode):
    """
    Subtracts the second input from the first.
    math, minus, difference, -
    """

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.subtract(a, b)


class MultiplyNode(BinaryOperationNode):
    """
    Multiplies two inputs.
    math, product, times, *
    """

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.multiply(a, b)


class DivideNode(BinaryOperationNode):
    """
    Divides the first input by the second.
    math, division, arithmetic, quotient
    """

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.divide(a, b)


class ModulusNode(BinaryOperationNode):
    """
    Calculates the remainder of division of the first input by the second.
    math, mod, modulus, remainder, %, modulo, division
    """

    def operation(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.mod(a, b)


class SineNode(GenflowNode):
    """
    Computes the sine of an input angle in radians.
    math, sine, radians, angle
    Returns a float value between -1 and 1.
    """

    angle_rad: float | int | Tensor = Field(title="Angle (Radians)", default=0.0)

    async def process(self, context: ProcessingContext) -> float | Tensor:
        res = np.sin(to_numpy(self.angle_rad))
        return await convert_output(context, res)


class CosineNode(GenflowNode):
    """
    Calculates the cosine of a given angle in radians.
    math, cosine, radians, angle
    Returns a float value between -1 and 1.
    """

    base: float | int | Tensor = Field(title="Base", default=1.0)
    exponent: float | int | Tensor = Field(title="Exponent", default=2.0)

    async def process(self, context: ProcessingContext) -> float | int | Tensor:
        a = to_numpy(self.base)
        b = to_numpy(self.exponent)
        if isinstance(a, np.ndarray) and isinstance(b, np.ndarray):
            (a, b) = pad_arrays(a, b)
        return await convert_output(context, np.power(a, b))


class SqrtTensor(GenflowNode):
    """
    Calculates the square root of the input.
    math, power, sqrt, square, root
    """

    x: int | float | Tensor = Field(title="Input", default=1.0)

    async def process(self, context: ProcessingContext) -> float | int | Tensor:
        return await convert_output(
            context, np.sqrt(to_numpy(self.x).astype(np.float32))
        )
