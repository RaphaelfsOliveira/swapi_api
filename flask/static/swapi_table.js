data = data[0]['results'];

remove_columns = [
    'films',
    'homeworld',
    'species',
    'url',
    'vehicles',
    'starships',
    'opening_crawl',
    'characters',
    'created',
    'edited',
    'planets',
    'people',
    'residents',
    'pilots',
]

var my_columns = [];

$.each(data[0], function (key, value) {
    var my_item = {};
    if (remove_columns.includes(key)) {
    } else {
        my_item.data = key;
        my_item.title = `<b>${key.toUpperCase()}</b>`;
        my_columns.push(my_item);
    }
});

$(document).ready(function () {
    $('select').formSelect();

    $('#myTable').DataTable({
        lengthChange: false,
        paging: false,
        data: data,
        columns: my_columns,
        columnDefs: [
            {
                targets: ['_all'],
                className: 'mdc-data-table__cell'
            }
        ]
    });

});