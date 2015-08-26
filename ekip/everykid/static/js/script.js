$(function () {
  'use strict';

  $('.lets-go, .educator-begin, .lets-get-going, .about-more').click(function(e) {

    e.preventDefault();

    $('html, body').animate({
        scrollTop: $(".content-inner").offset().top
     }, 1000);

    $('.animate-line').fadeIn(1200);
  });

  $('#about .participating li').click(function() {

    $(this).find('.description').fadeToggle();
  });

  if($('#plan-your-trip .sites').length) {

    $('html, body').animate({
        scrollTop: $(".content-inner-block").offset().top
     }, 1200);
  }

  $('#educators .back').click(function() {
    history.go(-1);
  });

}());
