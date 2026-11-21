
"""
FORGE-X autonomous engineering agent.

Runtime module for the official PLE model and tool execution environment.
Uses the Python standard library only.
"""

from __future__ import annotations

import os
import json
import math
import hashlib
import threading
from pathlib import Path
from datetime import datetime, timezone


AGENT_VERSION = "0.26.0"
_LOCK = threading.RLock()

STATE_DIR = Path(
    os.environ.get(
        "FORGE_X_STATE_DIR",
        str(Path(__file__).resolve().parent / "forge_x_runtime")
    )
)

STATE_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_FILE = STATE_DIR / "events.jsonl"
EVIDENCE_FILE = STATE_DIR / "evidence.jsonl"
CALCULATIONS_FILE = STATE_DIR / "calculations.jsonl"
VERIFICATION_FILE = STATE_DIR / "verification.jsonl"
TASK_STATE_FILE = STATE_DIR / "task_state.json"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    raw = json.dumps(
        value,
        sort_keys=True,
        default=str
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def safe_json(value, limit=12000):
    try:
        result = json.dumps(
            value,
            default=str,
            sort_keys=True
        )
    except Exception:
        result = repr(value)
    return result[:limit]


def append_record(path, record):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    line = json.dumps(
        record,
        sort_keys=True,
        default=str
    )

    with _LOCK:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


def record_event(event_type, payload):
    record = {
        "timestamp": utc_now(),
        "agent_version": AGENT_VERSION,
        "event_type": str(event_type),
        "payload": payload,
        "payload_sha256": digest(payload),
    }

    append_record(EVENTS_FILE, record)
    return record


def update_task_state(**updates):
    with _LOCK:
        state = {}

        if TASK_STATE_FILE.exists():
            try:
                state = json.loads(
                    TASK_STATE_FILE.read_text(encoding="utf-8")
                )
            except Exception:
                state = {}

        state.update(updates)
        state["updated_at"] = utc_now()
        state["agent_version"] = AGENT_VERSION

        temp = TASK_STATE_FILE.with_suffix(".tmp")
        temp.write_text(
            json.dumps(state, indent=2, sort_keys=True, default=str),
            encoding="utf-8"
        )
        temp.replace(TASK_STATE_FILE)

    return state


def current_task_state():
    if not TASK_STATE_FILE.exists():
        return {}

    try:
        return json.loads(
            TASK_STATE_FILE.read_text(encoding="utf-8")
        )
    except Exception:
        return {}


# -------------------------------------------------------------------------
# TASK UNDERSTANDING AND FOUR-DISCIPLINE ROUTING
# -------------------------------------------------------------------------

DISCIPLINE_TERMS = {
    "Structural": (
        "structural", "beam", "column", "truss", "foundation",
        "stress", "strain", "deflection", "reinforcement",
        "load", "shear", "moment", "bearing"
    ),
    "Civil": (
        "civil", "drainage", "grading", "earthwork", "road",
        "pavement", "site", "runoff", "stormwater", "culvert",
        "survey", "slope", "excavation", "quantity"
    ),
    "Electrical": (
        "electrical", "voltage", "current", "resistance",
        "circuit", "power", "transformer", "conductor",
        "breaker", "grounding", "motor", "wiring"
    ),
    "Mechanical": (
        "mechanical", "force", "velocity", "acceleration",
        "kinetic", "energy", "thermodynamic", "fluid",
        "pressure", "flow rate", "torque", "heat transfer",
        "pump", "gear"
    ),
}


def classify_task(text):
    normalized = str(text).lower()

    scores = {
        discipline: sum(
            1 for term in terms if term in normalized
        )
        for discipline, terms in DISCIPLINE_TERMS.items()
    }

    positive = [
        (name, score)
        for name, score in scores.items()
        if score > 0
    ]

    positive.sort(key=lambda item: item[1], reverse=True)

    if not positive:
        return {
            "discipline": None,
            "status": "UNRESOLVED",
            "scores": scores,
            "reason": "No discipline evidence identified."
        }

    if len(positive) > 1 and positive[0][1] == positive[1][1]:
        return {
            "discipline": None,
            "status": "UNRESOLVED",
            "scores": scores,
            "reason": "Multiple disciplines have equal evidence."
        }

    return {
        "discipline": positive[0][0],
        "status": "CLASSIFIED",
        "scores": scores,
        "reason": "Highest lexical evidence score."
    }


def prepare_messages(messages):
    """
    Add FORGE-X operating instructions to the real model conversation.
    Preserve the original task messages and official tool definitions.
    """

    instructions = (
        "You are FORGE-X, an autonomous engineering agent operating "
        "inside the official Physical Engineering's Last Exam runtime. "
        "Interpret the task, identify its objectives, constraints, "
        "engineering discipline, dependencies, and deliverables. "
        "Use only the official tools supplied by the runtime. "
        "Do not invent tools, protocol operations, source evidence, "
        "measurements, or completed deliverables. "
        "For structural, civil, electrical, and mechanical work, "
        "identify governing equations, units, assumptions, and "
        "calculation steps. Check dimensional consistency and "
        "independently recompute important results. "
        "Separate supplied project evidence from assumptions and "
        "estimates. Missing evidence must not be reported as PASS. "
        "Before completion, inspect generated files and verify that "
        "requested deliverables exist and are internally consistent. "
        "Do not claim professional engineering certification. "
        "When information is missing, use available official tools "
        "to obtain it or explicitly report the unresolved issue."
    )

    if not isinstance(messages, list):
        record_event(
            "MODEL_CONTEXT_NOT_LIST",
            {"message_type": type(messages).__name__}
        )
        return messages

    for message in messages:
        if (
            isinstance(message, dict)
            and message.get("role") == "system"
            and "You are FORGE-X" in str(message.get("content", ""))
        ):
            return messages

    prepared = list(messages)
    prepared.insert(
        0,
        {
            "role": "system",
            "content": instructions
        }
    )

    record_event(
        "AGENT_INSTRUCTIONS_INJECTED",
        {"message_count": len(prepared)}
    )

    return prepared


# -------------------------------------------------------------------------
# EVIDENCE FABRIC
# -------------------------------------------------------------------------

def record_evidence(
    evidence_id,
    value,
    unit=None,
    source=None,
    discipline=None,
    evidence_class="OBSERVED",
    confidence=None,
    metadata=None
):
    if not evidence_id:
        raise ValueError("Evidence ID is required.")

    if confidence is not None:
        confidence = float(confidence)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1.")

    record = {
        "evidence_id": str(evidence_id),
        "value": value,
        "unit": unit,
        "source": source,
        "discipline": discipline,
        "evidence_class": evidence_class,
        "confidence": confidence,
        "metadata": metadata or {},
        "status": "RECORDED",
        "timestamp": utc_now(),
        "value_sha256": digest(value),
    }

    append_record(EVIDENCE_FILE, record)

    record_event(
        "EVIDENCE_RECORDED",
        {
            "evidence_id": evidence_id,
            "evidence_class": evidence_class,
            "source": source
        }
    )

    return record


def observe_tool_result(args, kwargs, result):
    """
    Capture tool activity and returned results.

    A tool result is an observation, not automatically authoritative
    engineering evidence.
    """

    tool_payload = {
        "args": safe_json(args, 5000),
        "kwargs": safe_json(kwargs, 5000),
        "result_type": type(result).__name__,
        "result_sha256": digest(safe_json(result)),
        "result_preview": safe_json(result, 3000),
    }

    record_event("OFFICIAL_TOOL_RESULT", tool_payload)

    combined = (
        tool_payload["args"] + " " + tool_payload["kwargs"]
    ).lower()

    if "read_file" in combined:
        record_evidence(
            evidence_id="OBS-" + tool_payload["result_sha256"][:16],
            value=tool_payload["result_preview"],
            source="Official PLE tool result",
            evidence_class="OBSERVATION_CANDIDATE",
            confidence=None,
            metadata={
                "result_sha256": tool_payload["result_sha256"]
            }
        )

    return result


# -------------------------------------------------------------------------
# ENGINEERING CALCULATION REGISTRY
# -------------------------------------------------------------------------

def _finite(value, name):
    value = float(value)

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    return value


def calculate(discipline, method, inputs, evidence_ids=None):
    """
    Deterministic engineering methods.

    These methods do not replace project-specific standards,
    design requirements, or evidence review.
    """

    x = {
        key: _finite(value, key)
        for key, value in inputs.items()
    }

    d = str(discipline).lower()
    m = str(method).lower()

    result = None
    unit = None
    equation = None

    if d == "structural":
        if m == "axial_stress":
            result = x["force"] / x["area"]
            unit = "Pa"
            equation = "sigma = F/A"

        elif m == "axial_strain":
            result = x["change_length"] / x["original_length"]
            unit = "dimensionless"
            equation = "epsilon = delta_L/L"

        elif m == "hookes_law_stress":
            result = x["elastic_modulus"] * x["strain"]
            unit = "Pa"
            equation = "sigma = E*epsilon"

        else:
            raise ValueError("Unsupported structural method.")

    elif d == "civil":
        if m == "rectangular_area":
            result = x["length"] * x["width"]
            unit = "m^2"
            equation = "A = L*W"

        elif m == "prismatic_volume":
            result = x["length"] * x["width"] * x["depth"]
            unit = "m^3"
            equation = "V = L*W*D"

        elif m == "discharge":
            if x["time"] == 0:
                raise ValueError("Time cannot be zero.")

            result = x["volume"] / x["time"]
            unit = "m^3/s"
            equation = "Q = V/t"

        else:
            raise ValueError("Unsupported civil method.")

    elif d == "electrical":
        if m == "ohms_law_current":
            if x["resistance"] == 0:
                raise ValueError("Resistance cannot be zero.")

            result = x["voltage"] / x["resistance"]
            unit = "A"
            equation = "I = V/R"

        elif m == "electrical_power":
            result = x["voltage"] * x["current"]
            unit = "W"
            equation = "P = V*I"

        elif m == "series_resistance":
            result = x["resistance_1"] + x["resistance_2"]
            unit = "ohm"
            equation = "R_total = R1 + R2"

        else:
            raise ValueError("Unsupported electrical method.")

    elif d == "mechanical":
        if m == "newtons_second_law":
            result = x["mass"] * x["acceleration"]
            unit = "N"
            equation = "F = m*a"

        elif m == "kinetic_energy":
            result = 0.5 * x["mass"] * x["velocity"] ** 2
            unit = "J"
            equation = "KE = 0.5*m*v^2"

        elif m == "mechanical_work":
            result = x["force"] * x["distance"]
            unit = "J"
            equation = "W = F*d"

        else:
            raise ValueError("Unsupported mechanical method.")

    else:
        raise ValueError("Unknown engineering discipline.")

    result = _finite(result, "calculation result")

    record = {
        "calculation_id": "CAL-" + digest({
            "discipline": discipline,
            "method": method,
            "inputs": x,
            "timestamp": utc_now()
        })[:16],
        "discipline": discipline,
        "method": method,
        "equation": equation,
        "inputs": x,
        "result": result,
        "unit": unit,
        "evidence_ids": list(evidence_ids or []),
        "record_class": "RUNTIME_CALCULATION",
        "timestamp": utc_now(),
    }

    append_record(CALCULATIONS_FILE, record)
    record_event("ENGINEERING_CALCULATION", record)

    return record


def independently_verify(calculation, recomputed_value=None, tolerance=1e-9):
    reported = float(calculation["result"])

    if recomputed_value is None:
        fresh = calculate(
            calculation["discipline"],
            calculation["method"],
            calculation["inputs"],
            calculation.get("evidence_ids", [])
        )
        recomputed_value = float(fresh["result"])

    recomputed_value = float(recomputed_value)

    absolute_error = abs(reported - recomputed_value)
    relative_error = (
        absolute_error / max(abs(recomputed_value), 1e-15)
    )

    status = (
        "PASS"
        if absolute_error <= tolerance * max(1.0, abs(recomputed_value))
        else "FAIL"
    )

    verification = {
        "verification_id": "VER-" + digest({
            "calculation_id": calculation.get("calculation_id"),
            "reported": reported,
            "recomputed": recomputed_value
        })[:16],
        "calculation_id": calculation.get("calculation_id"),
        "reported_value": reported,
        "recomputed_value": recomputed_value,
        "unit": calculation.get("unit"),
        "absolute_error": absolute_error,
        "relative_error": relative_error,
        "status": status,
        "method": "INDEPENDENT_FORMULA_RECOMPUTATION",
        "timestamp": utc_now(),
    }

    append_record(VERIFICATION_FILE, verification)
    record_event("CALCULATION_VERIFICATION", verification)

    return verification


def agent_status():
    return {
        "agent_version": AGENT_VERSION,
        "state_directory": str(STATE_DIR),
        "task_state": current_task_state(),
        "files": {
            "events": str(EVENTS_FILE),
            "evidence": str(EVIDENCE_FILE),
            "calculations": str(CALCULATIONS_FILE),
            "verification": str(VERIFICATION_FILE),
        }
    }


record_event(
    "AGENT_MODULE_INITIALIZED",
    {
        "agent_version": AGENT_VERSION,
        "state_directory": str(STATE_DIR)
    }
)
