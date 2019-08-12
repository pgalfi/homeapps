jQuery.fn.extend({
    setupAutoComplete: function () {
        let input_object = this[0];
        $(this).before("<input type='hidden' name='" + input_object.name + "-id' id='" + input_object.id + "-id'>");
        let minLength = input_object.dataset["min-length"] || 3;
        let max_results = input_object.dataset["max-results"] || 30;
        let data_url = input_object.dataset.url;
        let data_id = input_object.dataset.id || "id";
        let data_query = input_object.dataset.query || "q";
        let data_set = input_object.dataset.set || "results";
        let data_text = input_object.dataset.text || "name";
        let data_options_str = input_object.dataset.options || "{}";
        let data_options = JSON.parse(data_options_str.replace(/'/g, '"'));
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
            $("#" + input_object.id + "-id").val(suggestion[data_id]);
        });

    }
});

$(document).ready(function () {
    $(".autocomplete-select").setupAutoComplete();
});

