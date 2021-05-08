$(document).ready(function() {
    $(".thumbnail").hover(function(e) {
        e.preventDefault();
        const self = this;
        $(".active").removeClass("active");
        $(self).addClass("active");
        $(".product-img").attr("src", $(self).attr("src"));
    });

    $(".upper__arrow").click(() => {
        console.log("done");
        $(".upper__arrow").scrollTop(180);
    });

    $(".lower__arrow").click((e) => {
        e.preventDefault();
        $(".lower__arrow").scrollDown(180);
    });
});