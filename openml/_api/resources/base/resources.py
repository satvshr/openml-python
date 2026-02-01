from __future__ import annotations

from typing import TYPE_CHECKING

from openml._api.config import ResourceType
from openml._api.resources.base import ResourceAPI

if TYPE_CHECKING:
    from openml._api.clients import HTTPClient, MinIOClient


class DatasetAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.DATASET

    def __init__(self, http: HTTPClient, minio: MinIOClient):
        self._minio = minio
        super().__init__(http)


class TaskAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.TASK


class EvaluationMeasureAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.EVALUATION_MEASURE


class EstimationProcedureAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.ESTIMATION_PROCEDURE


class EvaluationAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.EVALUATION


class FlowAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.FLOW


class StudyAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.STUDY


class RunAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.RUN


class SetupAPI(ResourceAPI):
    resource_type: ResourceType = ResourceType.SETUP
