$(document).ready(function course_table() {
    var table = $('#courses-table').DataTable({
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
            'url': 'view-courses-dt',
                },
        // 'displayStart': (page-1)*page_length,
        "stateSave": true,
        'initComplete': function() {
            table.page.info().page;
        },
        "columnDefs": [
                        {"orderable": true , "targets": 0},
                        {"orderable": true , "targets": 1},
                        {"orderable": true , "targets": 2},
                        {"orderable": true , "targets": 3},
                        {
                            "orderable": true , "targets": 4,
                            "render": function(data,type,row,meta){
                                return '<a href="'+row[4]+'">Edit</a>';
                            }
                        },
                        {
                            "orderable": true , "targets": 5,
                            "render": function(data,type,row,meta){
                                return '<a href="'+row[5]+'">Delete</a>';
                            }
                        },
                    ]
        // ...
        });
    });
