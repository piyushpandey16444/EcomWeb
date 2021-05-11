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
        const currentPosition = $(sliderComponent).scrollTop();
        $(sliderComponent).scrollTop(currentPosition + 200);
    });

    upperBtn.click(function(e) {
        e.preventDefault();
        const currentPosition = $(sliderComponent).scrollTop();
        $(sliderComponent).scrollTop(currentPosition - 200);
    });
});

scroll;