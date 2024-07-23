$(document).ready(function() {
    $('#fetchData').on('click', function() {
        var bggUrl = $('#bggUrl').val();
        if (bggUrl) {
            $.ajax({
                type: 'GET',
                url: 'games/fetch_bgg_data/',
                data: {
                    'bgg_url': bggUrl
                },
                success: function(data) {
                    $('#id_title').val(data.title);
                    $('#id_image').val(data.image);
                    $('#id_distributor').val(data.distributor);
                },
                error: function() {
                    alert('An error occurred. Please try again.');
                }
            });
        } else {
            alert('Please enter a BGG URL.');
        }
    });
});
