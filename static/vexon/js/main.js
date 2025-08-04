(function ($) {
    $(document).ready(function () {
        ////////////////////////////////////////////////////
        // 03. Search Js
        $(".search-open-btn").on("click", function () {
            $(".search__popup").addClass("search-opened");
        });

        $(".search-close-btn").on("click", function () {
            $(".search__popup").removeClass("search-opened");
        });

        {
            function animateElements() {
                $(".progressbar").each(function () {
                    var elementPos = $(this).offset().top;
                    var topOfWindow = $(window).scrollTop();
                    var percent = $(this).find(".circle").attr("data-percent");
                    var percentage = parseInt(percent, 10) / parseInt(100, 10);
                    var animate = $(this).data("animate");
                    if (elementPos < topOfWindow + $(window).height() - 10 && !animate) {
                        $(this).data("animate", true);
                        $(this)
                            .find(".circle")
                            .circleProgress({
                                startAngle: -Math.PI / 2,
                                value: percent / 100,
                                size: 150,
                                thickness: 10,
                                emptyFill: "#E7E6F1",
                                fill: {
                                    color: "#0A0571",
                                },
                            })
                            .on("circle-animation-progress", function (event, progress, stepValue) {
                                $(this)
                                    .find("div")
                                    .text((stepValue * 100).toFixed() + "%");
                            })
                            .stop();
                    }
                });
            }

            // Show animated elements
            animateElements();
            $(window).scroll(animateElements);
        }
        // sticky header active
        if ($("#header").length > 0) {
            $(window).on("scroll", function (event) {
                var scroll = $(window).scrollTop();
                if (scroll < 1) {
                    $("#header").removeClass("sticky");
                } else {
                    $("#header").addClass("sticky");
                }
            });
        }

        //Aos animation active
        AOS.init({
            offset: 0,
            duration: 400,
            easing: "ease-in-out",
            anchorPlacement: "top-bottom",
            disable: "mobile",
            once: false,
        });

        //Video poppup
        if ($(".play-btn").length > 0) {
            $(".play-btn").magnificPopup({
                type: "iframe",
            });
        }

        // page-progress
        var progressPath = document.querySelector(".progress-wrap path");
        var pathLength = progressPath.getTotalLength();
        progressPath.style.transition = progressPath.style.WebkitTransition = "none";
        progressPath.style.strokeDasharray = pathLength + " " + pathLength;
        progressPath.style.strokeDashoffset = pathLength;
        progressPath.getBoundingClientRect();
        progressPath.style.transition = progressPath.style.WebkitTransition = "stroke-dashoffset 10ms linear";
        var updateProgress = function () {
            var scroll = $(window).scrollTop();
            var height = $(document).height() - $(window).height();
            var progress = pathLength - (scroll * pathLength) / height;
            progressPath.style.strokeDashoffset = progress;
        };
        updateProgress();
        $(window).scroll(updateProgress);
        var offset = 50;
        var duration = 550;
        jQuery(window).on("scroll", function () {
            if (jQuery(this).scrollTop() > offset) {
                jQuery(".progress-wrap").addClass("active-progress");
            } else {
                jQuery(".progress-wrap").removeClass("active-progress");
            }
        });
        jQuery(".progress-wrap").on("click", function (event) {
            event.preventDefault();
            jQuery("html, body").animate({ scrollTop: 0 }, duration);
            return false;
        });

        //product colors
        const colors = $(".accordion1 .accordion-item");
        colors.on("click", function () {
            $(".accordion1 .accordion-item").removeClass("active");
            $(this).addClass("active");
        });

        //tes1 active
        const tes1 = $(".controls li");
        tes1.on("click", function () {
            $(".controls li").removeClass("active");
            $(this).addClass("active");
        });

        $("#ce-toggle1").click(function (event) {
            $(".plan-toggle-wrap1").toggleClass("active");
        });

        $("#ce-toggle1").change(function () {
            if ($(this).is(":checked")) {
                $(".tab-content #yearly1").hide();
                $(".tab-content #monthly1").show();
            } else {
                $(".tab-content #yearly1").show();
                $(".tab-content #monthly1").hide();
            }
        });

        //hero 1 slider
        $(".sidebar-slider-widget").slick({
            margin: "30",
            slidesToShow: 1,
            arrows: false,
            centerMode: true,
            dots: true,
            loop: true,
            centerMode: false,
            draggable: true,
            autoplay: true,
            autoplaySpeed: 4000,
            fade: true,
            fadeSpeed: 1000,
            responsive: [
                {
                    breakpoint: 769,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
                {
                    breakpoint: 480,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
            ],
        });

        // Blog 2 slider
        $(".blog2-meets-slider").slick({
            margin: "30",
            slidesToShow: 5,
            arrows: true,
            prevArrow: $(".blog2-slider-prev"),
            nextArrow: $(".blog2-slider-next"),
            centerMode: true,
            dots: false,
            loop: true,
            centerMode: false,
            draggable: true,
            autoplay: true,
            autoplaySpeed: 4000,
            fade: false,
            fadeSpeed: 1000,
            responsive: [
                {
                    breakpoint: 769,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
                {
                    breakpoint: 480,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
            ],
        });

        // Blog 4 slider
        $(".blog4-slider").slick({
            margin: "30",
            slidesToShow: 1,
            arrows: true,
            prevArrow: $(".blog4-slider-prev"),
            nextArrow: $(".blog4-slider-next"),
            centerMode: true,
            dots: false,
            loop: true,
            centerMode: false,
            draggable: true,
            autoplay: true,
            autoplaySpeed: 4000,
            fade: false,
            fadeSpeed: 1000,
            responsive: [
                {
                    breakpoint: 769,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
                {
                    breakpoint: 480,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 1,
                    },
                },
            ],
        });
        // Blog 5 slider
        $(".blog5-slider").slick({
            margin: "30",
            slidesToShow: 4,
            arrows: true,
            prevArrow: $(".blog5-slider-prev"),
            nextArrow: $(".blog5-slider-next"),
            centerMode: true,
            dots: false,
            loop: true,
            centerMode: false,
            draggable: true,
            autoplay: true,
            autoplaySpeed: 4000,
            fade: false,
            fadeSpeed: 1000,
            responsive: [
                {
                    breakpoint: 769,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "40px",
                        slidesToShow: 2,
                    },
                },
                {
                    breakpoint: 480,
                    settings: {
                        arrows: false,
                        centerMode: false,
                        centerPadding: "0px",
                        slidesToShow: 1,
                    },
                },
            ],
        });
    });

    /* Text Effect Animation */
    if ($(".text-anime-style-1").length) {
        let staggerAmount = 0.05,
            translateXValue = 0,
            delayValue = 0.5,
            animatedTextElements = document.querySelectorAll(".text-anime-style-1");

        animatedTextElements.forEach((element) => {
            let animationSplitText = new SplitText(element, { type: "chars, words" });
            gsap.from(animationSplitText.words, {
                duration: 1,
                delay: delayValue,
                x: 20,
                autoAlpha: 0,
                stagger: staggerAmount,
                scrollTrigger: { trigger: element, start: "top 85%" },
            });
        });
    }

    if ($(".text-anime-style-2").length) {
        let staggerAmount = 0.05,
            translateXValue = 20,
            delayValue = 0.5,
            easeType = "power2.out",
            animatedTextElements = document.querySelectorAll(".text-anime-style-2");

        animatedTextElements.forEach((element) => {
            let animationSplitText = new SplitText(element, { type: "chars, words" });
            gsap.from(animationSplitText.chars, {
                duration: 1,
                delay: delayValue,
                x: translateXValue,
                autoAlpha: 0,
                stagger: staggerAmount,
                ease: easeType,
                scrollTrigger: { trigger: element, start: "top 85%" },
            });
        });
    }

    if ($(".text-anime-style-3").length) {
        let animatedTextElements = document.querySelectorAll(".text-anime-style-3");

        animatedTextElements.forEach((element) => {
            //Reset if needed
            if (element.animation) {
                element.animation.progress(1).kill();
                element.split.revert();
            }

            element.split = new SplitText(element, {
                type: "lines,words,chars",
                linesClass: "split-line",
            });
            gsap.set(element, { perspective: 400 });

            gsap.set(element.split.chars, {
                opacity: 0,
                x: "50",
            });

            element.animation = gsap.to(element.split.chars, {
                scrollTrigger: { trigger: element, start: "top 95%" },
                x: "0",
                y: "0",
                rotateX: "0",
                opacity: 1,
                duration: 1,
                ease: Back.easeOut,
                stagger: 0.02,
            });
        });
    }

    //preloader
    $(window).on("load", function (event) {
        setTimeout(function () {
            $(".sec-preloader").fadeToggle();
        }, 500);
    });

    $("select").niceSelect();
})(jQuery);
