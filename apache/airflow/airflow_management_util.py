from operator import le
import subprocess
from datetime import date

# command reference
# https://airflow.apache.org/docs/apache-airflow/1.10.12/cli-ref.html
# https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#tasks


def run_command(command: str, **kwargs) -> str:
    res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return res.stdout.decode(), res.stderr.decode()


class CLI:
    def __init__(self, dag_name) -> None:
        self.dag_name = dag_name


    def get_all_dags(self):
        # airflow dags list [-h] [-o table, json, yaml, plain] [-S SUBDIR] [-v]
        res = run_command(f"airflow dags list")


    # dag operator
    def get_dag_runs(self) -> list:
        ''' returns list of dict [{"id":xxx,"date":xxx}, {},....]
        List DAG runs given a DAG id. If state option is given, 
        it will only search for all the dagruns with the given state. 
        If no_backfill option is given, it will filter out all backfill dagruns for given dag id. 
        If start_date is given, it will filter out all the dagruns that were executed before this date. 
        If end_date is given, it will filter out all the dagruns that were executed after this date.'''
        # airflow dags list-runs [-h] [-d DAG_ID] [-e END_DATE] [--no-backfill] [-o table, json, yaml, plain] [-s START_DATE] [--state STATE] [-v]
        res, err = run_command(f"airflow dags list-runs -d {self.dag_name}")
        delim = '''+================================='''
        header = ['dag_id', 'run_id', 'state', 'execution_date', 'state_date', 'end_date']
        rows = list(map(lambda x: x.strip(), res.split(delim)[-1].split('\n')))

        li_dag_run_hist = []
        data = {}
        for row in rows:
            if not row:
                continue
            for i, item in enumerate(row.split('|')):
                data[header[i]] = item.strip()
            li_dag_run_hist.append(data)
            data = {}
        return li_dag_run_hist


    def get_dag_last_run(self) -> dict:
        '''{'dag_id': 'defer_test ', 'run_id': ' manual__2022-04-14T04:59:58.190149+00:00 ', 'state': ' success ', 'execution_date': ' 2022-04-14T04:59:58.190149+00:00 ', 'state_date': ' 2022-04-14T04:59:59.208718+00:00 ', 'end_date': ' 2022-04-14T05:01:04.648644+00:00'}'''
        dag_run_hist = self.get_dag_runs()
        return dag_run_hist[0]

    
    def get_dag_show(self):
        '''Get the status of a dag run'''
        # airflow dags show [-h] [--imgcat] [-s SAVE] [-S SUBDIR] dag_id
        res = run_command(f"airflow dags show {self.dag_name}")
        print(res)


    def get_dag_status(self, exec_date):
        '''Get the status of a dag run'''
        # airflow dags state [-h] [-S SUBDIR] dag_id execution_date
        res = run_command(f"airflow tasks list {self.dag_name}")


    def get_dag_list_job(self):
        # airflow dags list-jobs [-h] [-d DAG_ID] [--limit LIMIT] [-o table, json, yaml, plain] [--state STATE] [-v]
        res = run_command(f"airflow tasks list {self.dag_name}")


    # task operator
    def get_dag_all_tasks_status(self, exec_date) -> list:
        '''Get the status of all task instances in a dag run'''
        # airflow tasks states-for-dag-run [-h] [-o table, json, yaml, plain] [-v] dag_id execution_date_or_run_id
        res = run_command(f"airflow tasks states-for-dag-run {self.dag_name} {exec_date}")
        header = ['dag_id', 'execution_date', 'task_id', 'state', 'state_date', 'end_date']
        rows = res[0].split('\n')[2:]
        li = []
        for row in rows:
            p=0
            di = {}
            try:
                for i, item in enumerate(row.split('|')):
                    # print(f"inside ---> {item.strip()}\n{i}:{item}")
                    di[header[p]] = item.strip()
                    if i % (len(header)-1) == 0 and i>0:
                        p=0
                        li.append(di)
                        di={}
                    p=p+1
            except:
                pass
        return li


    def get_tasks_list(self) -> list:
        '''returns list of task names ["task1", "task2", ...]'''
        # airflow tasks list [-h] [-S SUBDIR] [-t] [-v] dag_id
        res = run_command(f"airflow tasks list {self.dag_name}")
        return res.split('\n')


    def get_task_status(self, task_id, exec_date):
        # airflow tasks state [-h] [-S SUBDIR] [-v] dag_id task_id execution_date_or_run_id
        res = run_command(f"airflow tasks state {self.dag_name} {task_id} {exec_date}")
        return res

