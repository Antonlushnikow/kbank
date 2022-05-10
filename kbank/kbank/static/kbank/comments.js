$(document).ready(function(){

    class CommentContext {
        constructor(obj) {
            this.element = obj[0];
            this.URL = obj.attr("data-href");  // API URL
            this.objectId = obj.attr("data-id");
            this.comment = $(`.comment-${this.objectId}`)[1];  // Comment Text
        }   

    }

    // Create CSRF-token
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

    // Delete Comment
    $('.delete-comment').click(function(e){
        e.preventDefault();
        context = new CommentContext($(this));

        $.ajax({
            url: context.URL,
            method: "DELETE",
            headers: {'X-CSRFToken': csrftoken},
            success: function(data){
                context.comment.innerText = 'Комментарий удален';
            },
            error: function(error){
                console.log(error)
            }
        });
    });

    // Show-Hide Comment
    $('.show-comment').click(function(e){
        e.preventDefault();
        context = new CommentContext($(this));

        $.ajax({
            url: context.URL,
            method: "GET",
            data: {},
            success: function(data){
                if (data.is_visible) {
                    context.comment.classList.remove('hidden-comment');
                }
                else {
                    context.comment.classList.add('hidden-comment');
                }
            },
            error: function(error){
                console.log(error)
            }
        });
    });

     // Edit Comment
    $('.edit-comment').click(function(e){
        e.preventDefault();

        context = new CommentContext($(this));

        let divNewComment = $(`.edit-input-comment-${context.objectId}`)[0];  // Edit Comment Div
        let inputNewComment = divNewComment.getElementsByClassName('form-control')[0]; // Edit Comment Input
        let bntSubmitComment = divNewComment.getElementsByClassName('btn')[0]; // Edit Comment Button Submit
        let bntCancelComment = divNewComment.getElementsByClassName('btn')[1]; // Edit Comment Button Cancel

        context.comment.hidden = true;
        divNewComment.hidden = false;

        bntSubmitComment.onclick = function(e){
            e.preventDefault();
            
            $.ajax({
                url: context.URL,
                method: "PATCH",
                headers: {'X-CSRFToken': csrftoken},
                data: {
                    'body': inputNewComment.value,
                },
                success: function(data){
                    console.log(data);
                    context.comment.innerText = data.body;
                    context.comment.hidden = false;
                    divNewComment.hidden = true;
                },
                error: function(error){
                    console.log(error);
                }
            });
        };

        bntCancelComment.onclick = function(e){
            context.comment.hidden = false;
            divNewComment.hidden = true;
        }

    });

    // Reply to Comment
    $('.reply-comment').click(function(e){
        e.preventDefault();
        context = new CommentContext($(this));
        if (context.element.classList.contains("clicked")==false) {
            context.element.classList.add("clicked");
            let once = true;
            let divComment = $(`.comment-${context.objectId}`)[0];  // Edit Comment Div
            let div = document.createElement("div");
            let form = document.getElementsByTagName("form")[0];
            div.className = 'form-outline mb-4';
            div.innerHTML = '<form method="POST">' + form.innerHTML + '<input type=hidden name="parent" value="' + context.objectId + '" id="id_parent"></form>';
            divComment.after(div);
        }
    });


});
