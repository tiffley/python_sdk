from concurrent_client import parallelize_request_interface, parallelize_calculation


def worker(item, arg1, **kwargs):
    # any process
    print(f"{item}, {arg1} {kwargs}\n")
    return item * 8

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
    input_data_list = [1, 2, 3, 4, 5]

    results = parallelize_request_interface(func=worker, li=input_data_list, print_process=True, arg1=99, f=False)
    print(results)

    results = parallelize_calculation(func=worker, li=[1,2,3,4], arg1=99, arg2=False)
    print(results)

    input_data_list = [{"a":1},{"a":1543},{"a":143},{"a":100},{"a":10}]
    results = parallelize_calculation(func=sth_every, li=input_data_list, arg1=2, arg2=False)
    print(results)

    cls = Sth()
    results = parallelize_calculation(func=sth_same, li=input_data_list, cls=cls, arg2=False)
    print(results)
