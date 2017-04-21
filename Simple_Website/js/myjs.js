$(document).ready(
    function() {
        var picnum = Math.round(Math.random() * 14) + 1;
        var picpath = "img/Home_Page_Pics/Pictures/";
        var realpath = picpath + picnum + ".jpg"
        console.log(realpath);
        $("#photoimg").attr("src", realpath);
        $("#changephoto").click(function() {
            var picnum = Math.round(Math.random() * 14) + 1;
            var picpath = "img/Home_Page_Pics/Pictures/";
            var realpath = picpath + picnum + ".jpg"
            console.log(realpath);
            $("#photoimg").attr("src", realpath);
        });
    }
);