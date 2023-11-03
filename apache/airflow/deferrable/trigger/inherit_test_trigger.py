from common.deferrable.custom_trigger_base import BaseDeferTrigger, BaseAsyncDeferTrigger
import aiohttp


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

# good
class CustomTriggerNoArgs(BaseDeferTrigger):
    def __init__(self, all_args: dict):
        super().__init__(all_args=all_args)
        self.all_args['condition_func'] = self.is_True
        logger.info(self.all_args)
        try:
            logger.info(self)
            logger.info(vars(self))
        except Exception as e:
            logger.info(f">>> err inherit")
            logger.error(e)

    def is_True(self):
        logger.info(">> is this visible? logger")
        import datetime
        now = datetime.datetime.now().strftime("%M")
        if int(now) % 2 == 0:
            return True
        return False


# good
class WithArgCustomTrigger(BaseDeferTrigger):
    def __init__(self, all_args: dict):
        super().__init__(all_args=all_args)
        self.all_args['condition_func'] = self.is_True

    def is_True(self, arg):
        logger.info(">> is this visible? logger")
        return arg


# good
class AsyncCustomTrigger(BaseAsyncDeferTrigger):
    def __init__(self, all_args: dict):
        super().__init__(all_args=all_args)
        self.all_args['condition_func'] = self.async_http_request

    async def async_http_request(self, arg, url, params={}, header={}):
        logger.info(">> is this visible? async logger")
        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(url, params=params) as response:
                await response.json()
        return arg
