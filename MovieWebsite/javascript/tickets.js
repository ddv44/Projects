
window.onload = function() {
    let seats = document.getElementsByClassName("seat");
    var count = document.getElementById('ticket_num');
    var x = 0;

    for(let i = 0; i < seats.length; i++) {
        seats[i].onclick = function () {
            seats[i].style.backgroundColor = 'FF7F27';
        }
    }
};
