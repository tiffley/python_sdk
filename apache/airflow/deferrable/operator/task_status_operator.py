from datetime import datetime, timedelta
from croniter import croniter
from airflow.sensors.base import BaseSensorOperator
from common.deferrable.trigger.task_status_trigger import DagStatusTrigger, TaskStatusTrigger
from airflow.models.serialized_dag import SerializedDagModel
from airflow.utils.db import provide_session
from common.deferrable.custom_trigger_base import SimplestSyncToAsyncDeferTrigger
from common.dag_utils import calculate_upstream_execution_date

class DagSensorOperator(BaseSensorOperator):
    """ 
    DagSensorOperator(
            task_id=f'dagsensor_{target_dag}',
            dag_name=target_dag,
            dag_cron_schedule=target_dag_cron_schedule,
            my_cron_schedule=downstream_cron_schedule,
            dag=dag  
        )  
    """
    def __init__(self,
                 dag_name: str,
                 dag_cron_schedule: str,
                 my_cron_schedule: str,
                 *args,
                 **kwargs):
        super(DagSensorOperator, self).__init__(*args, **kwargs)
        self.dag_name = dag_name
        self.dag_cron_schedule = dag_cron_schedule
        self.my_cron_schedule = my_cron_schedule
    
    def execute(self, context):
        my_execution_date = context['dag_run'].execution_date
        upstream_execution_date = calculate_upstream_execution_date(self.dag_cron_schedule, self.my_cron_schedule, my_execution_date)
        self.log.info(f"My spec: crontab {self.my_cron_schedule}, execution date {my_execution_date}")
        self.log.info(f"Upstream spec: dag id {self.dag_name}, crontab {self.dag_cron_schedule}, execution date {upstream_execution_date}")
        self.defer(trigger=DagStatusTrigger(
            self.dag_name,
            execution_date= upstream_execution_date,
            triggerID=context['task_instance_key_str']),
            method_name="resume_method")
 
    def resume_method(self, context, event=None):
        return


class TaskSensorOperator(BaseSensorOperator):
    """
        TaskSensorOperator(
                task_id=f'tasksensor_{target_dag}_{task}',
                dag_name=target_dag,
                task_name=task,
                wait_sec=20, >>> optional. default is 60 sec
                exec_timedelta=timedelta(hours=-23), >>> optional. default is latest run
                dag=dag  
            )
    """
    def __init__(self,
                 task_name: str,
                 dag_name: str,
                 exec_timedelta: timedelta=None,
                 exec_cron:str=None,
                 my_cron:str=None,
                 wait_sec: int=60,
                 *args,
                 **kwargs):
        if not kwargs.get("poke_interval", None):
           kwargs['poke_interval'] = 300
        super(TaskSensorOperator, self).__init__(*args, **kwargs)
        self.dag_name = dag_name
        self.task_name = task_name
        self.exec_timedelta = exec_timedelta
        self.exec_cron = exec_cron
        self.my_cron = my_cron
        self.exec_date = None
        self.wait_sec = wait_sec

    @provide_session
    def execute(self, context, session=None):
        if self.exec_timedelta:
            # timedelta
            self.exec_date = context['execution_date'] + self.exec_timedelta
            print(f">>>>>> delta > {self.exec_date}")
        elif(self.my_cron and self.exec_cron):
            # cron based
            self.exec_date = calculate_upstream_execution_date(self.exec_cron, self.my_cron, context['execution_date'])
            print(f">>>>>> cron schedule > {self.exec_date}")
        else:
            # latest run
            tg_dag = SerializedDagModel.get(self.dag_name, session).dag
            self.exec_date = tg_dag.get_latest_execution_date()
            print(f">>>>>> latest > {self.exec_date}")

        # self.defer(trigger=TaskStatusTrigger(self.dag_name, self.task_name, execution_date=self.exec_date, 
        #         triggerID=context['task_instance_key_str'], wait_sec=self.wait_sec
        #         ), method_name="resume_method")

        all_args = {
            "package_path": "common.deferrable.condition_funcs",
            "module": "is_task_succeeded",
            "func_args": {
                "dag_name": self.dag_name,
                "task_name": self.task_name,
                "execution_date": self.exec_date
            },
            "wait_sec": self.wait_sec,
            "triggerID": context['task_instance_key_str']
        }
        self.defer(trigger=SimplestSyncToAsyncDeferTrigger(all_args), method_name="resume_method")
 
    def resume_method(self, context, event=None):
        return