$(function () {
  'use strict';

  $('.lets-go, .educator-begin').click(function(e) {

    e.preventDefault();

    $('html, body').animate({
        scrollTop: $(".content-inner-block").offset().top
     }, 1000);
  });

}());
