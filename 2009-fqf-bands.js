//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------

var search_box       = null
var search_text      = null

//------------------------------------------------------------------------------
// a favorite checkbox was clicked
//------------------------------------------------------------------------------
function favorite_checkbox_clicked() {
    var element = $(this)
    var id = element.attr("id").substr(0,2)
    var row = $("#" + id + "-r")
    
    if (element.val()) {
        row.css("display","table-row")
    }
    else {
        row.css("display","none")
    }
}

//------------------------------------------------------------------------------
// set up processing for favorite checkbox clicks
//------------------------------------------------------------------------------
function arm_favorite_checkboxes() {
    $(".fav-checkbox").click(favorite_checkbox_clicked)
}

//------------------------------------------------------------------------------
// filter the entries for the search criteria
//------------------------------------------------------------------------------
function search_filter(index) {
    if (this.title) {
        var title = this.title.toUpperCase()
        if (-1 != title.indexOf(search_text)) return true
    }
    
    var content = $(this).text().toUpperCase()
    return -1 != content.indexOf(search_text)
}

//------------------------------------------------------------------------------
// processing when the search text has changed
//------------------------------------------------------------------------------
function search_text_changed() {
    search_text = search_box.val().toUpperCase()
    
    if (search_text == "") {
        $(".entry").css("opacity", "1.0").css("-moz-opacity", "1.0")
        $("#selected-count").html("All")
    }
    else {
        $(".entry").css("opacity", "0.2").css("-moz-opacity", "0.2")
        var selected = $(".entry").filter(search_filter).css("opacity", "1.0").css("-moz-opacity", "1.0").size()
        $("#selected-count").html("" + selected)
    }
}

//------------------------------------------------------------------------------
// main function
//------------------------------------------------------------------------------
$(document).ready(function() {

    arm_favorite_checkboxes()
    
    search_box = $("#search-box")
    search_box.keyup(search_text_changed)
})

