$(document).ready(function(){
        function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('.delete-comment').click(function(e){
        e.preventDefault();

        const URL = $(this).attr("data-href");  // API URL
        const objectId = $(this).attr("data-id");
        let comment = $(`.comment-${objectId}`)[0];  // Comment

        $.ajax({
            url: URL,
            method: "DELETE",
            headers: {'X-CSRFToken': csrftoken},
            success: function(data){
                console.log('Deleted');
                console.log(comment);

                comment.innerText = 'Удалено';
            },
            error: function(error){
                console.log(error)
            }
        });
    });
});
