$(document).ready(function() {
    $(".thumbnail").hover(function(e) {
        e.preventDefault();
        const self = this;
        $(".active").removeClass("active");
        $(".hover__on").removeClass("hover__on");
        $(self).addClass("active");
        $(self).addClass("hover__on");
        $(".product__img").attr("src", $(self).attr("src"));
    });

    const upperBtn = $(".upper__arrow");
    const lowerBtn = $(".lower__arrow");
    const sliderComponent = $(".slider");

    lowerBtn.click(function(e) {
        e.preventDefault();
        var y = $(sliderComponent).scrollTop(); //your current y position on the page
        $(sliderComponent).scrollTop(y + 200);
    });

    upperBtn.click(function(e) {
        e.preventDefault();
        var y = $(sliderComponent).scrollTop(); //your current y position on the page
        $(sliderComponent).scrollTop(y - 200);
    });
});

scroll;