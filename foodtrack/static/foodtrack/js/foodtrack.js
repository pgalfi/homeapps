jQuery.fn.extend({
    setupAutoComplete: function () {
        let input_object = this[0];
        let minLength = input_object.dataset.minLength || 3;
        let max_results = input_object.dataset.maxResults || 30;
        let data_url = input_object.dataset.url;
        let data_id = input_object.dataset.id || "id";
        let data_query = input_object.dataset.query || "q";
        let data_set = input_object.dataset.set || "results";
        let data_text = input_object.dataset.text || "name";
        let data_options_str = input_object.dataset.options || "{}";
        let data_options = JSON.parse(data_options_str.replace(/'/g, '"'));
        let data_id_set_name = input_object.dataset.setName || input_object.name + "-id";
        let destination_id = input_object.id + "-id";
        let destination_element = $("[name='" + data_id_set_name + "'");
        if (!destination_element.length) {
            $(this).before("<input type='hidden' name='" + data_id_set_name + "' id='" + destination_id + "'>");
        } else destination_id = destination_element[0].id;
        let typingTimer;
        $(this).typeahead({
            minLength: minLength,
        }, {
            name: "food_list",
            limit: max_results,
            display: function (item) {
                return item[data_text];
            },
            source: function (query, sync, aSync) {
                clearTimeout(typingTimer);
                typingTimer = setTimeout(function () {
                    $.ajax({
                        url: data_url,
                        type: "get",
                        contentType: 'application/json',
                        dataType: "json",
                        data: {...data_options, [data_query]: query},
                        error: function(jqXHR, status, error) {
                            console.log(error);
                        },
                        success: function (data, status, jqXHR) {
                            data_results = [];
                            raw_data = data;
                            if (data.hasOwnProperty(data_set)) raw_data = data[data_set];
                            raw_data.forEach(function (item) {
                                data_results.push(item);
                            });
                            aSync(data_results);
                        }
                    })
                }, 400)
            },
        }).bind("typeahead:select", function (e, suggestion) {
            $("#" + destination_id).val(suggestion[data_id]);
        }).bind("typeahead:change", function (e) {
            if (e.currentTarget.value==="") {
                $("#" + destination_id).val("");
            }
        });

    }
});

$(document).ready(function () {
    $(".autocomplete-select").setupAutoComplete();
});

