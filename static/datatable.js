$(function () {
    let table = $('#example').dataTable({
        "columnDefs" : [{
            "targets" : [3,4],
            "orderable" : false,
        },
        {responsivePriority: 1, targets: 2},
        {responsivePriority: 2, targets: 1},
        {
            targets : [3,4],
            className : "all",
        }
    ],
        // "columnDefs" : [{
        //     "targets" : [3,4],
        //     "orderable" : false,
        // },

        "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
        responsive: true
    });
});