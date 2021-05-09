$(document).ready(function() {

    $(".thumbnail").hover(function(e) {
        e.preventDefault();
        const self = this;
        $(".active").removeClass("active");
        $(".hover__on").removeClass("hover__on");
        $(self).addClass("active");
        $(self).addClass("hover__on");
        $(".product-img").attr("src", $(self).attr("src"));
    });
});