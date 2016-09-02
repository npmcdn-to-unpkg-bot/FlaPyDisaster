

function change_table(source_id, target_class) {
    var me = $("#" + source_id);

    $.getJSON($SCRIPT_ROOT + "{{ url_for('change_table') }}", {
        name: me.val(),

    }, function (data) {
        # window.alert(data.table)
        var target = $("." + target_class);
        target.empty().append(data.table)
    });
}