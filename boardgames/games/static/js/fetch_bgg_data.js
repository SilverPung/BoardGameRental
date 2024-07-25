$(document).ready(function() {
    $('#manualTitleToggle').prop('checked', true);
    $('#manualDistributorToggle').prop('checked', true);
    
    
    
    
    $('#fetchData').on('click', function() {
        var bggUrl = $('#bggUrl').val();
        if (bggUrl) {
            $.ajax({
                type: 'GET',
                url: '/games/fetch_bgg_data/',
                data: {
                    'bgg_url': bggUrl
                },
                success: function(data) {
                    $('#id_image').val(data.image);
                    $('#titles_select').empty();
                    $('#distributors_select').empty();
                
                    // Populate 'titles_select'
                    data.titles.forEach(function(title) {
                        $('#titles_select').append($('<option>').val(title).text(title));
                    });
                
                    data.distributors.forEach(function(distributor) {
                        $('#distributors_select').append($('<option>').val(distributor).text(distributor));
                    });

                    // Show the manual input toggle buttons
                    $('#manualTitleToggle').removeClass('hidden');
                    $('#manualDistributorToggle').removeClass('hidden');

                    // Show the titles and distributors select, and hide the manual inputs
                    $('#titles_select').show();
                    $('#manual_title').hide();
                    $('#manualTitleToggle').prop('checked', false);

                    $('#distributors_select').show();
                    $('#manual_distributor').hide();
                    $('#manualDistributorToggle').prop('checked', false);

                    $('#manualTitleToggle').prop('checked', false);
                    $('#manualDistributorToggle').prop('checked', false);
                    $('#titles_select').show();
                    $('#manual_title').hide();
                    $('#distributors_select').show();
                    $('#manual_distributor').hide();


                },
                error: function() {
                    alert('An error occurred. Please try again.');
                }
            });
        } else {
            alert('Please enter a BGG URL.');
        }
    });

    // Toggle between manual input and fetched titles
    $('#manualTitleToggle').on('change', function() {
        if ($(this).is(':checked')) {
            $('#titles_select').hide();
            $('#manual_title').show();
        } else {
            $('#titles_select').show();
            $('#manual_title').hide();
        }
    });

    // Toggle between manual input and fetched distributors
    $('#manualDistributorToggle').on('change', function() {
        if ($(this).is(':checked')) {
            $('#distributors_select').hide();
            $('#manual_distributor').show();
        } else {
            $('#distributors_select').show();
            $('#manual_distributor').hide();
        }
    });

    // Update hidden fields on form submit
    $('form').on('submit', function() {
        if ($('#manualTitleToggle').is(':checked')) {
            $('#final_title').val($('#manual_title').val());
        } else {
            $('#final_title').val($('#titles_select').val());
        }

        if ($('#manualDistributorToggle').is(':checked')) {
            $('#final_distributor').val($('#manual_distributor').val());
        } else {
            $('#final_distributor').val($('#distributors_select').val());
        }
    });
});