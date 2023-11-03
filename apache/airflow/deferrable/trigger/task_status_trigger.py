import asyncio
from airflow.triggers.base import BaseTrigger, TriggerEvent
from common.airflow_management_util import *
from airflow.models.taskinstance import TaskInstance
from airflow.models import DagRun
from airflow.utils.db import provide_session
from airflow.models.serialized_dag import SerializedDagModel
import os
os.environ['PYTHONASYNCIODEBUG'] = '1'

"""
    Events must have a uniquely identifying value that would be the same
    wherever the trigger is run; this is to ensure that if the same trigger
    is being run in two locations (for HA reasons) that we can deduplicate its
    events.
    -> yield TriggerEvent(xxx)
    xxx should be unique for all trigger.
"""
def get_logger():
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('>>>> %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
logger = get_logger()


class DagStatusTrigger(BaseTrigger):
    def __init__(self, dag_name, mode="success", execution_date=None, triggerID=None):
        super().__init__()
        self.dag_name = dag_name
        self.mode = mode
        self.execution_date = execution_date
        self.triggerID = triggerID

    def serialize(self):
        return ("common.deferrable.trigger.task_status_trigger.DagStatusTrigger", {"dag_name": self.dag_name, "mode": self.mode, "execution_date":self.execution_date, "triggerID": self.triggerID})


    @provide_session
    def is_all_task_success(self, session=None) -> bool:
        # bag = DagBag()
        # tg_dag = bag.get_dag(self.dag_name)
        tg_dag = SerializedDagModel.get(self.dag_name, session).dag
        latest_dag_run_info = DagRun.find(dag_id=self.dag_name, execution_date=self.execution_date)[0]
        return True if latest_dag_run_info.state == "success" else False

    async def run(self):
        while self.is_all_task_success() is False:
            await asyncio.sleep(60)
        yield TriggerEvent(self.triggerID)


class TaskStatusTrigger(BaseTrigger):
    def __init__(self, dag_name, task_name, execution_date=None, triggerID=None, wait_sec=60):
        super().__init__()
        self.dag_name = dag_name
        self.task_name = task_name
        self.execution_date = execution_date
        self.triggerID = triggerID
        self.wait_sec = wait_sec

    def serialize(self):
        logger.info(f">>> TaskTrigger: serialize - \n-> common.deferrable.trigger.task_status_trigger.TaskStatusTrigger\nvars={vars(self)}")
        return ("common.deferrable.trigger.task_status_trigger.TaskStatusTrigger",
            {
                "dag_name": self.dag_name,
                "task_name": self.task_name,
                "execution_date":self.execution_date,
                "triggerID": self.triggerID,
                "wait_sec": self.wait_sec
            })


    @provide_session
    def is_task_succeeded(self, session=None):
        # bag = DagBag()
        # tg_dag = bag.get_dag(self.dag_name)
        tg_dag = SerializedDagModel.get(self.dag_name, session).dag
        task = tg_dag.get_task(self.task_name)
        ti = TaskInstance(task=task, execution_date=self.execution_date)
        stat = ti.current_state()
        logger.info(f">>> TaskTrigger: is_task_succeeded - \n->task instance status - {self.dag_name}.{self.task_name}:{self.execution_date} - {stat}")
        return True if stat == "success" else False

    async def run(self):
        while self.is_task_succeeded() is False:
            await asyncio.sleep(self.wait_sec)
        yield TriggerEvent(self.triggerID)