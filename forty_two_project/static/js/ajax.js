// Allow us to add in a search query to the context dictionary once we release keys on the search box
// The template is then rendered-to-response with the previous context updated with the search string.
// This should render solutions filtered not just by subject but by search string.
$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type: 'POST',
            'url': '',
            data:{
                'search_text': $('#search').val(),
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: searchSuccessful,
                dataType: 'html'
        })
    })
});

function searchSuccessful(data, textStatus, jqXHR){
    $('#search-results').html(data);
}