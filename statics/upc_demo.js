$(document).ready(function() {
    $('.crawl_url').each(function(ix) {
        var el = $(this);
        $.get('/specs', {remote_url: $(this).attr('data_url')})
            .done(function(data) {
                el.after(data);
            });
    });

    $(document).on('click', '.mark_data', function() {
        var d = $(this);
        var data = {judgement: d.attr('data-judgement'),
                    k: d.attr('data-k'),
                    v: d.attr('data-v'),
                    method: d.attr('data-method'),
                    remote_url: d.attr('data-remote-url')};
        $.post('/judge',
               data);

    });


});
