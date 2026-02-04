# License: BSD 3-Clause
from __future__ import annotations

import pytest
import pandas as pd
from openml._api.resources.task import TaskV1API, TaskV2API
from openml.testing import TestAPIBase
from openml.tasks.task import TaskType

class TestTasksV1(TestAPIBase):
    def setUp(self):
        super().setUp()
        self.resource = TaskV1API(self.http_client)

    @pytest.mark.uses_test_server()
    def test_list_tasks(self):
        """Verify V1 list endpoint returns a populated DataFrame."""
        tasks_df = self.resource.list(limit=5, offset=0)
        assert isinstance(tasks_df, pd.DataFrame)
        assert not tasks_df.empty
        assert "tid" in tasks_df.columns

    @pytest.mark.uses_test_server()
    def test_estimation_procedure_list(self):
        """Verify that estimation procedure list endpoint works."""
        procs = self.resource._get_estimation_procedure_list()
        assert isinstance(procs, list)
        assert len(procs) > 0
        assert "id" in procs[0]


class TestTasksCombined(TestAPIBase):
    def setUp(self):
        super().setUp()
        self.v1_resource = TaskV1API(self.http_client)

        self.v2_client = self._get_http_client(
            server="http://127.0.0.1:8001/",
            base_url="",
            api_key="",
            timeout_seconds=self.timeout_seconds,
            retries=self.retries,
            retry_policy=self.retry_policy,
        )
        self.v2_resource = TaskV2API(self.v2_client)

    def _get_first_tid(self, task_type: TaskType) -> int:
        """Helper to find an existing task ID for a given type using the V1 resource."""
        tasks = self.v1_resource.list(limit=1, offset=0, task_type=task_type)
        if tasks.empty:
            pytest.skip(f"No tasks of type {task_type} found on test server.")
        return int(tasks.iloc[0]["tid"])

    @pytest.mark.uses_test_server()
    def test_v2_get_task(self):
        """Verify that we can get a task from V2 API using a task ID found via V1."""
        tid = self._get_first_tid(TaskType.SUPERVISED_CLASSIFICATION)
        task_v1 = self.v1_resource.get(tid)
        task_v2 = self.v2_resource.get(tid)
        assert int(task_v1.task_id) == tid
        assert int(task_v2.task_id) == tid