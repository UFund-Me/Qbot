"""
一个简单展示 qdii 实时净值预测的例子，最大限度的利用缓存而减少网络请求
"""

import pandas as pd
import xalpha as xa
import logging

xa.set_backend(backend="csv", path="../../../lof/data", precached="20200103")

logger = logging.getLogger("xalpha")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

from xalpha import investinghooks


@xa.universal.lru_cache_time(ttl=180)
def cached_get_rt(code, **kws):
    return xa.get_rt(code, handler=False)


@xa.universal.lru_cache_time(ttl=1800)
def cached_get_bar(code, *args, **kws):
    if code.startswith("commodities/"):
        kws["handler"] = False
        return xa.get_bar(code, *args, **kws)
    return None


# xa.set_handler(method="rt", f=cached_get_rt)
# xa.set_handler(method="bar", f=cached_get_bar)


qdiis = [
    "SH501018",
    "SZ160416",
    "SZ161129",
    "SZ160723",
    "SZ160216",
    "SZ162411",
    "SZ163208",
    "SZ162719",
    "SZ165513",
    "SZ161815",  # fr
    "SZ161116",  # lu
    "SZ164701",
    "SZ160719",
    "SZ164824",
    # "SH513030",
    # "SZ160140",
    # "SZ165510",
    # "SZ164906",
    "SH513050",
]
nonqdiis = [
    "SH501021",
    "SH513880",
    "SH513520",
    "SH513000",
    "SH510510",
    "SZ159922",
    "SH510500",
    "SH512500",
    "SZ159920",
]
data = {
    "code": [],
    "name": [],
    "t1": [],
    "t0": [],
    "now": [],
    "t1rate": [],
    "t0rate": [],
    "position": [],
}

for c in qdiis:
    p = xa.QDIIPredict(c, fetch=True, save=True, positions=True)
    try:
        data["t1"].append(round(p.get_t1(return_date=False), 4))
        data["t1rate"].append(round(p.get_t1_rate(return_date=False), 2))
        try:
            data["t0"].append(round(p.get_t0(return_date=False), 4))
            data["t0rate"].append(round(p.get_t0_rate(return_date=False), 2))
        except ValueError:
            data["t0"].append("-")
            data["t0rate"].append("-")
        data["position"].append(round(p.get_position(return_date=False), 3))
        data["now"].append(xa.get_rt(c)["current"])
        data["code"].append(c)
        data["name"].append(xa.get_rt(c)["name"])
    except xa.exceptions.NonAccurate as e:
        print("%s cannot be predicted exactly now" % c)
        print(e.reason)

for c in nonqdiis:
    try:
        p = xa.RTPredict(c)
        data["t0"].append(round(p.get_t0(return_date=False), 4))
        data["t0rate"].append(round(p.get_t0_rate(return_date=False), 2))
        data["t1"].append(xa.get_rt("F" + c[2:])["current"])
        data["t1rate"].append("-")
        data["position"].append("-")
        data["now"].append(xa.get_rt(c)["current"])
        data["code"].append(c)
        data["name"].append(xa.get_rt(c)["name"])
    except xa.exceptions.NonAccurate as e:
        print("%s cannot be predicted exactly now" % c)
        print(e.reason)
df = pd.DataFrame(data)

htmlstr = (
    """<html>
<meta charset="UTF-8">

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.css">
<script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js"></script>

<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.js"></script>

<script>
  $(document).ready( function () {
    $('#df').DataTable({"scrollY": "88%",
  "scrollCollapse": true,
  "paging": false,
  "fixedHeader": true
});
} );
</script>
<style>
    td, th {
        text-align: center;
    }
    #df tbody tr:hover {
    background-color: #ffff99;
    }
</style>"""
    + df.to_html(table_id="df", index=False)
    + "</html>"
)


with open("demo.html", "w") as f:
    f.writelines([htmlstr])
