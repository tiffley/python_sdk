def list_divider(li, div_cnt=4) -> list[list]:
    """
    divide a list to some lists in a list
    li:: [1,2,3,...100]
    return:: [ [1,2,3,...], [4,5,6...], [], [..., 100] ]
    """
    chunk_size = len(li) // div_cnt  # Determine the size of each sublist
    sublists = [li[i:i + chunk_size] for i in range(0, len(li), chunk_size)]
    if len(sublists) > div_cnt:
        diff = len(sublists) - div_cnt
        for i in range(1, diff + 1):
            sublists[-i - 1].extend(sublists.pop())
    return sublists


