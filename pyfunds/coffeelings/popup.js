//DATE VARIABLES//
var d, dName, dMonth, dDay, dYear, dTail; //current date
var tMonth, tDay, tYear; //temporary date (hover or selected)
var lMonth, lDay; //locked date

//MISC VARIABLES//
var mood, overMonth, lastMood; //mood and calendar misc
var locked, locking, editing; //state variables

//STATIC//
var defaultNote = ". . .";
var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
var colors = { default: 'var(--lightvanilla)', amazing: 'var(--cinnamon)', ok: 'var(--light)', tired: 'var(--city)', sad: 'var(--dark)', stressed: 'var(--italian)'};
var moodResults = Object.keys(colors); //default, amazing, ...
var colorResults = Object.values(colors); //var(--lightvanilla), var(--cinnamon), ...
var monthArrays = generateYearList(2020);
var years = {};

//EVENT HANDLERS w jquery//

$(document).ready(function() {
  //mouseover trigger - indicates flavors!!
  $(".opt").mouseover(function(e) {
    $('#tail').show();
    mood = e.currentTarget.id;
    $('#tail_name').html(mood);
    crossFade(lastMood, mood);
    lastMood = mood;
  });

  $("div#mood_options").mouseleave(function() {
    $('#tail').hide();
    crossFade(lastMood, "default");
    lastMood = "default";
  });

  //click trigger - goes to calendar screen
  $(".opt").click(function() {
    setCell(dMonth, dDay - 1, colors[mood]);
    saveCell(dMonth, dDay - 1, colors[mood]);
    saveNote(dMonth, dDay - 1, $("#input").val());
    tYear = dYear;
    goToCalendar(tYear);
  });

  //trigger on year change
  $('.years').on('change', function(e) {
    tYear = this.value;
    goToCalendar(tYear);
  });

  $("#goToPick").click(function() {
    //DATA RESET: chrome.storage.sync.clear();
    //DATA RESET: chrome.storage.sync.set({'firstRun': 0});
    goToPick();
  });

  $("#goToInfo").click(function() {
    $("#info").show();
  });

  $("div.day").mouseover(function(e) {
    var target = e.currentTarget;
    indicateCell(target);
    $("#note").show();
  });

  $("div.day").hover(function(e){
    $(document).keydown(function(event){
      var key = (event.keyCode ? event.keyCode : event.which);
      if(key == '76' && !editing) setLock(tMonth, tDay);
    });
  });

  $("div.day").mousedown(function(e) {
    if (event.shiftKey) eraseColor(e); //any click & shift
    else {
      if (e.which === 1) switchColor(e); //left mouse click
      else if (e.which === 3 && !editing && !locking) setLock(tMonth, tDay); //right mouse click
    }
  });

  $("div.day").mouseleave(function(e) {
    $("#" + overMonth + "Name").css("color", 'var(--italian)');
    $('#tail').hide();
    if(!locked) $("#note").hide();
  });

  $("#infooverlay").click(function(e) {
    $("#info").hide();
  });

  $("#goEditNote").click(function() {
    editing = true;
    var text = years[tYear][lMonth][lDay][1];
    $("#goEditNote").hide();
    $("#noteContent").hide();
    $("#goSaveNote").show().css("margin-top", "-30px");
    $("#noteEditor").val(text).show().scrollTop(0);
    $("hr#line").css("margin-top", "2px");
  });

  $("#goSaveNote").click(function() {
    editing = false;
    var text = $("#noteEditor").val();
    saveNote(lMonth, lDay, text);
    $("#noteEditor").hide();
    if(text=="" || text ==null) $("#noteContent").html(defaultNote).show().scrollTop(0).css("opacity", "0.8");
    else $("#noteContent").html(text).show().scrollTop(0).css("opacity", "1");
    $("#goEditNote").show();
    $("#goSaveNote").hide();
    $("hr#line").css("margin-top", "-13px");
  });

  $("#goTrashNote").click(function(){
    killNote(lMonth, lDay);
  });

  $("#convertText").click(function(){
    saveDataToFile();
  });
});

//DOWNLOAD FUNCTIONALITY//

function saveDataToFile() {
  var blob = new Blob([getString()], {type: "text/plain"});
  var url = URL.createObjectURL(blob);
  var param = {
    url: url,
    filename: "my_coffeelings_" + tYear.toString() + ".txt"
  };
  chrome.downloads.download(param);
}

function getString(){
  var thisString = "";
  for (i = 0; i < years[tYear].length; i++) {
    for (j = 0; j < years[tYear][i].length; j++) {
      if (years[tYear][i][j][0] != null) {
        thisString += getDayString(years[tYear][i][j][0], i, j) + "\n";
      }
    }
  }
  return thisString;
}

function getDayString(color, month, day){
  var text = years[tYear][month][day][1];
  var mood = .[colorResults.indexOf(color)];
  mood = (mood==undefined || mood=="default") ? "" : "/ " + mood;
  var dayString = months[month] + " " + (day+1) + " " + mood;
  if(text!="" && text!=null) dayString += ("\n" + text);
  return dayString += "\n";
}

//ANIMATION//

function crossFade(x, y) {
  $("div#coffee_options #" + x).css('z-index', 3).stop(true, true, true).fadeOut(140);
  $("div#coffee_options #" + y).css('z-index', 1).stop(true, true, true).show();
}

$(document).bind('mousemove', function(e) {
  $("#tail").css({
    left: e.pageX + 5,
    top: e.pageY - 20
  });
});

function setBG(val){
  chrome.storage.local.set({'radioVal': val});
  $("#bg_3").attr('src', "art/bg_"+val+".png");
}

function getBG(){
  chrome.storage.local.get(['radioVal'], function(result) {
    var radioVal = result.radioVal;
    if(radioVal != null) $("#bg_3").attr('src', "art/bg_"+radioVal+".png");
    else $("#bg_3").attr('src', "art/bg_3.png");
  });
}

//NAVIGATION//

function isLeapYear(year) {
  return years[year][1].length === 29;
}

function goToCalendar() {
  if ($('#pick').is(":visible")) {
    setBG($('input:radio[name=reason]:checked').val());
    $('#pick').fadeOut(500);
    $('#calendar').delay(500).fadeIn(800);
    $("#tail").hide();
    $('#tail_name').hide();
    $('#tail_date').show().html('');
  } else {
    getBG();
    $('#calendar').fadeIn(800);
  }

  generateCalendar(years[tYear]);
  $('#cal_year').html(tYear);
  if(!isLeapYear(tYear)) $("#leapDay").attr('id', 'notADay');
  $("#tail_img").attr('src', "art/highlight3.png");
}

function goToPick() {
  getDate();
  if ($('#calendar').is(":visible")) {
    $('#calendar').fadeOut(500);
    $('#pick').delay(500).fadeIn(800);
    $("#tail").hide();
    $('#tail_date').hide();
    $('#tail_name').show().html('');
  } else $('#pick').fadeIn(800);
  $('#input').val(years[tYear][dMonth][dDay-1][1]);
  $("#tail_img").attr('src', "art/highlight.png");
}

//GENERAL//

function tempDName(month, day) {
  return "#" + months[month] + " div:nth-child(" + day + ")";
}

function generateDate() {
  d = new Date();
  dMonth = d.getMonth();
  dDay = d.getDate();
  dYear = d.getFullYear();
  dTail = months[dMonth].substring(0, 1) + dDay;
}

//NOTES//

function indicateCell(target) {
  overMonth = target.parentElement.id;
  $("#" + overMonth + "Name").css("color", 'var(--vanilla)');
  $('#tail').show();

  tMonth = months.indexOf(overMonth);
  tDay = Array.prototype.indexOf.call(target.parentElement.children, target);

  var day = tDay + 1;
  var monthDay = "<b>" + overMonth.substring(0, 1) + "</b>/<small>" + day;
  $('#tail_date').html(monthDay);
  if (!locked) setNote(years[tYear][tMonth][tDay][0], tMonth, tDay);
}

function setNote(color, month, day){
  var starsText = getMoodStars(color);
  var text = years[tYear][month][day][1];
  var mood = moodResults[colorResults.indexOf(color)];
  mood = (mood==undefined || mood=="default") ? "" : "/ " + mood;
  if(text=="" || text==null) $("#noteContent").html(defaultNote).css("opacity", "0.8");
  else $("#noteContent").html(text).css("opacity", "1");
  $("#noteDate").html("<small><b>" + months[month] + "</b> " + (day+1) + " " + mood + "</small><br>" + starsText);
}

function setLock(month, day) {
  $("div#lock").toggle();
  locking = true; //won't allow weird locking glitches where L is held too long
  setTimeout(function() { locking = false; }, 0.5 * 1000);
  locked = !locked;

  if (locked) {
    //assuming the player can't click in two spots, it'll save to whatever lMonth and lDay are
    lMonth = month;
    lDay = day;
  }
}

function saveNote(month, day, note) {
  years[tYear][month][day][1] = note;
  chrome.storage.local.set({
    'yearsSaved': years
  });
}

function killNote(month, day){
  years[tYear][month][day][1] = "";
  setNote("default", month, day);
  $(tempDName(month, day+1)).css("background-color", colorResults[0]);
  saveCell(month, day, null);
  chrome.storage.local.set({
    'yearsSaved': years
  });
}

//STARS//

function getMoodStars(color) {
  var stars = "";
  var numFilledStars = colorResults.indexOf(color);
  for (i = numFilledStars; i <= 5; i++) stars += "&#9733;";
  for (i = 1; i < numFilledStars; i++) stars += "&#9734;";
  stars += "</small>";
  if (numFilledStars == -1 || numFilledStars == 0) stars = "&#10035;";
  return stars;
}

//CELLS//

function markTodaysCell(month, day) { //marks todays cell w date & disables next cells
  var tempDay = day > 9 ? "" + day : "0" + day; //keeps numbering formats consistent
  $(tempDName(month, day)).append("<span id='dayNum'>" + tempDay + "</span>");
  for (i = month + 1; i < 12; i++) //disables next month's cells
    for (j = 0; j <= 31; j++) killCell(i, j);
}

function killCell(i, j) {
  var n = tempDName(i, j);
  if (!$(n).is("#notADay")) { //else it changes the notADays too
    $(n).css({
      "pointer-events": "none",
      "background-color": "var(--lightervanilla)"
    });
  }
}

function saveCell(month, day, color) {
  years[tYear][month][day][0] = color;
  chrome.storage.local.set({
    'yearsSaved': years
  });
}

function setCell(month, day, color) {
  day += 1;
  $(tempDName(month, day)).css("background-color", color);
}

function switchColor(e) {
  var target = e.currentTarget;
  var currentColor = target.style.backgroundColor;
  if (currentColor == "") currentColor = "var(--lightvanilla)";
  var currentColorIndex = (colorResults.indexOf(currentColor) + 1) % colorResults.length;
  tempColor = colorResults[currentColorIndex];
  target.style.backgroundColor = tempColor;
  saveCell(tMonth, tDay, tempColor);
  if(!locked || (tMonth == lMonth && tDay == lDay)) setNote(years[tYear][tMonth][tDay][0], tMonth, tDay);
}

function eraseColor(e) {
  var target = e.currentTarget;
  target.style.backgroundColor = colorResults[0];
  var tempColor = null;
  saveCell(tMonth, tDay, tempColor);
}

//START//

function getDate() {
  $('#month').html(months[dMonth]);
  $('#day').html(dDay);
  $('#years').empty();
  //generate all year options (if multiple)
  for(let key in years) {
    if(key===dYear.toString()) $('#years').append("<option value='" + key + "' selected>" + key + "</option>");
    else $('#years').append("<option value='" + key + "'>" + key + "</option>");
  }
}

document.addEventListener('DOMContentLoaded', start);
document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
}, false); //prevents right click from opening menu

function start() {
  generateDate();
  lastMood = "default";
  locked = false;

  //this can stay storage.sync... why not
  chrome.storage.sync.get(['firstRun'], function(result) {
    if (result.firstRun == 3) getSaved();
    else if (result.firstRun == 1 || result.firstRun == 2) switchToLocal();
    else firstRun();
  });
}

function setScreens(month, day) { //check if today's cell is filled already & if so, skips the first part
  tYear = dYear;
  var todayVal = years[tYear][month][day - 1][0];
  if (todayVal != null && todayVal != undefined && todayVal != "var(--lightvanilla)" && todayVal != "undefined") goToCalendar(tYear);
  else goToPick();
}

//CONVERTING DATA FROM HARDCODED 2020...//
//supporting multiple years & moving main variable status from monthArrays to years

function updateYears(result) {
  //VER 3.00 UPDATES
  years = result.yearsSaved;
  if(years === undefined) {
    console.log("reformatting your local data...");
    years = {};
    years[2020] = monthArrays;
  }
  if(!(dYear in years)) years[dYear] = generateYearList(dYear);
  
  //TESTING 3.00 UPDATES
  /*console.log(years[2020]);
  chrome.storage.local.set({'monthArraysSaved': years[2020]});
  chrome.storage.local.get(['monthArraysSaved'], function(result) {
    console.log(result.monthArraysSaved);
  });*/
}

function getSaved() {
  chrome.storage.local.get(['monthArraysSaved', 'yearsSaved'], function(result) {
    monthArrays = result.monthArraysSaved;
    updateYears(result);
    setScreens(dMonth, dDay);
    markTodaysCell(dMonth, dDay);
  });
}

function switchToLocal() {
  //VER 2.00 UPDATES
  //gets montharrays from storage.sync then starts saving as storage.local
  chrome.storage.sync.get(['monthArraysSaved', 'yearsSaved'], function(result) {
    monthArrays = result.monthArraysSaved;
    chrome.storage.local.set({'monthArraysSaved': monthArrays});
    updateYears(result);
    setScreens(dMonth, dDay);
    markTodaysCell(dMonth, dDay);
  });
  chrome.storage.sync.set({'firstRun': 3});
}

function generateCalendar(year) {
  for (i = 0; i < year.length; i++) {
    for (j = 0; j < year[i].length; j++) {
      if (year[i][j][0] != null) setCell(i, j, year[i][j][0]);
      else setCell(i, j, colorResults[0]);
    }
  }
}

function firstRun() {
  years[dYear] = generateYearList(dYear);
  monthArrays = generateYearList(2020); //here just in case any if statements try to see if it's there
  chrome.storage.local.set({
    'monthArraysSaved': monthArrays,
    'yearsSaved': years
  });
  chrome.storage.sync.set({'firstRun': 3});
  goToPick();
}

//GENERATES BASE DATA FOR EACH YEAR//
/*nested structure:
- 1 dictionary for all years = {2020: [], 2021: []}
- 1 array per year = []
- 1 array per month = []
- 1 array per day that holds 2 = [mood, note]*/

function generateYearList(year) {
  let yearArray = new Array(12);
  for(let i = 1; i <= 12; i++) {
    yearArray[i-1] = generateMonthList(year, i);
  }
  return yearArray;
}

function generateMonthList(year, month) {
  let days = new Date(year, month, 0).getDate();
  let monthArray = [1, 2, 3];
  for(let i = 0; i < days; i++) {
    monthArray[i] = new Array(2);
  }
  return monthArray;
}
