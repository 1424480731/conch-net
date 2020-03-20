$(window).on("load", function() {
    "use strict";


    /*==============================================
                RESPONSIVE MOBILE MENU FUNCTION
    ===============================================*/


    $(".menu-btn").on("click", function(){
      $(this).toggleClass("active");
      $(".responsive-mobile-menu").toggleClass("active");
    });

    $(".responsive-mobile-menu ul ul").parent().addClass("menu-item-has-children");
    $(".responsive-mobile-menu ul li.menu-item-has-children > a").on("click", function() {
      $(this).parent().toggleClass("active").siblings().removeClass("active");
      $(this).next("ul").slideToggle();
      $(this).parent().siblings().find("ul").slideUp();
      return false;
    });

    if($(window).width() < 480 ) {
        $(".menu-btn").on("click", function(){
            $("body").toggleClass("no-scroll");
        });
    };
    
    /*==============================================
                SINGLE POST VISIBLE FUNCTION
    ===============================================*/    

    $(".single-post .pro-info > h3").on("click", function(){
        $(this).nextAll(".hidden").slideToggle();
        $(this).toggleClass("active");
    });

    /*==============================================
                    HALF MAP POSITIONING
    ===============================================*/


    var pt_height = $(".post-info").innerHeight();
    $(".post-img").css({
        "height": pt_height
    });


    var cont_height = $(".contact-details").innerHeight();
    $("#map-container.fullwidth-home-map.add-map").css({
        "height": cont_height
    });


    /*==============================================
                      SETTING HEIGHT OF DIVS
    ===============================================*/

    var ab_height = $(".agent-info").outerHeight();
    $(".agent-img").css({
        "height": ab_height
    });

    $(".horizental-view .sale-item").each(function(){

        var it_height = $(this).find(".item-info").outerHeight();
        $(this).find(".item-img").css({
            "height": it_height
        });

    });


    var hd_height = $("header").innerHeight();
    $(".half-map").css({
        "margin-top": hd_height
    });
    $(".half-map #map-container, .half-map .svg-map").css({
        "top": hd_height
    });


    /*==============================================
                      ACCORDION FUNCITON
    ===============================================*/

    $(".toggle").each(function(){
        $(this).find('.content').hide();
        $(this).find('h2:first').addClass('active').next().slideDown(500).parent().addClass("activate");
        $('h2', this).click(function() {
            if ($(this).next().is(':hidden')) {
                $(this).parent().parent().find("h2").removeClass('active').next().slideUp(500).removeClass('animated fadeInUp').parent().removeClass("activate");
                $(this).toggleClass('active').next().slideDown(500).addClass('animated fadeInUp').parent().toggleClass("activate");
            }
        });
    });
 
   

    /*==============================================
                    SIGN IN / REGISTER 
    ===============================================*/


    $('.popup-head ul li, .register-op').on("click", function(){
        var tab_id = $(this).attr('data-tab');
        $('.popup-head ul li').removeClass('active');
        $('.popup-form').removeClass('current');
        $(this).addClass('active animated fadeIn');
        $("#"+tab_id).addClass('current animated fadeIn');
        return false;
    });

    $(".login-form").on("click", function(){
        $(".popup").addClass("active");
        $(".wrapper").addClass("overlay")
    });
    $("html").on("click", function(){
        $(".popup").removeClass("active");
        $(".wrapper").removeClass("overlay");
    });
    $(".popup, .login-form").on("click", function(e) {
        e.stopPropagation();
    });


    $(".search-btn").on("click", function(){
       window.location.href="06_Properties_Half_Grid_Map_View.html";
       return false;
    });

    $(".handle-counter .btn").on("click", function() {
        return false;
    });


    /*==============================================
                    SMOOTH SCROLLING
    ===============================================*/

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

});
