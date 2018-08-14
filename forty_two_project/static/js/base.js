$(document).ready(function(){
    $('ul.tabs').tabs();  // Make solution sections interactive tabs.

    $('ul.tabs').click(function(){
        this.scroll();
    });

    $('.dropdown-trigger').dropdown(); // For the user side menu.


    $('.sidenav').sidenav();  // Add a sidenav menu for when the window is narrow.
    $('select').formSelect(); // Initialise form 'selection' dropdown fields.
    $('input#sol-title, textarea#sol-description').characterCounter();  // Add a character counter to fields with limits.


    $('.tooltipped').tooltip();  // Adding tooltips for solution titles (they don't always fit with the grid)

    $('.fixed-action-btn').floatingActionButton();  // Initialise the new solution button as a fab

    $('.modal').modal();  // Initialise modals

    // Open a modal containing an add new solution form.
    $('.fixed-action-btn').click(function(){
        $('.modal').open();
    });
    M.updateTextFields();  // Make form fields responsive (show number of characters used etc.).


    $('#fab-new-sol').hover(function(){
        var angle = ($('#fab-new-sol').data('angle')) || 0;
        angle -= 45;
        $('#fab-new-sol').css({'transform': 'rotate('+angle+'deg)'});
        $('#fab-new-sol').data('angle', angle);
    }, function(){
        var angle = ($('#fab-new-sol').data('angle')) || 0;
        angle += 45;
        $('#fab-new-sol').css({'transform': 'rotate('+angle+'deg)'});
        $('#fab-new-sol').data('angle', angle);
    });
});