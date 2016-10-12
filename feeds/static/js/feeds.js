$(function() {
    $(".btn-compose").click(function() {
        if ($(".compose").hasClass("composing")) {
            $(".compose").removeClass("composing");
            $(".compose").slideUp();
        }
        else {
            $(".compose").addClass("composing");
            $(".compose textarea").val("");
            $(".compose").slideDown(400, function() {
                $(".compose textarea").focus();
            });
        }
    });

    $(".btn-cancel-compose").click(function() {
        if ($(".compose").hasClass("composing")) {
            $(".compose").removeClass("composing");
        }
        $(".compose").slideUp();
    });

    $(".btn-post").click(function() {
        var last_feed = $(".stream li:first-child").attr("feed-id");
        if (last_feed == undefined) {
            last_feed = "0";
        }
        $("#compose-form input[name='last_feed']").val(last_feed);
        $.ajax({
            url: '/feeds/post/',
            data: $("#compose-form").serialize(),
            type: 'post',
            cache: false,
            success: function(data) {
                $("ul.stream").prepend(data);
                $(".compose").slideUp();
                $(".compose").removeClass("composing");

            }
        })
    })

})
