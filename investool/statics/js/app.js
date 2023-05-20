$(document).ready(function () {
  // 初始化 materialize
  M.AutoInit();

  // 导航栏激活
  var currentNav = $(location).attr("pathname");
  if (currentNav.startsWith("/fund")) {
    $("#nav-fund").addClass("active");
    $("#nav-fund").siblings().removeClass("active");
  } else if (currentNav == "/about") {
    $("#nav-about").addClass("active");
    $("#nav-about").siblings().removeClass("active");
  } else if (currentNav == "/comment") {
    $("#nav-comment").addClass("active");
    $("#nav-comment").siblings().removeClass("active");
  } else if (currentNav == "/materials") {
    $("#nav-materials").addClass("active");
    $("#nav-materials").siblings().removeClass("active");
  } else {
    $("#nav-stock").addClass("active");
    $("#nav-stock").siblings().removeClass("active");
  }

  // 筛选表单中开关显示检测表单
  $("#selector_with_checker").click(function () {
    $("#checker_options").toggle();
  });

  var human_float_slice = function (floats, unit) {
    var result = "";
    for (i = 0; i < floats.length; i++) {
      var n = floats[i];
      if (unit == "元") {
        var yi = n / 100000000.0;
        if (Math.abs(yi) >= 1) {
          result += yi.toFixed(2) + "亿元<br/>";
        } else if (n / 10000.0 >= 1) {
          result += yi.toFixed(2) + "万元<br/>";
        }
      } else {
        result += n.toFixed(2) + unit + "<br/>";
      }
    }
    return result;
  };

  // 基本面选股请求处理
  $("#selector_submit_btn").click(function () {
    $(this).addClass("disabled");
    $("#model_header").text($(this).text() + "中，请稍候...");
    $("#load_modal").modal()[0].M_Modal.options.dismissible = false;
    $("#load_modal").modal("open");
    $.ajax({
      url: "/selector",
      type: "post",
      data: $("#selector_form").serialize(),
      success: function (data) {
        if (data.Error) {
          $("#err_msg").text(data.Error);
          $("#error_modal").modal("open");
          $("#selector_submit_btn").removeClass("disabled");
          $("#load_modal").modal("close");
          return;
        }
        if (data.Stocks.length == 0) {
          $(".dropdown-structure").addClass("hide");
          $("#selector_result #result_table").html(
            '<div class="row"><p class="center flow-text">无法找到符合条件的股票</p></div>'
          );
        } else {
          $.each(data.Stocks, function (i, stock) {
            var cm = stock.code.split(".");
            if (stock.right_price != "--") {
              stock.right_price = stock.right_price.toFixed(2);
            }
            $("#selector_result tbody").append(
              "<tr>" +
                '<td><span class="copybtn waves-effect waves-red" data-clipboard-text="' +
                cm[0] +
                '">' +
                cm[0] +
                //     '<i class="material-icons tiny">content_copy</i></span></td>' +
                '<td><a target="_blank" href="http://quote.eastmoney.com/' +
                cm[1] +
                cm[0] +
                '.html">' +
                stock.name +
                "</a></td>" +
                '<td class="hide st_1">' +
                stock.industry +
                "</td>" +
                '<td class="hide st_2">' +
                stock.keywords +
                "</td>" +
                '<td class="hide st_3">' +
                stock.company_profile +
                "</td>" +
                '<td class="hide st_4">' +
                stock.main_forms +
                "</td>" +
                '<td class="hide st_5">' +
                (stock.byys_ration * 100).toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_6">' +
                stock.report_date_name +
                "</td>" +
                '<td class="hide st_7">' +
                stock.report_opinion +
                "</td>" +
                '<td class="hide st_8">' +
                stock.jzpg +
                "</td>" +
                '<td class="hide st_9">' +
                stock.latest_roe +
                "%" +
                "</td>" +
                '<td class="hide st_55">' +
                stock.latest_fina_roe +
                "%" +
                "</td>" +
                '<td class="hide st_10">' +
                stock.roe_tbzz.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_11">' +
                human_float_slice(stock.roe_5y, "%") +
                "</td>" +
                '<td class="hide st_12">' +
                stock.latest_eps +
                "</td>" +
                '<td class="hide st_13">' +
                stock.eps_tbzz.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_14">' +
                human_float_slice(stock.eps_5y, "") +
                "</td>" +
                '<td class="hide st_15">' +
                stock.total_income +
                "</td>" +
                '<td class="hide st_16">' +
                stock.total_income_tbzz.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_17">' +
                human_float_slice(stock.total_income_5y, "元") +
                "</td>" +
                '<td class="hide st_18">' +
                stock.net_profit +
                "</td>" +
                '<td class="hide st_19">' +
                stock.net_profit_tbzz.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_20">' +
                human_float_slice(stock.net_profit_5y, "元") +
                "</td>" +
                '<td class="hide st_21">' +
                stock.zxgxl.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_22">' +
                stock.fina_report_date +
                "</td>" +
                '<td class="hide st_23">' +
                stock.fina_appoint_publish_date +
                "</td>" +
                '<td class="hide st_24">' +
                stock.fina_actual_publish_date +
                "</td>" +
                '<td class="hide st_25">' +
                stock.total_market_cap +
                "</td>" +
                '<td class="hide st_26">' +
                stock.price +
                "元" +
                "</td>" +
                '<td class="hide st_27">' +
                stock.right_price +
                "元" +
                "</td>" +
                '<td class="hide st_28">' +
                stock.price_space +
                "</td>" +
                '<td class="hide st_29">' +
                (stock.hv * 100).toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_30">' +
                stock.zxfzl.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_31">' +
                stock.fzldb.toFixed(2) +
                "</td>" +
                '<td class="hide st_32">' +
                stock.netprofit_growthrate_3_y.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_33">' +
                stock.income_growthrate_3_y.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_34">' +
                stock.listing_yield_year.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_35">' +
                stock.listing_volatility_year.toFixed(2) +
                "%" +
                "</td>" +
                '<td class="hide st_36">' +
                stock.pe.toFixed(2) +
                "</td>" +
                '<td class="hide st_37">' +
                stock.peg.toFixed(2) +
                "</td>" +
                '<td class="hide st_38">' +
                stock.org_rating +
                "</td>" +
                '<td class="hide st_39">' +
                stock.profit_predict +
                "</td>" +
                '<td class="hide st_40">' +
                stock.valuation_syl +
                "</td>" +
                '<td class="hide st_41">' +
                stock.valuation_sjl +
                "</td>" +
                '<td class="hide st_42">' +
                stock.valuation_sxol +
                "</td>" +
                '<td class="hide st_43">' +
                stock.valuation_sxnl +
                "</td>" +
                '<td class="hide st_44">' +
                stock.hyjzsp +
                "</td>" +
                '<td class="hide st_45">' +
                stock.ztzd +
                "</td>" +
                '<td class="hide st_46">' +
                human_float_slice(stock.mll_5y, "%") +
                "</td>" +
                '<td class="hide st_47">' +
                human_float_slice(stock.jll_5y, "%") +
                "</td>" +
                '<td class="hide st_48">' +
                stock.listing_date +
                "</td>" +
                '<td class="hide st_49">' +
                stock.netcash_operate +
                "</td>" +
                '<td class="hide st_50">' +
                stock.netcash_invest +
                "</td>" +
                '<td class="hide st_51">' +
                stock.netcash_finance +
                "</td>" +
                '<td class="hide st_52">' +
                stock.netcash_free +
                "</td>" +
                '<td class="hide st_53">' +
                stock.free_holders_top_10 +
                "</td>" +
                '<td class="hide st_54">' +
                stock.main_money_net_inflows +
                "</td>" +
                "</tr>"
            );
          });
        }
        $("title").text(data.PageTitle);
        $("#stock_forms").remove();
        $("#selector_result").removeClass("hide");
        $("html, body").animate({ scrollTop: 0 }, 0);
        $("#load_modal").modal("close");
      },
    });
  });

  // 个股检测请求处理
  $("#checker_submit_btn").click(function () {
    if ($("#checker_keyword").val() == "") {
      $("#err_msg").text("请填写股票代码或简称");
      $("#error_modal").modal("open");
      return;
    }
    $(this).addClass("disabled");
    $("#model_header").text($(this).text() + "中，请稍候...");
    $("#load_modal").modal()[0].M_Modal.options.dismissible = false;
    $("#load_modal").modal("open");
    $.ajax({
      url: "/checker",
      type: "post",
      data: $("#checker_form").serialize(),
      success: function (data) {
        if (data.Error) {
          $("#err_msg").text(data.Error);
          $("#error_modal").modal("open");
          $("#checker_submit_btn").removeClass("disabled");
          $("#load_modal").modal("close");
          return;
        }
        $("title").text(data.PageTitle);
        $("#stock_forms").remove();
        $("#checker_results").removeClass("hide");
        if (data.Results.length == 0) {
          $("#checker_results h4").text("暂不支持对该股进行检测");
        } else {
          $.each(data.Results, function (i, result) {
            var cm = data.StockNames[i].split("-")[1].split(".");
            $("#checker_results").append(
              '<br/><div class="divider"></div><br/><div id="checker_result_' +
                i +
                '"><div class="row"><a target="_blank" href="http://quote.eastmoney.com/' +
                cm[1] +
                cm[0] +
                '.html">' +
                data.StockNames[i] +
                "</a><br/>当前检测财报数据来源:" +
                data.FinaReportNames[i] +
                "<br/>最新财报预约发布日期:" +
                data.FinaAppointPublishDates[i] +
                "</div>" +
                '<table class="centered striped">' +
                '<thead><tr><th width="30%">指标</th><th width="40%">描述</th><th width="30%">结果</th></tr></thead>' +
                "<tbody></tbody>" +
                "</table>" +
                "</div>"
            );
            $.each(result, function (k, v) {
              okdesc = "❌";
              if (v.ok == "true") {
                okdesc = "✅";
              }
              $(`#checker_result_${i} tbody`).append(
                "<tr><td>" +
                  k +
                  "</td><td>" +
                  v.desc +
                  "</td><td>" +
                  okdesc +
                  "</td></tr>"
              );
            });
            $(`#checker_result_${i} tbody`).append(
              "<tr><td>主力资金净流入</td><td>" +
                data.MainMoneyNetInflows[i] +
                "</td><td>--</td></tr>"
            );
            $(`#checker_result_${i}`).append(
              '<div class="row">' +
                '<br><h5 class="center">年报数据趋势概览</h5>' +
                '<div class="col s12">' +
                '<div id="line-chart-' + i + '" style="width:100%;height:400px;"></div>' +
                "</div>" +
                "</div>"
            );
            var lineChart = echarts.init(document.querySelector(`#line-chart-${i}`));
            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'cross' }
                },
                legend: {
                    data: data.Lines[i].legends,
                    top: 'bottom'
                },
                toolbox: {
                    show: true,
                    feature: {
                        dataView: {},
                        magicType: { type: ['bar'] },
                        restore: {},
                    }
                },
                xAxis: {
                    data: data.Lines[i].xAxis
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: "ROE",
                        type: 'line',
                        data: data.Lines[i].data[0]
                    },
                    {
                        name: "EPS",
                        type: 'line',
                        data: data.Lines[i].data[1]
                    },
                    {
                        name: "ROA",
                        type: 'line',
                        data: data.Lines[i].data[2]
                    },
                    {
                        name: "毛利率",
                        type: 'line',
                        data: data.Lines[i].data[3]
                    },
                    {
                        name: "净利率",
                        type: 'line',
                        data: data.Lines[i].data[4]
                    },
                    {
                        name: "营收",
                        type: 'line',
                        data: data.Lines[i].data[5]
                    },
                    {
                        name: "毛利润",
                        type: 'line',
                        data: data.Lines[i].data[6]
                    },
                    {
                        name: "净利润",
                        type: 'line',
                        data: data.Lines[i].data[7]
                    },
                ]
            };
            lineChart.setOption(option);
            window.onresize = function() { lineChart.resize(); };
          });
        }
        $("html, body").animate({ scrollTop: 0 }, 0);
        $("#load_modal").modal("close");
      },
    });
  });

  // 返回顶部按钮
  $("#to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 500);
  });
  // 按钮通过点击展示
  $(".fixed-action-btn").floatingActionButton({
    hoverEnabled: false,
  });

  // 导出结果csv文件
  $(".export-result-btn").click(function (e) {
    tableExport("selector_result_table", "investool-exported", "csv");
  });

  // 展示字段设置
  var checkboxLimit = 10;
  var checkboxCountCheck = function () {
    var checkedCount = $(".dropdown-content input[type=checkbox]:checked")
      .length;
    if (checkedCount > checkboxLimit && checkedCount % 5 == 1) {
      M.toast({
        html: "展示信息过多，导出CSV详情文件即可在本地查看完整信息哦~",
        classes: "rounded",
      });
    }
  };

  // 下拉框设置
  $(".dropdown-trigger").dropdown({
    constrainWidth: true,
    closeOnClick: false,
  });
  $(".dropdown-content>li>a").css("color", "#000000");
  $(".dropdown-content>li>a").css("font-size", "11px");
  $(".dropdown-content>li>a").css("font-weight", "normal");

  for (let i = 1; i <= 55; i++) {
    $(`#sf_${i}`).change(function () {
      checkboxCountCheck();
      $(`.st_${i}`).toggleClass("hide");
    });
  }

  // 点击复制
  var clipboard = new ClipboardJS(".copybtn");
  clipboard.on("success", function (e) {
    M.toast({ html: "已复制代码至剪贴板" });
  });

  // 基金字段
  for (let i = 1; i <= 23; i++) {
    $(`#f${i}`).change(function () {
      $(`.t${i}`).toggleClass("hide");
      if (this.checked) {
        localStorage.setItem(`t${i}`, 1);
      } else {
        localStorage.removeItem(`t${i}`);
      }
    });
    if (localStorage[`t${i}`] == 1) {
      $(`.t${i}`).removeClass("hide");
      $(`#f${i}`).attr("checked", "true");
    }
  }

  // 设置排序图标
  $(".sortable").click(function () {
    var s = $(this).find("a").attr("sort");
    localStorage.setItem("fund_sort", s);
  });
  var fund_sort = localStorage["fund_sort"];
  if (fund_sort === null) {
    fund_sort = "0";
  }
  $(`.sortable a[sort='${fund_sort}'] i`).removeClass("hide");

  // 基金检测表单中开关显示检测持仓股票
  $("#check_stocks").click(function () {
    $("#checker_options").toggleClass("hide");
  });

  // 基金检测提交
  $("#check_fund_submit_btn").click(function () {
    if ($("#fundcode").val() == "") {
      $("#err_msg").text("请填写基金代码");
      $("#error_modal").modal("open");
      return;
    }
    $(this).addClass("disabled");
    $("#model_header").text($(this).text() + "中，请稍候...");
    $("#load_modal").modal()[0].M_Modal.options.dismissible = false;
    $("#load_modal").modal("open");
    $.ajax({
      url: "/fund/check",
      type: "post",
      data: $("#fundcheck_form").serialize(),
      success: function (data) {
        if (data.Error) {
          $("#err_msg").text(data.Error);
          $("#error_modal").modal("open");
          $("#check_fund_submit_btn").removeClass("disabled");
          $("#load_modal").modal("close");
          return;
        }

        $("title").text(data.PageTitle);
        $("#index_content").remove();
        $("#fund_check_results").removeClass("hide");

        $.each(data.Funds, function (code, fund) {
          var year_1_rank_ratio = "❌";
          if (
            fund.performance.year_1_rank_ratio < data.Param.year_1_rank_ratio
          ) {
            year_1_rank_ratio = "✅";
          }
          var year_2_rank_ratio = "❌";
          if (
            fund.performance.year_2_rank_ratio <
            data.Param.this_year_235_rank_ratio
          ) {
            year_2_rank_ratio = "✅";
          }
          var year_3_rank_ratio = "❌";
          if (
            fund.performance.year_3_rank_ratio <
            data.Param.this_year_235_rank_ratio
          ) {
            year_3_rank_ratio = "✅";
          }
          var year_5_rank_ratio = "❌";
          if (
            fund.performance.year_5_rank_ratio <
            data.Param.this_year_235_rank_ratio
          ) {
            year_5_rank_ratio = "✅";
          }
          var this_year_rank_ratio = "❌";
          if (
            fund.performance.this_year_rank_ratio <
            data.Param.this_year_235_rank_ratio
          ) {
            this_year_rank_ratio = "✅";
          }
          var month_6_rank_ratio = "❌";
          if (
            fund.performance.month_6_rank_ratio < data.Param.month_6_rank_ratio
          ) {
            month_6_rank_ratio = "✅";
          }
          var month_3_rank_ratio = "❌";
          if (
            fund.performance.month_3_rank_ratio < data.Param.month_3_rank_ratio
          ) {
            month_3_rank_ratio = "✅";
          }
          var min_scale = "❌";
          if (fund.net_assets_scale / 100000000.0 >= data.Param.min_scale) {
            min_scale = "✅";
          }
          var max_scale = "❌";
          if (fund.net_assets_scale / 100000000.0 <= data.Param.max_scale) {
            max_scale = "✅";
          }
          var manager = "❌";
          if (
            fund.manager.manage_days / 365.0 >=
            data.Param.min_manager_years
          ) {
            manager = "✅";
          }
          var stddev_avg135 = "❌";
          if (fund.stddev.avg_135 <= data.Param.max_135_avg_stddev) {
            stddev_avg135 = "✅";
          }
          var sharp_avg135 = "❌";
          if (fund.sharp.avg_135 >= data.Param.min_135_avg_sharp) {
            sharp_avg135 = "✅";
          }
          var maxretr_avg135 = "❌";
          if (fund.max_retracement.avg_135 <= data.Param.max_135_avg_retr) {
            maxretr_avg135 = "✅";
          }
          $("#fund_check_results").append(
            '<div class="row" id="' +
              fund.code +
              '"><h4 class="center"><a target="_blank" href="http://fund.eastmoney.com/' +
              fund.code +
              '.html">' +
              fund.name +
              "(" +
              fund.code +
              ')</a>检测结果</h4><p class="tiny center">以下所有数据与信息仅供参考，不构成投资建议</p><div class="divider"></div><table class="centered striped"><thead><tr><th width="30%">指标</th><th width="40%">描述</th><th width="30%">结果</th></tr></thead><tbody><tr><td>近1年绩效排名前' +
              data.Param.year_1_rank_ratio +
              "%</td><td>近1年绩效排名前" +
              fund.performance.year_1_rank_ratio.toFixed(2) +
              "%</td><td>" +
              year_1_rank_ratio +
              "</td></tr><tr><td>近2,3,5年及今年来绩效排名前" +
              data.Param.this_year_235_rank_ratio +
              "%</td><td>近2年绩效排名前" +
              fund.performance.year_2_rank_ratio.toFixed(2) +
              "%</td><td>" +
              year_2_rank_ratio +
              "</td></tr><tr><td>近2,3,5年及今年来绩效排名前" +
              data.Param.this_year_235_rank_ratio +
              "%</td><td>近3年绩效排名前" +
              fund.performance.year_3_rank_ratio.toFixed(2) +
              "%</td><td>" +
              year_3_rank_ratio +
              "</td></tr><tr><td>近2,3,5年及今年来绩效排名前" +
              data.Param.this_year_235_rank_ratio +
              "%</td><td>近5年绩效排名前" +
              fund.performance.year_5_rank_ratio.toFixed(2) +
              "%</td><td>" +
              year_5_rank_ratio +
              "</td></tr><tr><td>近2,3,5年及今年来绩效排名前" +
              data.Param.this_year_235_rank_ratio +
              "%</td><td>今年来绩效排名前" +
              fund.performance.this_year_rank_ratio.toFixed(2) +
              "%</td><td>" +
              this_year_rank_ratio +
              "</td></tr><tr><td>近6个月绩效排名前" +
              data.Param.month_6_rank_ratio +
              "%</td><td>近6个月绩效排名前" +
              fund.performance.month_6_rank_ratio.toFixed(2) +
              "%</td><td>" +
              month_6_rank_ratio +
              "</td></tr><tr><td>近3个月绩效排名前" +
              data.Param.month_3_rank_ratio +
              "%</td><td>近3个月绩效排名前" +
              fund.performance.month_3_rank_ratio.toFixed(2) +
              "%</td><td>" +
              month_3_rank_ratio +
              "</td></tr><tr><td>基金规模最低" +
              data.Param.min_scale +
              "亿</td><td>基金规模" +
              (fund.net_assets_scale / 100000000.0).toFixed(2) +
              "亿</td><td>" +
              min_scale +
              "</td></tr><tr><td>基金规模最高" +
              data.Param.max_scale +
              "亿</td><td>基金规模" +
              (fund.net_assets_scale / 100000000.0).toFixed(2) +
              "亿</td><td>" +
              max_scale +
              "</td></tr><tr><td>基金经理管理该基金不低于" +
              data.Param.min_manager_years +
              '年</td><td>基金经理:<a href="https://appunit.1234567.com.cn/fundmanager/manager.html?managerid=' +
              fund.manager.id +
              '" target="_blank">' +
              fund.manager.name +
              "</a><br/>管理该基金:" +
              (fund.manager.manage_days / 365.0).toFixed(2) +
              "年<br/>任职回报:" +
              fund.manager.manage_repay.toFixed(2) +
              "%</td><td>" +
              manager +
              "</td></tr><tr><td>近1,3,5年波动率平均值不高于" +
              data.Param.max_135_avg_stddev.toFixed(2) +
              "%</td><td>近1,3,5年波动率平均值:" +
              fund.stddev.avg_135.toFixed(2) +
              "%<br/>近1年波动率:" +
              fund.stddev.year_1.toFixed(2) +
              "%<br/>近3年波动率:" +
              fund.stddev.year_3.toFixed(2) +
              "%<br/>近5年波动率:" +
              fund.stddev.year_5.toFixed(2) +
              "%</td><td>" +
              stddev_avg135 +
              "</td></tr><tr><td>近1,3,5年夏普比率平均值不低于" +
              data.Param.min_135_avg_sharp.toFixed(2) +
              "%</td><td>近1,3,5年夏普比率平均值:" +
              fund.sharp.avg_135.toFixed(2) +
              "%<br/>近1年夏普比率:" +
              fund.sharp.year_1.toFixed(2) +
              "%<br/>近3年夏普比率:" +
              fund.sharp.year_3.toFixed(2) +
              "%<br/>近5年夏普比率:" +
              fund.sharp.year_5.toFixed(2) +
              "%</td><td>" +
              sharp_avg135 +
              "</td></tr><tr><td>近1,3,5年最大回撤率平均值不高于" +
              data.Param.max_135_avg_stddev.toFixed(2) +
              "%</td><td>近1,3,5年最大回撤率平均值:" +
              fund.max_retracement.avg_135.toFixed(2) +
              "%<br/>近1年最大回撤率:" +
              fund.max_retracement.year_1.toFixed(2) +
              "%<br/>近3年最大回撤率:" +
              fund.max_retracement.year_3.toFixed(2) +
              "%<br/>近5年最大回撤率:" +
              fund.max_retracement.year_5.toFixed(2) +
              "%</td><td>" +
              maxretr_avg135 +
              "</td></tr></tbody></table>" +
              "</div>"
          );
          if (data.StockCheckResults) {
            var stockCheckResult = data.StockCheckResults[fund.code];
            $(`#${fund.code}`).append(
              '<br/><h5 class="center">持仓股票检测结果</h5>'
            );
            $.each(stockCheckResult.check_results, function (i, result) {
              var cm = stockCheckResult.names[i].split("-")[1].split(".");
              var index = i + 1;
              $(`#${fund.code}`).append(
                '<div id="checker_result_' +
                  i +
                  '"><div class="row"><div class="divider"></div><div class="col s12 m12 l6">' +
                  index +
                  '. <a target="_blank" href="http://quote.eastmoney.com/' +
                  cm[1] +
                  cm[0] +
                  '.html">' +
                  stockCheckResult.names[i] +
                  "</a> | 持仓占比:" +
                  fund.stocks[i].hold_ratio +
                  "%<br/>所属行业:" +
                  fund.stocks[i].industry +
                  " | 最新调仓:" +
                  fund.stocks[i].adjust_ratio +
                  "%" +
                  "<br/>当前检测财报数据来源:" +
                  stockCheckResult.fina_report_names[i] +
                  "<br/>最新财报预约发布日期:" +
                  stockCheckResult.fina_appoint_publish_dates[i] +
                  "</div>" +
                  '<table class="centered striped">' +
                  '<thead><tr><th width="30%">指标</th><th width="40%">描述</th><th width="30%">结果</th></tr></thead>' +
                  "<tbody></tbody>" +
                  "</table>" +
                  "</div>"
              );
              $.each(result, function (k, v) {
                okdesc = "❌";
                if (v.ok == "true") {
                  okdesc = "✅";
                }
                $(`#${fund.code} #checker_result_${i} tbody`).append(
                  "<tr><td>" +
                    k +
                    "</td><td>" +
                    v.desc +
                    "</td><td>" +
                    okdesc +
                    "</td></tr>"
                );
              });
            });
          }
        });
        $("html, body").animate({ scrollTop: 0 }, 0);
        $("#load_modal").modal("close");
      },
    });
  });
});
