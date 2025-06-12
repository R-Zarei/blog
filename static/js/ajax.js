$(document).ready(function () {

    // Send the post like and change heart button and like number
    $("#like").click(function () {
        $.ajax({
            type: 'GET',
            url: '/like/' + $('#postSlug').val() + '/' + $('#postPk').val(),
            dataType: 'json',
            success: function (response) {
                // console.log(response)
                if (response.status === "liked") {
                    $('#like').attr('class', 'fa fa-heart');
                } else {
                    $('#like').attr('class', 'fa fa-heart-o');
                }
                $('#likeNum').text(response.like_num);
            },
        });
    });

    // Send the comments and resaved that with ajax
    $('#form-submit').click(function () {
        var body = $('#body').val();
        var parentId = $('#parent_id').val();
        var csrfToken = $('#csrfToken').val();
        $.ajax({
            type: 'POST',
            url: $('#commentUrl').val(),
            data: {
                'body': body,
                'parent_id': parentId,
            },
            headers: {"X-CSRFToken": csrfToken},
            success: function (response) {
                // select user image url.
                if (response.user_img_url) {
                    var userImgUrl = response.user_img_url;
                }
                else {
                    var userImgUrl = $("#userImg").val();
                }

                // comment html code.
                var newComment = '<li style="display: table" name="' + response.id + '">' +
                    '<div class="author-thumb">' +
                    '<img src="' + userImgUrl + '" alt="profile_img"/>' +
                    '</div>' +
                    '<div class="right-content">' +
                    '<h4>' + response.user_name + '<span>' + response.date + '</span></h4>' +
                    '<p>' + response.body + '</p>' +
                    '<button onClick="is_reply(' + response.id + ')" style=" font-weight: bold ; font-size: 13px;  background: transparent; border: none; color: #f48840">Reply\n</button>' +
                    '</div>' +
                    '</li>';
                var newReply = '<li class="replied" style="display: table" name="' + parentId + '">' +
                    '<div class="author-thumb">' +
                    '        <img src="' + userImgUrl + '" alt="profile_img"/>' +
                    '    </div>' +
                    '    <div class="right-content">' +
                    '        <h4>' + response.user_name + '<span>' + response.date + '</span></h4>' +
                    '        <p>' + response.body +'</p>' +
                    '    </div>' +
                    '</li>';

                // clear comment input box after submit comment.
                $("#body").val('');
                // add comment to page.
                if (parentId) {
                    $('[name="'+parentId+'"]').last().after(newReply);
                    $('#parent_id').val('');
                }
                else {
                    var commetn = $("#comment-block li");
                    if (commetn.length > 0) {
                        commetn.last().after(newComment);
                    } else {
                        $("#comment-block").append(newComment);
                    }
                }
            },
            error: function () {
                alert('Somthing went wrong, try again.');
            }
        });
    });
});
