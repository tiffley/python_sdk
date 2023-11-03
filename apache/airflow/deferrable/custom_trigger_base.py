import functools
import asyncio
from airflow.triggers.base import BaseTrigger, TriggerEvent
import os
os.environ['PYTHONASYNCIODEBUG'] = '1'

''' how to use
case 1 >> create a function only
updated - recommend to use SimplestSyncToAsyncDeferTrigger
sample
BaseDeferOperator(TriggerClass=SimplestSyncToAsyncDeferTrigger, all_args=defer_args, **af_kwargs)

----------

case 2 >> create your own trigger
1. import this trigger and create your own trigger
    - create condition function which returns boolean. 
        sensor will be deferred until this function returns True
        pass dict in all_args if the function needs args: all_args={"arg1": val}
    - You can also pass any other task params: retries=5
2. import your trigger to your operator.
sample
    from common.deferrable.custom_trigger_base import BaseDeferTrigger

    class CustomTrigger(BaseDeferTrigger):
        def __init__(self, all_args: dict):
            all_args['condition_func'] = is_even_min
            super().__init__(all_args=all_args)

        def is_even_min():
            import datetime
            now = datetime.datetime.now().strftime("%M")
            if int(now) % 2 == 0:
                return True
            return False
'''


class BaseDeferTrigger(BaseTrigger):
    """
    all_args = {
        'condition_func': function which returns boolean,
        'func_args': {'arg1':'val'} - args to use in condition_func,
        'wait_sec': optional,
        'triggerID': automatically passed from operator
    }
    """
    def __init__(self, all_args: dict):
        super().__init__()
        self.all_args = all_args
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
        self.logger = get_logger()

    def serialize(self):
        return (self.get_cls_path(), {"all_args": self.all_args})

    def get_cls_path(self):
        return str(self.__class__).split("'")[1]

    async def run(self):
        while self.all_args['condition_func'](**self.all_args.get('func_args',{})) is False:
            await asyncio.sleep(self.all_args['wait_sec'])
        yield TriggerEvent(self.all_args['triggerID'])


class BaseAsyncDeferTrigger(BaseDeferTrigger):
    async def run(self):
        while await self.all_args['condition_func'](**self.all_args.get('func_args',{})) is False:
            await asyncio.sleep(self.all_args['wait_sec'])
        yield TriggerEvent(self.all_args['triggerID'])


# recommended - convert sync to async - should use this as default
class SimplestSyncToAsyncDeferTrigger(BaseDeferTrigger):
    """
    all_args = {
        'package_path': package_path where the module is stored,
        'module': function name which returns boolean,
            -> from {package_path} import {module}
        'func_args': {'arg1':'val'} - args to use in condition_func,
        'wait_sec': optional,
        'triggerID': automatically passed from operator
    }
    """
    def import_module(self):
        self.logger.info(f"SimplestSyncToAsyncDeferTrigger - try: from {self.all_args['package_path']} import {self.all_args['module']}")
        exec(f"from {self.all_args['package_path']} import {self.all_args['module']}")
        self.logger.info(f"SimplestSyncToAsyncDeferTrigger - imported: {locals()}")
        return locals()[self.all_args['module']]

    async def run_func_as_async(self):
        async_import = asyncio.coroutine(self.import_module)
        async_func = asyncio.coroutine(await async_import())
        return await async_func(**self.all_args.get('func_args',{}))

    async def run(self):
        while await self.run_func_as_async() is False:
            await asyncio.sleep(self.all_args['wait_sec'])
        yield TriggerEvent(self.all_args['triggerID'])

