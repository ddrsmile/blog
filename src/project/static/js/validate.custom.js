$("form").validate({
    rules: {
        name: {
            minlength: 3,
            maxlength: 20,
            required: true
        },
        phone: {
            required: true
        },
        email: {
            required: true,
            email: true
        },
        subject: {
            selectcheck: true
        },
        message: {
            minlength: 3,
            required: true
        }
    },
    highlight: function(element) {
    var id_attr = "#" + $( element ).attr("id") + "1";
    $(element).closest('.form-group').removeClass('has-success').addClass('has-error');
    $(id_attr).removeClass('glyphicon-ok').addClass('glyphicon-remove');
    },
    unhighlight: function(element) {
    var id_attr = "#" + $( element ).attr("id") + "1";
    $(element).closest('.form-group').removeClass('has-error').addClass('has-success');
    $(id_attr).removeClass('glyphicon-remove').addClass('glyphicon-ok'); 
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) {
        if(element.length) {
          error.insertAfter(element);
        } else {
          error.insertAfter(element);
        }
    } 
});
jQuery.validator.addMethod('selectcheck', function (val) {
  return (val != 0);
}, "件名をご選択ください。");
