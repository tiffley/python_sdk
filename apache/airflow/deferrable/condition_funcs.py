import aiohttp
from airflow.models.taskinstance import TaskInstance
from airflow.utils.db import provide_session
from airflow.models.serialized_dag import SerializedDagModel
from datetime import datetime 
import pendulum
from time import sleep

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

""" 
>>> how to
1. create functions which returns bool.
    (sensor will be deferred until function returns True)
2. import from dag and use with get_custom_deferrable_operator

>>> example
1. create func in this file
    def is_bool(val=True):
        return val

2. create task in dag
    from common.deferrable.get_custom_deferrable_operator import get_custom_deferrable_operator
    from common.deferrable.condition_funcs import is_bool

- w/o args
    task1 = get_custom_deferrable_operator(
        task_id=f'is_true',
        condition_func=is_bool,
        retries=2,
        dag=dag
    )

- w/ args
    args = {
        "func_args": {"val":True},
        "wait_sec": 20
    }
    task2 = get_custom_deferrable_operator(
        task_id=f'is_true',
        condition_func=is_bool,
        defer_args=args,
        retries=2,
        dag=dag
    )
"""


# >>> common -------------

# >> async
async def async_http_request(url, params={}, header={}):
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url, params=params) as response:
            return await response.json()


# >>> test -------------
def test_is_true(arg):
    logger.info(f"from ><><>< test_is_true")
    # just pass bool True/False to check if the sensor works fine
    return arg


# >>> task sensor -------------
@provide_session
def is_task_latest_succeeded(dag_name, task_name, session=None):
    tg_dag = SerializedDagModel.get(dag_name, session).dag
    execution_date = tg_dag.get_latest_execution_date()
    task = tg_dag.get_task(task_name)
    ti = TaskInstance(task=task, execution_date=execution_date)
    stat = ti.current_state()
    logger.info(f">>> TaskTrigger: is_task_succeeded - \n->task instance status - {dag_name}.{task_name}:{execution_date} - {stat}")
    return True if stat == "success" else False

# NG exited with error 'str' object has no attribute 'utcoffset'
@provide_session
def is_task_succeeded(dag_name, task_name, execution_date, session=None):
    ''' 
    original: self.exec_date = context['execution_date'] + self.exec_timedelta
    execution_date can be something like this?
    '{{ (execution_date + macros.timedelta(days=1)) }}' (seems this is str, convert below)
    '''
    logger.info(f">>> TaskTrigger:1 {execution_date} {type(execution_date)}")
    if isinstance(execution_date, str):
        execution_date = pendulum.parse(execution_date)
    logger.info(f">>> TaskTrigger:2 {execution_date} {type(execution_date)}")

    tg_dag = SerializedDagModel.get(dag_name, session).dag
    task = tg_dag.get_task(task_name)
    ti = TaskInstance(task=task, execution_date=execution_date)
    stat = ti.current_state()
    logger.info(f">>> TaskTrigger: is_task_succeeded - \n->task instance status - {dag_name}.{task_name}:{execution_date} - {stat}")
    return True if stat == "success" else False
