from __future__ import annotations

from typing import TYPE_CHECKING

from openml._api.resources.dataset import DatasetV1API, DatasetV2API
from openml._api.resources.estimation_procedure import (
    EstimationProcedureV1API,
    EstimationProcedureV2API,
)
from openml._api.resources.evaluation import EvaluationV1API, EvaluationV2API
from openml._api.resources.evaluation_measure import EvaluationMeasureV1API, EvaluationMeasureV2API
from openml._api.resources.flow import FlowV1API, FlowV2API
from openml._api.resources.run import RunV1API, RunV2API
from openml._api.resources.setup import SetupV1API, SetupV2API
from openml._api.resources.study import StudyV1API, StudyV2API
from openml._api.resources.task import TaskV1API, TaskV2API
from openml.enums import APIVersion, ResourceType

if TYPE_CHECKING:
    from openml._api.resources.base import ResourceAPI

API_REGISTRY: dict[
    APIVersion,
    dict[ResourceType, type[ResourceAPI]],
] = {
    APIVersion.V1: {
        ResourceType.DATASET: DatasetV1API,
        ResourceType.TASK: TaskV1API,
        ResourceType.EVALUATION_MEASURE: EvaluationMeasureV1API,
        ResourceType.ESTIMATION_PROCEDURE: EstimationProcedureV1API,
        ResourceType.EVALUATION: EvaluationV1API,
        ResourceType.FLOW: FlowV1API,
        ResourceType.STUDY: StudyV1API,
        ResourceType.RUN: RunV1API,
        ResourceType.SETUP: SetupV1API,
    },
    APIVersion.V2: {
        ResourceType.DATASET: DatasetV2API,
        ResourceType.TASK: TaskV2API,
        ResourceType.EVALUATION_MEASURE: EvaluationMeasureV2API,
        ResourceType.ESTIMATION_PROCEDURE: EstimationProcedureV2API,
        ResourceType.EVALUATION: EvaluationV2API,
        ResourceType.FLOW: FlowV2API,
        ResourceType.STUDY: StudyV2API,
        ResourceType.RUN: RunV2API,
        ResourceType.SETUP: SetupV2API,
    },
}
