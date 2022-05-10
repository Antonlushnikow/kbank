$(document).ready(function(){
    $('.read-notification').click(function(e){
        e.preventDefault();
        const URL = $(this).attr("data-href");  // API URL
        const objectId = $(this).attr("data-id");  // Notification ID
        markAsRead = $(this)[0];
        notification = $(`.notification-${objectId}`)[0];  // Notification Body

        $.ajax({
            url: URL,
            method: "GET",
            data: {},
            success: function(data){
                if (data.is_read) {
                    markAsRead.innerText = "Пометить как непрочитанное";
                    notification.classList.remove('fw-bold');
                } else {
                    markAsRead.innerText = "Пометить как прочитанное";
                    notification.classList.add('fw-bold');
                }

            },
            error: function(error){
                console.log(error)
            }
        });
    });
});