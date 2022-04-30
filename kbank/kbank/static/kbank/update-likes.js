$(document).ready(function(){
    $('.like-btn').click(function(e){
        e.preventDefault();
        const likeURL = $(this).attr("data-href");  // API URL
        const objectId = $(this).attr("data-id");
        let likeCount = $(this).next("span");  // Total count of likes
        console.log(likeCount);
        let likeIcon = $(this).children(`.like-icon-${objectId}`);  // Font-awesome icon

        $.ajax({
            url: likeURL,
            method: "GET",
            data: {},
            success: function(data){
                // Icon change
                if (data.liked) {
                    likeIcon[0].classList.remove("fa-regular");
                    likeIcon[0].classList.add("fa-solid");
                } else {
                    likeIcon[0].classList.remove("fa-solid");
                    likeIcon[0].classList.add("fa-regular");
                }
                // Update like count from API
                likeCount[0].innerText = data.like_count;
            },
            error: function(error){
                console.log(error)
            }
        });
    });
});