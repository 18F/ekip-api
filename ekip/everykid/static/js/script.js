$(function () {
  'use strict';

  $('.lets-go, .educator-begin, .lets-get-going, .about-more').click(function(e) {

    e.preventDefault();

    $('html, body').animate({
        scrollTop: $(".content-inner").offset().top
     }, 1000);

    $(this).addClass('active');

    $('.animate-line').fadeIn(1200);

  });

  // toggle agency descriptions
  $('#about .participating li').click(function() {

    $(this).find('.description').fadeToggle();

    $(this).toggleClass('open').toggleClass('closed');

    $('.closed .expand').html('click to expand');
    $('.open .expand').html('click to collapse');

  });

  $('#about .participating li h4').hover(function() {

    $(this).next().fadeIn();

  }, function () {

    $(this).next().fadeOut();

  })

  // scroll down to pass/field trip sites
  if($('#plan-your-trip .sites').length) {

    // don't scroll if tablet size or less
    if($(window).width() > 1024) {
      $('html, body').animate({
        scrollTop: $(".sites-container").offset().top
     }, 1200);
    }

  }

  // educator form (back to edit)
  $('#educators .back').click(function() {

    history.go(-1);

  });

}());
