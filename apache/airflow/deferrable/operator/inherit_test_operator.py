from common.deferrable.custom_operator_base import BaseDeferOperator
from common.deferrable.trigger.inherit_test_trigger import CustomTrigger

class CustomOperator(BaseDeferOperator):
    def __init__(self, all_args, **kwargs):
        print(f">>all> {all_args}")
        print(f">>kw> {kwargs}")
        super().__init__(TriggerClass=CustomTrigger, all_args=all_args, **kwargs)