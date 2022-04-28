$(document).ready(function(){
    $('.show-comment').click(function(e){
        e.preventDefault();
        const URL = $(this).attr("data-href");  // API URL
        const objectId = $(this).attr("data-id");
        let comment = $(`.comment-${objectId}`)[0];  // Comment

        $.ajax({
            url: URL,
            method: "GET",
            data: {},
            success: function(data){
                if (data.is_visible) {
                    comment.classList.remove('hidden-comment');
                }
                else {
                    comment.classList.add('hidden-comment');
                }


            },
            error: function(error){
                console.log(error)
            }
        });
    });
});