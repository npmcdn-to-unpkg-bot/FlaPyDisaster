

function change_table(source_id, target_class) {
    var me = $("#" + source_id);

    $.getJSON($SCRIPT_ROOT + "{{ url_for('change_table') }}", {
        name: me.val(),

    }, function (data) {
        // window.alert(data.table)
        var target = $("." + target_class);
        target.empty().append(data.table)
    });
}

function save_event_to_raster() {
    $.getJSON("{{ url_for('hurricane_save_event_to_raster') }}", {test: "test"},
        function (data) {
            console.log('Got raster response');
            //console.log(data.file_uri);
            document.getElementById("event_pic").src = data.file_uri
        }
    );
}
//
//function save_event_to_raster(){
//    $.ajax({
//    dataType: "json",
//        url: "{{ url_for('hurricane_save_event_to_raster') }}",
//        method: "GET",
//        success: function (data) {
//                    console.log('Got raster response');
//                    //console.log(data.file_uri);
//                    document.getElementById("event_pic").src = data.file_uri;
//                }
//    });
//}