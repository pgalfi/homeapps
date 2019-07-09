$(function(){
	$("#search_button").bind("click", update_property_list);
	$("#next_button").bind("click", next_page);
	$("#prev_button").bind("click", prev_page);
	$("#paginator").bind("change", page_selected)

});

function update_property_list(e, page=1) {
    console.log(page);
    let form_element = document.getElementById("search-form");
    let formData = new FormData(form_element);
    let url_params = "page=" + encodeURIComponent(page);
    for (let pair of formData.entries()) {
        if (pair[0]==='page') continue;
        url_params += "&" + pair[0] + "=" + encodeURIComponent(pair[1]);
    }
    $.ajax({
        url: "/housing/api/houses?" + url_params,
        type: "GET",
        success: function(data) {
            let count = data.count;
            let pages = (count +9) / 10;
            let page_selector = $("#paginator");
            page_selector.children("option").remove();
            for (let i=1; i<=pages; i++)
                page_selector.append("<option value='" + i +"'>" + i + "</>");
            page_selector.find("option[value='" + page + "']").prop('selected', 'selected');
            buildHouseList(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('error: ' + textStatus + ': ' + errorThrown);
        }
    });

    return false;
}

function next_page() {
    let page_selector = $("#paginator");
    let current_page = parseInt(page_selector.children("option:selected").val());
    let last_page = parseInt(page_selector.children("option:last").val());
    if (current_page<last_page) update_property_list(null, current_page + 1);
    return false;
}

function prev_page() {
    let page_selector = $("#paginator");
    let current_page = parseInt(page_selector.children("option:selected").val());
    if (current_page>1) update_property_list(null, current_page - 1);
    return false;
}

function page_selected() {
    let page_selector = $("#paginator");
    let current_page = parseInt(page_selector.children("option:selected").val());
    update_property_list(null, current_page);
}

function property_click(house_link) {
    let house_id = $(house_link).closest(".row")[0].id;
    $.ajax({
        url: "/housing/api/houses/" + house_id + "/viewed/",
        type: "POST",
        success: function(data) {

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('error: ' + textStatus + ': ' + errorThrown);
        }
    });
}

function like_property(button_link) {
    let house_id = $(house_link).closest(".row")[0].id;
    $.ajax({
        url: "/housing/api/houses/" + house_id + "/liked/",
        type: "POST",
        success: function(data) {

        },
        error: function (jqXHR, textStatus, errorThrown) {
            alert('error: ' + textStatus + ': ' + errorThrown);
        }
    });
    return false;
}

function buildHouseList(api_data) {
    let html_element = `
            <div class="row mb-1 with-border" id="house-%house_id%">
                    <div class="col-lg-3">
                      <img src="%img_link%" class="property-image">
                    </div>
                    <div class="col-lg-7">
                        <h5 class="card-title"><a href="%id_link%" target="_blank" 
                        onclick="property_click(this);">%desc_short%</a> (%advertiser_name%)</h5>
                        <p class="card-text">%desc_long%</p>
                        <p class="card-text mb-0"><small class="text-muted">Date: %post_date%</small></p>
                      
                    </div>
                  <div class="col-lg-2">
                      <p class="card-text font-weight-bold">DETAILS:</p>
                      <p class="card-text mb-0"><span class="font-weight-bold">Price: </span>%price_format% 
                      %advertiser_currency%</p>
                      <p class="card-text m-0"><span class="font-weight-bold">
                          Size: </span>%size% m<span class="text-superscript">2</span></p>
                      <p class="card-text mb-0"><span class="font-weight-bold">Rooms: </span>%rooms%</p>
                      %viewed%
                      %liked%
                  </div>
            </div>
    `;
    let page_selector = $("#paginator");
    let current_page = page_selector.children("option:selected").val();

    let house_listing = $("div.house-listing");
    house_listing.html("");
    console.log(api_data);
    for (let i=0; i<api_data.results.length; i++) {
        let house = api_data.results[i];
        console.log(house);
        let image_link = "";
        let profile_link = "";
        for (let j=0; j<house.links.length; j++) {
            let alink = house.links[j];
            if (alink.link_type===20) profile_link = alink.link;
            if (alink.link_type===10) image_link = alink.link;
        }
        let one_element = html_element;
        one_element = one_element.replace("%desc_long%", house.description);
        one_element = one_element.replace("%desc_short%", house.description.substring(0, 50));
        one_element = one_element.replace("%img_link%", image_link);
        one_element = one_element.replace("%id_link%", profile_link);
        one_element = one_element.replace("%reference_id%", house.reference_id);
        one_element = one_element.replace("%house_id%", house.id);
        one_element = one_element.replace("%post_date%", house.post_date);
        one_element = one_element.replace("%advertiser_name%", house.advertiser_name);
        one_element = one_element.replace("%advertiser_currency%", house.advertiser_currency);
        one_element = one_element.replace("%price_format%", house.price);
        one_element = one_element.replace("%size%", (house.size==null ? '' : house.size));
        one_element = one_element.replace("%rooms%", (house.rooms===null ? '' : house.rooms));
        if (house.viewed_date !== null ) one_element = one_element.replace("%viewed%",
            '<p class="card-text mb-0"><img src="/static/housing/img/viewed.png" class="card-small-image" alt=""/>Viewed: '
            + house.viewed_date + '</p>');
        else one_element = one_element.replace("%viewed%", '');
        if (house.liked === true) one_element = one_element.replace("%liked%",
            '<p class="card-text mb-0"><img src="/static/housing/img/like.png" class="card-small-image" alt=""/>' +
            '<button class="btn-primary btn-sm" onclick="like_property(this);">Not Like</button></p>');
        else one_element = one_element.replace("%liked%", '<p class="card-text mb-0">' +
            '<button class="btn-primary btn-sm" onclick="like_property(this);">Like</button></p>');
        house_listing.append(one_element);
    }

}