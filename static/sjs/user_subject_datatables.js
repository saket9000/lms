$(document).ready(function subject_table() {
    var table = $('#user-subjects-table').DataTable({
        // ...
        "dom": '<"top"lBf>rt<"bottom"ip><"clear">',
        buttons: [
            {
                extend: 'copy',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'print',
                exportOptions: {
                    columns: ':visible'
                }
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':visible'
                }
            },

            'colvis'
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            'url': 'view-user-subjects-dt',
                },
        // 'displayStart': (page-1)*page_length,
        "stateSave": true,
        'initComplete': function() {
            table.page.info().page;
        },
        "columnDefs": [
                        {"orderable": true , "targets": 0},
                        {"orderable": true , "targets": 1},
                        {
                            "orderable": true , "targets": 2,
                            "render": function(data,type,row,meta){
                                return '<a href="'+row[2]+'">View</a>';
                            }
                        },
                    ]
        // ...
        });
    });
