from common.deferrable.custom_operator_base import BaseDeferOperator
from common.deferrable.custom_trigger_base import  SimplestSyncToAsyncDeferTrigger

""" how to use
You can choose create function or trigger class.
- simplest framework (just create a function which returns bool)
    1. define condition function - sensor will be deferred until this function returns True
    2. if function needs args, create dict in dag script
        (you can pass {'wait_sec': sec} if you want to change defer time. default is 60sec.)
    3. call get_simplest_custom_deferrable_operator / get_simplest_async_custom_deferrable_operator
        (
            - pass args dict in defer_args: defer_args={"arg1": val}
            - You can also pass any other task params: retries=5
        )

    sample:
        from common.deferrable.get_custom_deferrable_operator import get_simplest_SyncToAsync_deferrable_operator
            args = {
                "func_args": {"arg": True},
                "wait_sec": 20
            }
            get_simplest_SyncToAsync_deferrable_operator(
                task_id=f'simple_true',
                package_path="common.deferrable.condition_funcs",
                module="test_is_true",
                defer_args=args,
                retries=2,
                dag=dag
            )

- trigger framework
    you can refer this to create your trigger
    from common.deferrable.trigger.inherit_test_trigger import WithArgCustomTrigger, AsyncCustomTrigger

    then, use get_custom_deferrable_operator in your dag
    sample:
        args = {
            "func_args": {"arg":True},
            "wait_sec": 20
        }
        get_custom_deferrable_operator(
            task_id=f'is_true',
            TriggerClass=WithArgCustomTrigger,
            defer_args=args,
            retries=2,
            dag=dag
        )
"""

def get_custom_deferrable_operator(TriggerClass, defer_args: dict={}, **af_kwargs):
    """  use this if you created your own trigger
    defer_args = {
        'func_args': optional {'arg1':'val'} - args to use in condition_func,
        'wait_sec': optional
    }
    """
    return BaseDeferOperator(TriggerClass=TriggerClass, all_args=defer_args, **af_kwargs)


# recommended - just pass normal function, it will be automatically converted sync to async
def get_simplified_SyncToAsync_deferrable_operator(package_path, module, defer_args: dict={}, **af_kwargs):
    """  just pass function path
    defer_args = {
        'package_path':(f"from {package_path} import {module}")
        'module': same above
        'func_args': optional {'arg1':'val'} - args to use in condition_func,
        'wait_sec': optional
    }
    """
    defer_args['package_path'] = package_path
    defer_args['module'] = module
    return BaseDeferOperator(TriggerClass=SimplestSyncToAsyncDeferTrigger, all_args=defer_args, **af_kwargs)

