$(document).ready(function(){
    $('ul.tabs').tabs();  // Give tabs interactivity

    $('ul.tabs').click(function(){
        this.scroll();
    });

    $('.dropdown-trigger').dropdown();

    $('.sidenav').sidenav();  // Add a sidenav menu for when the window is narrow.
    $('select').formSelect();
    $('input#sol-title, textarea#sol-description').characterCounter();
    M.updateTextFields();
});