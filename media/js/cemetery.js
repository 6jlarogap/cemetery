/**
 * Created with PyCharm.
 * User: ilvar
 * Date: 06.06.12
 * Time: 23:30
 * To change this template use File | Settings | File Templates.
 */
$(function() {
    if (top.location.href != '/') {
        if (navigator.userAgent.toLowerCase().indexOf("chrome") >= 0) {
            $('input:-webkit-autofill').each(function(){
                var text = $(this).val();
                var name = $(this).attr('name');
                $(this).after(this.outerHTML).remove();
                $('input[name=' + name + ']').val(text);
            });
        }
    }
    $('input').attr('autocomplete', 'off');

    COUNTRY_URL = '/geo/autocomplete/country/';
    REGION_URL = '/geo/autocomplete/region/';
    CITY_URL = '/geo/autocomplete/city/';
    STREET_URL = '/geo/autocomplete/street/';

    $('input.autocomplete[name$=country]').typeahead({
        source: function (typeahead, query) {
            if (query.length < 2) { return }
            $.ajax({
                url: COUNTRY_URL + "?query=" + query,
                success: function(data) {
                    typeahead.process(data)
                }
            });
        },
        onselect: function (obj) {
            console.log(obj);
        }
    });
    $('input.autocomplete[name$=region]').typeahead({
        source: function (typeahead, query) {
            if (query.length < 2) { return }
            var input = $(this)[0].$element;
            var country = input.parents('.well').find('input[name$=country]').val();
            $.ajax({
                url: REGION_URL + "?query=" + query + "&country=" + country,
                success: function(data) {
                    typeahead.process(data)
                }
            });
        },
        onselect: function (obj) {
            console.log(obj);
        }
    });
    $('input.autocomplete[name$=city]').typeahead({
        source: function (typeahead, query) {
            if (query.length < 2) { return }
            var input = $(this)[0].$element;
            var country = input.parents('.well').find('input[name$=country]').val();
            var region = input.parents('.well').find('input[name$=region]').val();
            $.ajax({
                url: CITY_URL + "?query=" + query + "&country=" + country + "&region=" + region,
                success: function(data) {
                    typeahead.process(data)
                }
            });
        },
        onselect: function (obj) {
            console.log(obj);
        }
    });
    $('input.autocomplete[name$=street]').typeahead({
        source: function (typeahead, query) {
            if (query.length < 2) { return }
            var input = $(this)[0].$element;
            var country = input.parents('.well').find('input[name$=country]').val();
            var region = input.parents('.well').find('input[name$=region]').val();
            var city = input.parents('.well').find('input[name$=city]').val();
            $.ajax({
                url: STREET_URL + "?query=" + query + "&country=" + country + "&region=" + region + "&city=" + city,
                success: function(data) {
                    typeahead.process(data)
                }
            });
        },
        onselect: function (obj) {
            console.log(obj);
        }
    });

    updateControls();

    $('a.load').click(function(){
        $('#block_empty').hide();
        $('#block_empty').load(this.href, function() {
            updateControls();

            $('#block_empty').fadeIn('fast');
        });
        return false;
    });

    $('form.in-place').live('submit', function(){
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data, function(data) {
            $('#block_empty').html(data);
        });
        return false;
    });

    $('form.main-add :input').change(function(){
        var ready = true;
        $('form.main-add :input').each(function() {
            if (!$(this).val()) {
                ready = false;
            }
        });
        if (!ready) {
            $('form.main-add .btn-primary').attr('disabled', 'disabled');
        } else {
            $('form.main-add .btn-primary').removeAttr('disabled');
        }
    });

});

function updateControls() {
    $('span.move-left').remove();
    $('input[id*=date]').after('<span class="add-on move-left"><i class="icon-calendar"></i></span>').datepicker({inline: true});
    $('input[id*=time]').after('<span class="add-on move-left"><i class="icon-time"></i></span>').timepicker({inline: true});

}