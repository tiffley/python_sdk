from glob import glob
import os

p = f'/Users/Documents/workspace/git_repo/open-source'


folder = "spark/"

tg = ["spark-submit"]

# contents = ["org.apache.spark.sql.connector.catalog.", "TableCatalog"]

f_judge = all
c_judge = all

is_fn_search = True


def search_by_filename(dir_path, li_tgs, judge=any):
    if judge(list(map(lambda x: x in fn, li_tgs))):
        return fn.replace(dir_path, '')

def search_by_contents(dir_path, li_contents, judge=any):
    with open(fn, 'r') as f:
        script = f.read()
    for row in script.split('\n'):
        if judge(list(map(lambda x: x in row, li_contents))):
            return fn.replace(dir_path, '')


if __name__ == '__main__':
    for fn in glob(os.path.join(p, folder, "**"), recursive=True):
        if 'test' in fn.lower():
            continue

        if is_fn_search:
            res = search_by_filename(p, tg, f_judge)
            if res:
                print(res)
        else:
            if not search_by_filename(p, tg, f_judge):
                continue
            try:
                res = search_by_contents(p, contents, c_judge)
                if res:
                    print(res)
            except:
                continue



