from airflow.sensors.base import BaseSensorOperator


''' how to use
1. create your custom trigger
2. import this operator and create your own custom operator with custom trigger
3. import custom operator from dag

sample
- create custom operator 
    from common.deferrable.custom_operator_base import BaseDeferOperator
    from common.deferrable.trigger.xxx import xxxTrigger

    class CustomOperator(BaseDeferOperator):
        def __init__(self, all_args, **kwargs):
            super().__init__(TriggerClass=xxxTrigger, all_args=all_args, **kwargs)

- from dag side, use created custom operator
    from common.deferrable.operator.xxx import xxxOperator

    args = {
        "": "",
        "": "",
        "": ""
    }
    xxxOperator(
        task_id=f'xxx',
        all_args=args,
        retries=2,
        dag=dag
    )

'''

class BaseDeferOperator(BaseSensorOperator):
    """
    all_args = {
        'condition_func': function which returns boolean,
        'func_args': {'arg1':'val'} - args to use in condition_func,
        'wait_sec': optional
    }
    """
    def __init__(self, TriggerClass, all_args: dict, *args, **kwargs):
        # https://github.com/apache/airflow/issues/10790
        # Here's another potential hint: We have increased the poke_interval value for a subset of our sensors yesterday to 5 minutes (from the default 1 minute), and the issue seems to have disappeared for the affected sensors.
        if not kwargs.get("poke_interval", None):
            kwargs['poke_interval'] = 300

        super(BaseDeferOperator, self).__init__(*args, **kwargs)
        self.all_args = all_args
        self.TriggerClass = TriggerClass

    def execute(self, context):
        self.all_args['triggerID'] = context['task_instance_key_str']
        print(f">> operator args check >>>> {self.all_args}")
        if not self.all_args.get('wait_sec', None):
            self.all_args['wait_sec'] = 85
        self.defer(trigger=self.TriggerClass(self.all_args), method_name="resume_method")
 
    def resume_method(self, context, event=None):
        return