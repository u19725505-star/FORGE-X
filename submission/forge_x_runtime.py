"""FORGE-X local engineering calculation runtime."""

import json
import math
from copy import deepcopy

TOOL_NAME = "forge_x_calculate"

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": TOOL_NAME,
        "description": (
            "Perform a numerical engineering calculation with "
            "independent recomputation and explicit verification status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "discipline": {
                    "type": "string",
                    "enum": [
                        "structural",
                        "civil",
                        "electrical",
                        "mechanical"
                    ]
                },
                "method": {
                    "type": "string"
                },
                "inputs": {
                    "type": "object"
                }
            },
            "required": [
                "discipline",
                "method",
                "inputs"
            ],
            "additionalProperties": False
        }
    }
}

DISCIPLINES = {
    "structural",
    "civil",
    "electrical",
    "mechanical"
}


def _number(value, name):
    if isinstance(value, bool):
        raise ValueError(name + " must be numeric.")

    number = float(value)

    if not math.isfinite(number):
        raise ValueError(name + " must be finite.")

    return number


def _primary(method, inputs):

    if method == "axial_stress":
        force = _number(inputs["force"], "force")
        area = _number(inputs["area"], "area")

        if area <= 0:
            raise ValueError("Area must be positive.")

        return force / area

    if method == "flow_rate":
        volume = _number(inputs["volume"], "volume")
        time = _number(inputs["time"], "time")

        if time <= 0:
            raise ValueError("Time must be positive.")

        return volume / time

    if method == "ohms_law":
        voltage = _number(inputs["voltage"], "voltage")
        resistance = _number(inputs["resistance"], "resistance")

        if resistance <= 0:
            raise ValueError("Resistance must be positive.")

        return voltage / resistance

    if method == "kinetic_energy":
        mass = _number(inputs["mass"], "mass")
        velocity = _number(inputs["velocity"], "velocity")

        if mass < 0:
            raise ValueError("Mass cannot be negative.")

        return 0.5 * mass * velocity ** 2

    raise ValueError("Unsupported calculation method.")


def _independent(method, inputs):
    # Separate expression paths for numerical cross-checking.

    if method == "axial_stress":
        return (
            _number(inputs["force"], "force")
            * (1.0 / _number(inputs["area"], "area"))
        )

    if method == "flow_rate":
        return (
            _number(inputs["volume"], "volume")
            * (1.0 / _number(inputs["time"], "time"))
        )

    if method == "ohms_law":
        return (
            _number(inputs["voltage"], "voltage")
            * (1.0 / _number(inputs["resistance"], "resistance"))
        )

    if method == "kinetic_energy":
        mass = _number(inputs["mass"], "mass")
        velocity = _number(inputs["velocity"], "velocity")

        return (
            mass * velocity * velocity * 0.5
        )

    raise ValueError("Unsupported verification method.")


def calculate_and_verify(payload):

    if not isinstance(payload, dict):
        raise ValueError("Payload must be an object.")

    discipline = str(
        payload.get("discipline", "")
    ).lower()

    method = str(payload.get("method", ""))

    inputs = payload.get("inputs")

    if discipline not in DISCIPLINES:
        raise ValueError("Unsupported discipline.")

    if not isinstance(inputs, dict):
        raise ValueError("Inputs must be an object.")

    expected = {
        "structural": "axial_stress",
        "civil": "flow_rate",
        "electrical": "ohms_law",
        "mechanical": "kinetic_energy",
    }

    if expected[discipline] != method:
        raise ValueError("Discipline/method mismatch.")

    primary = _primary(method, inputs)
    independent = _independent(method, inputs)

    difference = abs(primary - independent)

    tolerance = max(
        1e-12,
        abs(primary) * 1e-10,
    )

    consistent = (
        math.isfinite(primary)
        and math.isfinite(independent)
        and difference <= tolerance
    )

    return {
        "discipline": discipline,
        "method": method,
        "result": primary,
        "independent_result": independent,
        "absolute_difference": difference,
        "numerically_consistent": consistent,
        "verification_status": (
            "NUMERICALLY_CONSISTENT"
            if consistent else "FAIL"
        ),
        "engineering_status": "UNRESOLVED",
        "evidence_authenticated": False,
        "engineering_signoff": False,
        "limitations": [
            "Numerical agreement is not engineering approval.",
            "Source evidence has not been authenticated.",
            "Applicable standards and assumptions require review.",
            "No professional engineering signoff is implied."
        ]
    }


def merge_tools(existing):

    if existing is None:
        existing = []

    if not isinstance(existing, (list, tuple)):
        raise TypeError("Official tools must be a list.")

    merged = deepcopy(list(existing))

    for item in merged:
        if isinstance(item, dict):
            function = item.get("function", {})

            if function.get("name") == TOOL_NAME:
                raise ValueError("Duplicate local tool detected.")

    merged.append(deepcopy(TOOL_SCHEMA))

    return merged


def extract_tool_call(value, depth=0):

    if depth > 10:
        return None

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception:
            return None

    if isinstance(value, (list, tuple)):
        for item in value:
            found = extract_tool_call(item, depth + 1)

            if found is not None:
                return found

        return None

    if not isinstance(value, dict):
        return None

    function = value.get("function")

    if isinstance(function, dict):
        if function.get("name") == TOOL_NAME:
            return value

    if value.get("name") == TOOL_NAME:
        return value

    for key in (
        "args",
        "kwargs",
        "tool_call",
        "tool_calls",
        "arguments",
        "content",
        "message",
        "messages",
    ):
        if key in value:
            found = extract_tool_call(
                value[key],
                depth + 1,
            )

            if found is not None:
                return found

    return None


def parse_arguments(call):

    function = call.get("function", call)

    arguments = function.get("arguments", {})

    if isinstance(arguments, str):
        arguments = json.loads(arguments)

    if not isinstance(arguments, dict):
        raise ValueError("Tool arguments must be an object.")

    return arguments


def dispatch_tool(arguments):

    if isinstance(arguments, str):
        arguments = json.loads(arguments)

    if isinstance(arguments, dict) and "function" in arguments:
        arguments = parse_arguments(arguments)

    return calculate_and_verify(arguments)


def prepare_tool_result(call):

    arguments = parse_arguments(call)

    return dispatch_tool(arguments)


def tool_call_id(call):

    return (
        call.get("id")
        or call.get("tool_call_id")
        or "forge-x-local-calculation"
    )
