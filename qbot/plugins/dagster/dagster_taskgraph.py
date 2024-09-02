from quant_project.datafeed import mongo_utils

from dagster import asset  # noqa F401
from dagster import get_dagster_logger  # noqa F401
from dagster import DynamicOut, DynamicOutput, graph, job, op


@op(out=DynamicOut())
def load_bondlist():
    cols = ["code", "bond_short_name", "stk_code", "list_date", "delist_date"]
    filters = {col: 1 for col in cols}
    filters["_id"] = 0
    items = mongo_utils.get_db()["cb_basic"].find({}, filters)
    items = list(items)
    items = ["1", "2", "3"]
    for idx, item in enumerate(items):
        yield DynamicOutput(item, mapping_key=str(idx))


@op
def update_factor_chg(item):
    print("step...")
    return item


@op(name="update_close")
def update_factor_close(item):
    print(item)
    return item


@graph
def task_graph(item):
    update_factor_close(item)
    results = update_factor_chg(item)
    return results


@op
def merge_datas(results):
    print("merging...")


@job
def cb_task_job():
    bonds = load_bondlist()
    results = bonds.map(task_graph)
    print(results.collect())
    merge_datas(results.collect())


one_code_job = task_graph.to_job("task_graph_job")

if __name__ == "__main__":
    result = cb_task_job.execute_in_process()
