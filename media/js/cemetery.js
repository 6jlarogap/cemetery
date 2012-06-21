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

    $('input.autocomplete[name$=country]').attr('autocomplete', 'off').typeahead({
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
    $('input.autocomplete[name$=region]').attr('autocomplete', 'off').typeahead({
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
    $('input.autocomplete[name$=city]').attr('autocomplete', 'off').typeahead({
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
    $('input.autocomplete[name$=street]').attr('autocomplete', 'off').typeahead({
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

    $('a.load').live('click', function(){
        $('#block_empty').hide();
        $('#block_empty').load(this.href, function() {
            updateControls();
            $('#block_empty').fadeIn('fast', function() {
                $('#id_customer-customer_type').change();
            });
        });
        return false;
    });

    $('form.in-place').live('submit', function(){
        var url = $(this).attr('action');
        var data = $(this).serialize();
        $.post(url, data, function(data) {
            $('#block_empty').html(data);
            $('.errorlist').addClass('alert');
            updateInnerForm();
        });
        return false;
    });

    $('#id_operation, #id_place, #id_person').live('change', function(){
        var ready = true;
        $('#id_operation, #id_place, #id_person').each(function() {
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

    $('#id_operation, #id_place, #id_person').change();

    $('.errorlist').addClass('alert');

    $('#mainform #id_account_book_n_from').parents('p').before('<br/>');

    $('#id_customer-customer_type').live('change', function() {
        if ($(this).val() == 1) {
            $('.fields-fizik').slideUp('fast', function() {
                $('.fields-yurik').slideDown('fast');
            });
        } else {
            $('.fields-yurik').slideUp('fast', function() {
                $('.fields-fizik').slideDown('fast');
            });
        }
    });

    $('#id_customer-agent_director').live('change', function() {
        if ($(this).is(':checked') ) {
            $('.fields-agent').slideUp('fast');
        } else {
            $('.fields-agent').slideDown('fast');
        }
    });
});

function makeDatePicker(obj) {
    $.datepicker.setDefaults($.datepicker.regional['']);
    var now = new Date();
    var now_year = now.getFullYear();

    obj.after('<span class="add-on move-left"><i class="icon-calendar"></i></span>').datepicker({
        dateFormat: 'dd.mm.yy',
        changeMonth: true,
        changeYear: true,
        yearRange: '1900:' + now_year,
        firstDay: 1,
        monthNamesShort: ['Янв','Фев','Март','Апрель','Май','Июнь','Июль','Авг','Сен','Окт','Ноя','Дек'],
        dayNamesMin: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
        showOn: "focus",
        inline: true
    });

    if (now.getMonth() == 11 && now.getDate() > 20) {
        $('input#id_burial_date').datepicker('option', 'yearRange', '1900:' +  (now_year + 1));
    }
}

function makeTimePicker(obj) {
    obj.after('<span class="add-on move-left"><i class="icon-time"></i></span>').timepicker({
        showOn: "focus",
        hourText: 'Ч',
        minuteText: 'М',
        showPeriodLabels: false,
        minutes: {
            starts: 0,
            ends: 45,
            interval: 15
        },
        hours: {
            starts: 8,
            ends: 19,
            interval: 1
        },
        inline: true
    });
}

function updateControls() {
    $('span.move-left').remove();
    makeDatePicker($('input[id*=date]'));
    makeTimePicker($('input[id*=time]'));
    $('#id_customer-customer_type').change();
    setTimeout(function() {
        $('#id_customer-agent_director').change();
    }, 100);
}

function updateInnerForm() {
    makeDatePicker($('#block_empty input[id*=date]'));
    makeTimePicker($('#block_empty input[id*=time]'));
    $('#id_customer-customer_type').change();
    setTimeout(function() {
        $('#id_customer-agent_director').change();
    }, 100);
}