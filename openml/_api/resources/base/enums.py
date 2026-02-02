from __future__ import annotations

from enum import Enum


class APIVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"


class ResourceType(str, Enum):
    DATASET = "dataset"
    TASK = "task"
    TASK_TYPE = "task_type"
    EVALUATION_MEASURE = "evaluation_measure"
    ESTIMATION_PROCEDURE = "estimation_procedure"
    EVALUATION = "evaluation"
    FLOW = "flow"
    STUDY = "study"
    RUN = "run"
    SETUP = "setup"
    USER = "user"


class RetryPolicy(str, Enum):
    HUMAN = "human"
    ROBOT = "robot"
