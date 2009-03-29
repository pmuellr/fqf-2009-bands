//------------------------------------------------------------------------------
//
//------------------------------------------------------------------------------

var search_box       = null
var search_text      = null
var supports_db      = false
var db               = null

//------------------------------------------------------------------------------
// a favorite checkbox was clicked
//------------------------------------------------------------------------------
function favorite_checkbox_clicked() {
    var element  = $(this)
    var id       = element.attr("id").substr(0,2)
    var row      = $("#" + id + "-r")
    var selected = element.val()
    
    if (selected) {
        selected = true
        row.css("display","table-row")
    }
    else {
        selected = false
        row.css("display","none")
    }
    
    if (!db) return
    
    if (selected) {
        var stmt = "INSERT INTO favorite_shows (id) VALUES(?);"
    }
    else {
        var stmt = "DELETE FROM favorite_shows WHERE id=?;"
    }
    
    db.transaction(
        function (transaction) {
            transaction.executeSql(
                stmt, 
                [id], 
                function() {}, 
                errorHandler
                )
        }
    )
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
// null handler
//------------------------------------------------------------------------------
function nullDataHandler(transaction, results) { }

//------------------------------------------------------------------------------
// error handler
//------------------------------------------------------------------------------
function errorHandler(transaction, error) {
    alert('Oops.  Error was ' + error.message + ' (Code ' + error.code + ')')

    return true
}

//------------------------------------------------------------------------------
// initialize the checkboxes from the db, finished
//------------------------------------------------------------------------------
function initialize_checkboxes_from_db_finished(transaction, results) {
    for (var i=0; i<results.rows.length; i++) {
        var row = results.rows.item(i)
        var id  = row['id']
        $("#" + id + "-c").each(function() { this.checked = true})
        $("#" + id + "-r").css("display","table-row")
    }
}

//------------------------------------------------------------------------------
// initialize the checkboxes from the db
//------------------------------------------------------------------------------
function initialize_checkboxes_from_db() {
    db.transaction(
        function (transaction) {
            // The first query causes the transaction to (intentionally) fail if the table exists.
            transaction.executeSql(
                'SELECT id from favorite_shows;', 
                [], 
                initialize_checkboxes_from_db_finished, 
                errorHandler
                )
        }
    )
}

//------------------------------------------------------------------------------
// create tables
//------------------------------------------------------------------------------
function createTables(db) {
    db.transaction(
        function (transaction) {
            // The first query causes the transaction to (intentionally) fail if the table exists.
            transaction.executeSql(
                'CREATE TABLE favorite_shows(id VARCHAR NOT NULL PRIMARY KEY);', 
                [], 
                function() {}, 
                function() {}
                )
        }
    )
}

//------------------------------------------------------------------------------
// initialize database
//------------------------------------------------------------------------------
function init_db() {
    try {
        var shortName = 'fqf-2009'
        var version   = '1.0'
        var maxSize   = 1000000
        return openDatabase(shortName, version, shortName, maxSize)
    }
    
    catch(e) {
        if (e == INVALID_STATE_ERR) {
            alert("Invalid database version.")
        } 
        else {
            alert("Unknown error "+e+".")
        }
    }

    return null
}

//------------------------------------------------------------------------------
// main function
//------------------------------------------------------------------------------
$(document).ready(function() {

    supports_db = (null != window.openDatabase)
    if (supports_db) {
        $(".no-supports-db" ).css("display","none")
        db = init_db()
        createTables(db)
    }

    arm_favorite_checkboxes()
    
    initialize_checkboxes_from_db()
    
    search_box = $("#search-box")
    search_box.keyup(search_text_changed)
})

