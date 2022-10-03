var canvas = document.getElementById('canvas')

var context = canvas.getContext('2d');

canvas.addEventListener('click', function(event) {
    var x = event.clientX;
    var y = event.clientY;
    context.beginPath();
    context.arc(x, y, 10, 0, 2 * Math.PI);
    context.stroke();
})