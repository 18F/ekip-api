$(function () {
  'use strict';

  $('.lets-go, .educator-begin, .get-started').click(function(e) {

    e.preventDefault();

    $('html, body').animate({
        scrollTop: $(".content-inner").offset().top
     }, 1000);
  });

}());
