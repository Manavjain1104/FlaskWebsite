
$(function() {

  var covidText = "Coronavirus (COVID-19) Updates";
  var covidLink = "https://www.mygov.in/covid-19";


  /* DO NOT EDIT BELOW THIS LINE */
  if($('body:not(.fsComposeMode)').length) {
    var covidBanner = "<div id='covid-banner' class='covid-banner'>" + covidText +" | " + "<a href=" + covidLink + ">Click Here To Check Status</a></div>"
    $('body').prepend(covidBanner);
  }

});

function myFunction() {
  var x = document.getElementById("covid-banner");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}