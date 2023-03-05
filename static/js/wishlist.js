$(document).ready(function () {
        let isLoading = false;

        $('.favorite-form').submit(function (e) {
        e.preventDefault()
        if (!isLoading) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const url = $(".favorite-form").attr("action");
            const ann_id = $(this).attr('id');
            isLoading = true;

            $.ajax({
                type: 'POST',
                url: url,
                dataType: "json",
                mode: 'same-origin',
                headers: {
                    'X-CSRFToken': csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                data: JSON.stringify({
                    'csrfmiddlewaretoken': csrftoken,
                    'ann_id': ann_id,
                }),
                success: function (response) {
                    $('#heart-' + ann_id).addClass(response.status ? 'bi-heart-fill text-danger' : 'bi-heart')
                        .removeClass(response.status ? 'bi-heart' : 'bi-heart-fill text-danger');
                    isLoading = false;
                },
                error: function (error) {
                    console.log(error);
                },
                statusCode: {
                    403: function (error) {
                        console.log(error);
                    },
                },
            });
        }
    });
});