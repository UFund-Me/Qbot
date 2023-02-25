



export const dateFormat = (dateInput, format = 'yyyy-MM-dd'):string => {
  const dateObj = new Date(dateInput)

  if (!dateObj.getFullYear()) {
    console.log(dateInput, dateObj)
    return dateInput
  }

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
  const [year, month, date, hour, minute, second] = [
    dateObj.getFullYear(),
    dateObj.getMonth(),
    dateObj.getDate(),
    dateObj.getHours(),
    dateObj.getMinutes(),
    dateObj.getSeconds()
  ]

  const dateMap = {
    yyyy: year, // 年份

    eM: months[month], // 英语月份
    MM: (month + 1 + '').padStart(2, '0'), // 月份，两位数加0
    M: month + 1, // 月份，不加0

    dd: (date + '').padStart(2, '0'), // 日期，两位数加0
    d: date, // 日期，不加0

    HH: (hour + '').padStart(2, '0'), // 24小时进制，两位数加0
    H: hour,
    hh: (hour % 12 + '').padStart(2, '0'), // 12小时进制
    h: hour % 12,
    mer: hour > 12 ? 'pm' : 'am', // 上午还是下午

    mm: (minute + '').padStart(2, '0'), // 分钟
    m: minute,

    ss: (second + '').padStart(2, '0'), // 秒
    s: second
  }

  const reg = /eM|mer|yyyy|MM|M|dd|d|HH|H|hh|h|mm|m|ss|s/g

  return format.replace(reg, (match) => dateMap[match])
}

/**
 * 数字四舍五入同时保留几位小数
 * @param num 数字
 * @param fractionDigits 保留几位小数
 */
export const roundToFix = (num: number|string, fractionDigits: number = 2):number=>{
  const powNum = Math.pow(10, fractionDigits)
  return Number((Math.round(Number(num) * powNum) / powNum).toFixed(fractionDigits))
}

/**
 * 不允许选未来的日期
 */
export const disabledFuture = (date) => {
  const selectDate = new Date(date).getTime()
  const now = Date.now()
  return selectDate > now
}

/**
 * 格式化成百分比字符串
 */
export const formatPercentVal = (val: number) => {
  return roundToFix(val * 100) + '%' 
}

/** 
 * jsonp 获取数据 
 * */
window['getJSONP'] = (url: string,callback: Function, opt?:{
  onload?: Function
}) => {
  var cbnum = "cb" + window['getJSONP'].counter++;
  var cbname = "getJSONP." + cbnum;

  if (url.indexOf("?") == -1) {
     url += "?callback=" + cbname;
     url += "?cb=" + cbname;
  } else {
     url += "&callback=" + cbname;
     url += "&cb=" + cbname;
  }

  var script = document.createElement("script");
  script.referrerPolicy = "no-referrer"
  window['getJSONP'][cbnum] = function (response) {
     try {
        callback(response);
     }
     finally {
        delete window['getJSONP'][cbnum];
        script.parentNode!.removeChild(script);
     }
  };

  script.src = url
  if(opt && opt.onload) {
    script.onload = ()=>{
      opt.onload!()
    }
  }
  
  document.body.appendChild(script);
}
window['getJSONP'].counter = 0;