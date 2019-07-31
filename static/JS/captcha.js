function getCaptcha(url) {
    $.ajax({
            url: url,
            type: "GET",
            data: {},
            dataType:"text",
            success: function (data) {
                // language=JQuery-CSS
                data = jQuery.parseJSON(data);
                $('#id_uuid').val(data.uuid);
                $("#captcha").attr("src","data:image/png;base64,"+data.image);
            }, error: function () {
                xtalert.alertError("获取图片失败");
            }
        });
}

function checkCaptcha(url) {
    var uuid = $('#id_uuid').val();
    var code = $('#id_captcha').val();
    bool = false
    $.ajax({
            url: url,
            type: "POST",
            data: {'uuid': uuid, 'code': code},
            dataType:"text",
            async: false,
            success: function (data) {
                data = jQuery.parseJSON(data);
                if( data.status == 0 ){
                    console.log('success')
                    bool = true
                }
                else{
                    console.log('failed')
                    xtalert.alertError("验证码错误");
                    bool = false
                }
            }, error: function () {
                xtalert.alertError("验证失败");
                bool = false
            }
        });
    console.log(bool);
    return bool
}

