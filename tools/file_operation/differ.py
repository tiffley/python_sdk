from glob import glob
import os


folder = "kafka_client"
extension_filter=['.py']

parent = ['/PycharmProjects/workspace/', '']


def find_diff_file_existence(li_parent, folder):
    # return (set{}, set{}) 
    # check filenames and detect diff between parents.
    whole = []
    for core in li_parent:
        li = list(filter(lambda x: (not 'pg.py' in x.lower() and not 'pycache' in x.lower() and not 'test' in x.lower()) and not os.path.isdir(x), glob(os.path.join(core, folder, "**"), recursive=True)))
        whole.append(set(map(lambda x: x.replace(os.path.join(core, folder), ''), li)))
    return whole[0] - whole[1], whole[1] - whole[0]


def find_content_diff_files(parent, folder, missing_files):
    # return list of file names (diff[], same[])
    # check the file content and detect diff
    ls = list(filter(lambda x: not 'test' in x.lower() and not os.path.isdir(x) and x.replace(os.path.join(parent[0], folder), '') not in missing_files
                     , glob(os.path.join(parent[0], folder, "**"), recursive=True)))
    diff = []
    same = []
    for fn in ls:
        try:
            with open(fn, 'r') as f:
                c1 = f.read()
            with open(fn.replace(parent[0], parent[1]), 'r') as f:
                c2 = f.read()
        except:
            continue
        if c1 != c2:
            diff.append(fn.replace(os.path.join(parent[0], folder), ''))
        else:
            same.append(fn.replace(os.path.join(parent[0], folder), ''))
    return diff, same


def run(extension_filter=[]):
    print('>>> file_existence_diff')
    name_diff = find_diff_file_existence(parent, folder)
    for x in name_diff:
        print()
        print(x)
    print()

    print('>>> content_diff')
    missing_files = []
    for x in name_diff:
        missing_files.extend(list(x))
    content_diff, same = find_content_diff_files(parent, folder, missing_files)
    print('\n<><><><><><><>\n')
    print(content_diff)
    # print('\n<><><><><><><>\n')
    # print(same)
    if extension_filter:
        print('\n<><><><><><><>\n')
        print('final output ------>>>')
        print(parent)
        i = True
        for x in name_diff:
            print('\n--- name diff')
            for fn in x:
                for e in extension_filter:
                    if e in fn:
                        print(fn)
                        if i:
                            print(f"cp {os.path.join(parent[0], folder)}{fn} ./{folder}{fn}")
            i = False
            
        print('\n--- content diff')
        li = []
        for fn in content_diff:
            for e in extension_filter:
                if e in fn:
                    print(fn)
                    li.append(fn)
        print('\n--- some cp cmds')
        for fn in li:
            print(f"cp {os.path.join(parent[0], folder)}{fn} ./{folder}{fn}")


if __name__ == '__main__':
    run(extension_filter)



