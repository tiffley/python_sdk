import concurrent.futures


# ---------------- CPU-bound Process concurrent ----------------
# Calculation - for the functions which run on your local CPU

# --------- func
def parallelize_calculation(func, li, *args, **kwargs) -> list:
    """ This is normal function. Call this function and pass your function and list as args.
    CPU-bound concurrency which does not require any network related process.

    < params >
    :param func: function
    :param li: list
    :param args: no use
    :param kwargs: additional args which you want to use in your function
    :return: list

    li_len and i (from enumerate) are passed to your function -> Helps to know the status.

    < usage >
    - step1: define a worker for each item from the list
    - step2: call this function

    - step1
    # process for each item in list
    def worker(item, **kwargs):
        print(f"{kwargs['i']} / {kwargs['li_len']}\n")
        # any process
        print(f"{item}, {kwargs}\n")
        return item * 8

    - with additional args
    def worker(item, arg1, arg2, **kwargs):
        ...

    - step2
    results = parallelize_calculation(func=worker, li=[1,2,3,4])
    - with additional args
    results = parallelize_calculation(func=worker, li=[1,2,3,4], arg1=99, arg2=False)
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(func, arg, i=i, li_len=len(li), **kwargs) for i, arg in enumerate(li)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    return results


# --------- deco class
class ParallelizeCalculation:
    """ This is decorator class.
    CPU-bound concurrency which does not require any network related process.

    li_len and i (from enumerate) are passed to your function -> Helps to know the status.

    < usage >
    - step1: define a worker for each item from the list
    - step2: define a function with the decorator. @ParallelizeCalculation(max_workers=4, func=worker)
             this function is only for interface, does nothing.
    - step3: call the step2 function and pass

    - step1
    # process for each item in list
    def worker(item, **kwargs):
        print(f"{kwargs['i']} / {kwargs['li_len']}\n")
        # any process
        print(f"{item}, {kwargs}\n")
        return item * 8

    - step2
    @ParallelizeCalculation(max_workers=4, func=worker)
    def calc_interface(li=[], **kwargs):
        pass

    - step3
    results = calc_interface(li=[1, 2, 3, 4, 5], arg1=1)
    """
    def __init__(self, max_workers, func):
        self.max_workers = max_workers
        self.func = func

    def __call__(self, func):
        def wrapper(li, *args, **kwargs):
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self.func, arg, i=i, li_len=len(li), **kwargs) for i, arg in enumerate(li)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            return results
        return wrapper


# ---------------- IO-bound Thread concurrent ----------------
# Network request - for the functions which are related to network such as API

# --------- deco func
def parallelize_request(max_workers):
    """ This is decorator function.
    May not need of using this, call parallelize_request_interface. (worker=4)
    IO-bound concurrency which uses network such as API

    < params >
    :param max_workers:
    :return:

    li_len and i (from enumerate). -> Helps to know the status.

    < usage >
    - step1: define a worker for each item from the list
    - step2: define a function with the decorator. @parallelize_request(max_workers=4)
    - step3: call the step2 function and pass

    - step1
    # process for each item in list
    def worker(item, **kwargs):
        # any process
        print(f"{item}, {kwargs}\n")
        return item * 8

    - with additional args
    def worker(item, arg1, **kwargs):
        # any process
        print(f"{item}, {arg1} {kwargs}\n")
        return item * 8

    - step2
    @parallelize_request(max_workers=4)
    def con_interface(*item, li=[], **kwargs):
        print(f"{kwargs['i']} / {kwargs['li_len']}\n")
        item_from_li = item[0]
        return worker(item_from_li, **kwargs)

    - step3
    results = calc_interface(li=[1, 2, 3, 4, 5], arg1=1)
    """
    def decorator(func):
        def wrapper(li, *args, **kwargs):
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(func, arg, i=i, li_len=len(li), **kwargs) for i, arg in enumerate(li)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            return results
        return wrapper
    return decorator


# --------- func
@parallelize_request(max_workers=4)
def parallelize_request_interface(*item, func=None, li=[], print_process=False, **kwargs):
    """ This is normal function utilizing parallelize_request. Call this function and pass your function and list as args.
    IO-bound concurrency which uses network such as API

    < params >
    :param item: no use
    :param func: your defined function
    :param li: list
    :param print_process: bool
    :param kwargs:
    :return:

    < usage >
    - step1: define a worker for each item from the list
    - step2: call this function

    - step1
    def worker(item, **kwargs):
        # any process
        print(f"{item}, {kwargs}\n")
        return item * 8

    - with arg
    def worker(item, arg1, **kwargs):
        # any process
        print(f"{item}, {arg1} {kwargs}\n")
        return item * 8

    - step2
    results = parallelize_request_interface(func=worker, li=[1,2,3,4], print_process=True)
    - with arg
    results = parallelize_request_interface(func=worker, li=[1,2,3,4], print_process=True, arg1=False)
    """
    if func is None:
        raise Exception(">>>> No function passed to parallelize_request_interface")
    if print_process:
        print(f">> processing {kwargs['i']} / {kwargs['li_len']}")
    item_from_li = item[0]
    return func(item_from_li, **kwargs)


# ---------

""" examples

--- i.e. <1>
def worker(item, arg1, **kwargs):
    return item * 8

if __name__ == "__main__":
    input_data_list = [1, 2, 3, 4, 5]
    <1-a>
    results = parallelize_request_interface(func=worker, li=input_data_list, print_process=True, arg1=99)
    <1-b>
    results = parallelize_calculation(func=worker, li=input_data_list, arg1=99, arg2_in_kwargs=False)


--- i.e. <2>    
class Sth:
    def __init__(self, a=999):
        self.a = a

    def run(self, di):
        print(di)
        return self.a * 10, di

def sth_same(item, cls, **kwargs):
    return cls.run(item)

def sth_every(item, arg1, **kwargs):
    cls = Sth(arg1)
    return cls.run(item)

if __name__ == "__main__":
    input_data_list = [{"a":1},{"a":1543},{"a":143},{"a":100},{"a":10}]
    
    <2-a> initiate class according to every item in the list
    results = parallelize_calculation(func=sth_every, li=input_data_list, arg1=2, arg2=False)

    <2-b> reuse the same class instance for all items
    cls = Sth()
    results = parallelize_calculation(func=sth_same, li=input_data_list, cls=cls, arg2=False)
    
"""
