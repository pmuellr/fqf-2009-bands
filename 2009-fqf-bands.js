//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------

var c_circle_open = "\u25EF"
var c_circle_fill = "\u25C9"

var search_box       = null
var search_text      = null
var report_button    = null
var showing_report   = false

//------------------------------------------------------------------------------
//
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
//
//------------------------------------------------------------------------------
function is_hearted(index) {
    var char = this.innerHTML 
    return char == c_circle_fill
}

//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------
function report_button_clicked() {
    showing_report = !showing_report
    if (showing_report) {
        report_button.val("Show Schedule")
        return
    }
    
    report_button.val("Show Favorites Report")
}

//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------
function toggle_favorite_entry(id) {
    var element = $("#" + id + "-c")
    var row     = $("#" + id + "-r")
    
    var c = element.html()
    if (c == c_circle_open) {
        element.html(c_circle_fill)
        row.css("display","table-row")
    }
    else {
        element.html(c_circle_open)
        row.css("display","none")
    }
    
}

//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------
$(document).ready(function() {
    report_button = $("#report-button")
    report_button.click(report_button_clicked)
    
    search_box = $("#search-box")
    
    search_box.keyup(function() {
        search_text = search_box.val().toUpperCase()
        
        if (search_text == "") {
            // opacity: -moz-opacity:
            $(".entry").css("opacity", "1.0").css("-moz-opacity", "1.0")
            $("#selected-count").html("All")
        }
        else {
            $(".entry").css("opacity", "0.2").css("-moz-opacity", "0.2")
            var selected = $(".entry").filter(search_filter).css("opacity", "1.0").css("-moz-opacity", "1.0").size()
            $("#selected-count").html("" + selected)
        }
    })
})

