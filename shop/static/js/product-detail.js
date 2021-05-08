$(document).ready(function() {
    $(".thumbnail").hover(function(e) {
        e.preventDefault();
        const self = this;
        $(".active").removeClass("active");
        $(self).addClass("active");
        $(".product-img").attr("src", $(self).attr("src"));
    });
});