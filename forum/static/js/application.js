$(document).ready(function() {
	"use strict";

/******************** TYPED ********************/
$(function() {
        $(".element").typed({
            strings: ["Échangez", "Rencontrez", "Recrutez"],
            typeSpeed: 50,
	    backSpeed: 100,
            backDelay: 1000,
        });
});

/******************** NAVBAR ********************/
var animationProp = $('.navbar-nemo'); //Navbar wraper

if ( matchMedia( 'only screen and (min-width: 768px)' ).matches && animationProp.hasClass('navbar-transparent') ) {
   var scrollPos = $(this).scrollTop(),
       animationEndPos = 150, //At the point background add
       logo = animationProp.find('.navbar-brand img');

   //if visitor refresh on the middle of the document
   if(scrollPos > animationEndPos) {
      animationProp.removeClass('navbar-transparent');
      logo.attr('src', 'images/logo-alt.png');
   }

   //toggle existing class
   $(document).scroll(function() {
      scrollPos = $(this).scrollTop();

      if( scrollPos > animationEndPos ) {
         animationProp.removeClass('navbar-transparent');

         //change logo into black
         logo.attr('src', 'images/logo-alt.png');
      } else {
         animationProp.addClass('navbar-transparent');

         //change logo into base
         logo.attr('src', 'images/logo.png');

      }
   });
}

/******************** BACKGROUND VIDEO ********************/
var vidContainer1 = document.querySelector(".video-player");
var vidContainer2 = document.querySelector(".the-video-2");

if ( vidContainer1 != null ) {
   var vid = vidContainer1.querySelector("video");
   var pauseButton = vidContainer1.querySelector("button");

  vid.addEventListener('ended', function() {
     // only functional if "loop" is removed
     vid.pause();
     // to capture IE10
     // vidFade();
  });

  pauseButton.addEventListener("click", function() {
     if (vid.paused) {
        vid.play();
        $(pauseButton).animate({'bottom': '50px', 'opacity': '0.5'});
        $(pauseButton).find('.play').removeClass('active');
        $(pauseButton).find('.pause').addClass('active');

     } else {
        vid.pause();
        $(pauseButton).animate({'bottom': '50%', 'opacity': '1'});
        $(pauseButton).find('.pause').removeClass('active');
        $(pauseButton).find('.play').addClass('active');
     }
  });
}

if( vidContainer2 != null ) {
  var vid = vidContainer2.querySelector("video");
  var pauseButton = vidContainer2.querySelector("button");

  vid.addEventListener('ended', function() {
     // only functional if "loop" is removed
     vid.pause();
     // to capture IE10
     // vidFade();
  });

  pauseButton.addEventListener("click", function() {
     if (vid.paused) {
        vid.play();
        $(vidContainer2).addClass('playing');
        $(pauseButton).find('.play').removeClass('active');
        $(pauseButton).find('.pause').addClass('active');

     } else {
        vid.pause();
        $(vidContainer2).removeClass('playing');
        $(pauseButton).animate({'bottom': '50%', 'opacity': '1'});
        $(pauseButton).find('.pause').removeClass('active');
        $(pauseButton).find('.play').addClass('active');
     }
  });
}

/******************** NAVBAR APPEAR ON SCROLL ********************/
if( animationProp.hasClass('appear-onscroll') ) {
   $(document).scroll(function() {
      var scrollPos = $(this).scrollTop();

      if( scrollPos > 150 ) {
         animationProp.removeClass('appear-onscroll');
      } else {
         animationProp.addClass('appear-onscroll');
      }
   });
}

/******************** ONE PAGE NAVIGATION ********************/
$('.navbar-nav').onePageNav({
   currentClass: 'active',
   scrollOffset: 74
});

/******************** NAVBAR COLLAPSE ON CLICK ********************/
/*$('.navbar-nav').on('click', 'a', function(event) {
   $('.navbar-collapse').collapse('hide');
});*/

// Function for email address validation
function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

/******************** CONTACT FORM ********************/
$('#contact-form').on('submit', function(e) {
    e.preventDefault();
    var error_msg = $(this).find('.error-msg');
    var success_msg = $(this).find('.success-msg');
    var data = {
       nom_complet: $(this).find('input[name="nom_complet"]').val(),
       nom: $(this).find('input[name="nom"]').val(),
       tel: $(this).find('input[name="tel"]').val(),
       email: $(this).find('input[name="email"]').val(),
       captcha: grecaptcha.getResponse()
    }

    if (validateEmail(data.email) && data.nom && data.tel && data.nom_complet && data.captcha) {
      $.ajax({
             type: "GET",
             url: $(this).attr('action'),
             data: data,
             success: function() {
                $("#send_mail").prop('disabled', true);
                success_msg.fadeIn(500);
                error_msg.fadeOut(500);
            },
            error: function() {
                $("#send_mail").prop('enabled', true);
                error_msg.fadeIn(500);
                alert('Veuillez cocher la case \'Je ne suis pas un robot\'');
                success_msg.fadeOut(500);
            }
      });
    } else {
        $("#send_mail").prop('enabled', true);
        error_msg.fadeIn(500);
        success_msg.fadeOut(500);
    }

return false;
});

});
