import axios from "axios";

var Interval;
var holiday;
var RealtimeFundcode = null;
var RealtimeIndcode = null;
var fundListM = [];
var showBadge = 1;
var BadgeContent = 1;
var BadgeType = 1;
var userId = null;

var getGuid = () => {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (
    c
  ) {
    var r = (Math.random() * 16) | 0,
      v = c == "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}
var getHoliday = () => {
  let url = "http://x2rr.github.io/funds/holiday.json";
  return axios.get(url);
};
var checkHoliday = date => {
  var nowMonth = date.getMonth() + 1;
  var nowYear = date.getFullYear();
  var strDate = date.getDate();
  if (nowMonth >= 1 && nowMonth <= 9) {
    nowMonth = "0" + nowMonth;
  }
  if (strDate >= 0 && strDate <= 9) {
    strDate = "0" + strDate;
  }

  let check = false;
  var nowDate = nowMonth + "-" + strDate;
  let holidayList = holiday.data;
  for (const year in holidayList) {
    if (holidayList.hasOwnProperty(year)) {
      const yearData = holidayList[year];
      if (year == nowYear) {
        for (const day in yearData) {
          if (yearData.hasOwnProperty(day)) {
            const dayData = yearData[day];
            if (nowDate == day && dayData.holiday) {
              check = true;
            }
          }
        }
      }
    }
  }
  return check;
};

var toNum = a => {
  var a = a.toString();
  var c = a.split(".");
  var num_place = ["", "0", "00", "000", "0000"],
    r = num_place.reverse();
  for (var i = 0; i < c.length; i++) {
    var len = c[i].length;
    c[i] = r[len] + c[i];
  }
  var res = c.join("");
  return res;
};

var cpr_version = (a, b) => {
  var _a = toNum(a),
    _b = toNum(b);
  if (_a == _b) console.log("版本号相同！版本号为：" + a);
  if (_a > _b) console.log("版本号" + a + "是新版本！");
  if (_a < _b) console.log("版本号" + b + "是新版本！");
};

var isDuringDate = () => {

  //时区转换为东8区
  var zoneOffset = 8;
  var offset8 = new Date().getTimezoneOffset() * 60 * 1000;
  var nowDate8 = new Date().getTime();
  var curDate = new Date(nowDate8 + offset8 + zoneOffset * 60 * 60 * 1000);

  if (checkHoliday(curDate)) {
    return false;
  }
  var beginDateAM = new Date();
  var endDateAM = new Date();
  var beginDatePM = new Date();
  var endDatePM = new Date();

  beginDateAM.setHours(9, 30, 0);
  endDateAM.setHours(11, 35, 0);
  beginDatePM.setHours(13, 0, 0);
  endDatePM.setHours(15, 5, 0);
  if (curDate.getDay() == "6" || curDate.getDay() == "0") {
    return false;
  } else if (curDate >= beginDateAM && curDate <= endDateAM) {
    return true;
  } else if (curDate >= beginDatePM && curDate <= endDatePM) {
    return true;
  } else {
    return false;
  }
};

var formatNum = val => {
  let num = parseFloat(val);
  let absNum = Math.abs(num);
  if (absNum < 10) {
    return num.toFixed(2);
  } else if (absNum < 100) {
    return num.toFixed(1);
  } else if (absNum < 1000) {
    return num.toFixed(0);
  } else if (absNum < 10000) {
    return (num / 1000).toFixed(1) + 'k';
  } else if (absNum < 1000000) {
    return (num / 1000).toFixed(0) + 'k';
  } else if (absNum < 10000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else {
    return (num / 1000000).toFixed(0) + 'M';
  }
}

var setBadge = (fundcode, Realtime, type) => {
  let fundStr = null;
  if (type == 3) {
    let url =
      "https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f3&secids=" +
      fundcode +
      "&_=" +
      new Date().getTime();
    axios.get(url).then((res) => {
      let data = res.data.data.diff;
      let text = data[0].f3.toString();
      let num = data[0].f3;
      chrome.browserAction.setBadgeText({
        text: text
      });
      let color = Realtime ?
        num >= 0 ?
        "#F56C6C" :
        "#4eb61b" :
        "#4285f4";
      chrome.browserAction.setBadgeBackgroundColor({
        color: color
      });
    });
  } else {
    if (type == 1) {
      fundStr = fundcode;
    } else {
      fundStr = fundListM.map((val) => val.code).join(",");
    }

    let url =
      "https://fundmobapi.eastmoney.com/FundMNewApi/FundMNFInfo?pageIndex=1&pageSize=200&plat=Android&appType=ttjj&product=EFund&Version=1&deviceid=" + userId + "&Fcodes=" +
      fundStr;
    axios
      .get(url)
      .then((res) => {
        let allAmount = 0;
        let allGains = 0;
        let textStr = null;
        let sumNum = 0;
        if (type == 1) {
          let val = res.data.Datas[0];
          let data = {
            fundcode: val.FCODE,
            name: val.SHORTNAME,
            jzrq: val.PDATE,
            dwjz: isNaN(val.NAV) ? null : val.NAV,
            gsz: isNaN(val.GSZ) ? null : val.GSZ,
            gszzl: isNaN(val.GSZZL) ? 0 : val.GSZZL,
            gztime: val.GZTIME,
            num: 0
          };
          let slt = fundListM.filter(
            (item) => item.code == data.fundcode
          );
          if (!slt.length) {
            return false;
          }
          data.num = slt[0].num;
          var sum = 0;

          let num = data.num ? data.num : 0;

          if (val.PDATE != "--" && val.PDATE == val.GZTIME.substr(0, 10)) {
            data.gsz = val.NAV;
            data.gszzl = isNaN(val.NAVCHGRT) ? 0 : val.NAVCHGRT;
            sum = (
              (data.dwjz - data.dwjz / (1 + data.gszzl * 0.01)) *
              num
            ).toFixed(1);
          } else {
            if (data.gsz) {
              sum = ((data.gsz - data.dwjz) * num).toFixed(1);
            }

          }


          if (BadgeType == 1) {
            textStr = data.gszzl;
            sumNum = textStr;
          } else {
            if (num != 0) {
              sumNum = sum;
              textStr = formatNum(sum);
            } else {
              sumNum = "0";
              textStr = "0";
            }
          }

        } else {
          res.data.Datas.forEach((val) => {
            let slt = fundListM.filter(
              (item) => item.code == val.FCODE
            );
            let num = slt[0].num ? slt[0].num : 0;
            let NAV = isNaN(val.NAV) ? null : val.NAV;
            allAmount += NAV * num;
            var sum = 0;
            if (val.PDATE != "--" && val.PDATE == val.GZTIME.substr(0, 10)) {
              let NAVCHGRT = isNaN(val.NAVCHGRT) ? 0 : val.NAVCHGRT;
              sum = (NAV - NAV / (1 + NAVCHGRT * 0.01)) * num
            } else {
              let gsz = isNaN(val.GSZ) ? null : val.GSZ
              if (gsz && NAV) {
                sum = (gsz - NAV) * num
              }
            }
            allGains += sum;

          });
          if (BadgeType == 1) {
            if (allAmount == 0 || allGains == 0) {
              sumNum = "0"
              textStr = "0"
            } else {
              textStr = (100 * allGains / allAmount).toFixed(2);
              sumNum = textStr
            }

          } else {
            sumNum = allGains;
            textStr = formatNum(allGains);
          }
        }


        chrome.browserAction.setBadgeText({
          text: textStr
        });
        let color = Realtime ?
          sumNum >= 0 ?
          "#F56C6C" :
          "#4eb61b" :
          "#4285f4";
        chrome.browserAction.setBadgeBackgroundColor({
          color: color
        });

      })
      .catch((error) => {

      });
  }



};


var startInterval = (RealtimeFundcode, type = 1) => {
  endInterval(Interval);
  let Realtime = isDuringDate();
  RealtimeFundcode = RealtimeFundcode;
  setBadge(RealtimeFundcode, Realtime, type);
  let time = 2 * 60 * 1000;
  if (type == 3) {
    time = 10 * 1000;
  }
  Interval = setInterval(() => {
    if (isDuringDate()) {
      setBadge(RealtimeFundcode, true, type);
    } else {
      chrome.browserAction.setBadgeBackgroundColor({
        color: "#4285f4"
      });
    }
  }, time);
};

var endInterval = () => {
  clearInterval(Interval);
  chrome.browserAction.setBadgeText({
    text: ""
  });
};

var runStart = (RealtimeFundcode, RealtimeIndcode) => {

  if (showBadge == 1 && BadgeContent == 1) {
    if (RealtimeFundcode) {
      startInterval(RealtimeFundcode);
    } else {
      endInterval();
    }
  } else if (showBadge == 1 && BadgeContent == 2) {
    startInterval(null, 2);
  } else if (showBadge == 1 && BadgeContent == 3) {
    if (RealtimeIndcode) {
      startInterval(RealtimeIndcode, 3);
    } else {
      endInterval();
    }

  } else {
    endInterval();
  }

};


var getData = () => {
  chrome.storage.sync.get(["holiday", "fundListM", "RealtimeFundcode", "RealtimeIndcode", "showBadge", "BadgeContent", "BadgeType", "userId"], res => {
    RealtimeFundcode = res.RealtimeFundcode ? res.RealtimeFundcode : null;
    RealtimeIndcode = res.RealtimeIndcode ? res.RealtimeIndcode : null;
    fundListM = res.fundListM ? res.fundListM : [];
    showBadge = res.showBadge ? res.showBadge : 1;
    BadgeContent = res.BadgeContent ? res.BadgeContent : 1;
    BadgeType = res.BadgeType ? res.BadgeType : 1;
    if (res.userId) {
      userId = res.userId;
    } else {
      userId = getGuid();
      chrome.storage.sync.set({
        userId: userId,
      });
    }
    if (res.holiday) {
      holiday = res.holiday;
      runStart(RealtimeFundcode, RealtimeIndcode);
    } else {
      getHoliday().then(res => {
        chrome.storage.sync.set({
            holiday: res.data
          },
          () => {
            holiday = res.data;
            runStart(RealtimeFundcode, RealtimeIndcode);
          }
        );
      }).catch(err => {
        chrome.storage.sync.set({
            holiday: {}
          },
          () => {
            holiday = {};
            runStart(RealtimeFundcode, RealtimeIndcode);
          }
        );
      });
    }
  });
}

getData();

chrome.contextMenus.create({
  title: "以独立窗口模式打开",
  contexts: ["browser_action"],
  onclick: () => {
    chrome.windows.create({
      url: chrome.runtime.getURL("popup/popup.html"),
      width: 700,
      height: 550,
      top: 200,
      type: "popup",
    }, (function (e) {
      chrome.windows.update(e.id, {
        focused: true
      })
    }))
  }
})

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type == "DuringDate") {
    let DuringDate = isDuringDate();
    sendResponse({
      farewell: DuringDate
    });
  }
  if (request.type == "refresh") {
    getData();
  }
  if (request.type == "refreshHoliday") {
    holiday = request.data;
  }
  if (request.type == "refreshBadgeAllGains") {
    let allAmount = 0;
    let allGains = 0;
    let sumNum = 0;
    request.data.forEach((val) => {
      let slt = fundListM.filter(
        (item) => item.code == val.FCODE
      );
      let num = slt[0].num ? slt[0].num : 0;
      let NAV = isNaN(val.NAV) ? null : val.NAV;
      allAmount += NAV * num;
      var sum = 0;
      if (val.PDATE != "--" && val.PDATE == val.GZTIME.substr(0, 10)) {
        let NAVCHGRT = isNaN(val.NAVCHGRT) ? 0 : val.NAVCHGRT;
        sum = (NAV - NAV / (1 + NAVCHGRT * 0.01)) * num
      } else {
        let gsz = isNaN(val.GSZ) ? null : val.GSZ;
        if (gsz != null && NAV != null) {
          sum = (gsz - NAV) * num;
        }

      }
      allGains += sum;

    });
    let textStr = null;
    if (BadgeType == 1) {
      if (allAmount == 0 || allGains == 0) {
        textStr = "0"
        sumNum = "0"
      } else {
        textStr = (100 * allGains / allAmount).toFixed(2);
        sumNum = textStr
      }

    } else {
      textStr = formatNum(allGains);
      sumNum = allGains;
    }

    chrome.browserAction.setBadgeText({
      text: textStr
    });
    let color = isDuringDate() ?
      sumNum >= 0 ?
      "#F56C6C" :
      "#4eb61b" :
      "#4285f4";
    chrome.browserAction.setBadgeBackgroundColor({
      color: color
    });
  }
  if (request.type == "endInterval") {
    endInterval();
  }
  if (request.type == "startInterval") {
    startInterval(request.id);
  }
  if (request.type == "refreshOption") {
    switch (request.data.type) {
      case "showBadge":
        showBadge = request.data.value;
        break;
      case "BadgeContent":
        BadgeContent = request.data.value;
        break;
      case "BadgeType":
        BadgeType = request.data.value;
        break;
    }
    getData();
  }
  if (request.type == "refreshBadge") {
    let textstr = null;
    let num = 0;
    if (BadgeType == 1) {
      textstr = request.data.gszzl;
      num = request.data.gszzl;
    } else {
      num = request.data.gains;
      textstr = formatNum(request.data.gains);
    }
    chrome.browserAction.setBadgeText({
      text: textstr
    });
    let color = isDuringDate() ?
      num >= 0 ?
      "#F56C6C" :
      "#4eb61b" :
      "#4285f4";
    chrome.browserAction.setBadgeBackgroundColor({
      color: color
    });
  }
});