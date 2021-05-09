$(document).ready(() => {
    const showPassword1Toggle = $(".icon-one");
    const showPassword2Toggle = $(".icon-two");
    const getPassword1Field = $(".ap_password1");

    showPassword1Toggle.click((e) => handleShow1Toggle());
    showPassword2Toggle.click((e) => handleShow2Toggle());
});

const handleShow1Toggle = (e) => {
    if ($(".icon-one").hasClass("fa-eye")) {
        $(".icon-one").removeClass("fa-eye");
        $(".icon-one").addClass("fa-eye-slash");
        $(".ap_password1").attr("type", "text");
    } else if ($(".icon-one").hasClass("fa-eye-slash")) {
        $(".icon-one").removeClass("fa-eye-slash");
        $(".icon-one").addClass("fa-eye");
        $(".ap_password1").attr("type", "password");
    }
};

const handleShow2Toggle = (e) => {
    if ($(".icon-two").hasClass("fa-eye")) {
        $(".icon-two").removeClass("fa-eye");
        $(".icon-two").addClass("fa-eye-slash");
        $(".ap_password2").attr("type", "text");
    } else if ($(".icon-two").hasClass("fa-eye-slash")) {
        $(".icon-two").removeClass("fa-eye-slash");
        $(".icon-two").addClass("fa-eye");
        $(".ap_password2").attr("type", "password");
    }
};