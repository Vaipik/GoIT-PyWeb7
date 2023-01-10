$(function ($) {
    $('#login').submit(function (e) {
        e.preventDefault()
        console.log(this)
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.alert-danger').text(response.error).removeClass('d-none')
                }
            },
            error: function (response) {
                console.log('err - ', response)
        }
    })
})
})