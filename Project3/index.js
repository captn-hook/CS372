
var canvas = document.getElementById('canvas')

var context = canvas.getContext('2d');

context.beginPath()
context.rect(0, 0, context.canvas.width, context.canvas.height);
context.fillStyle = 'rgb(200, 0, 0)';
context.fill();

var i = 0;
var j = 0;

canvas.addEventListener('click', function(event) {

    context.beginPath()
    context.rect(0, 0, context.canvas.width, context.canvas.height);
    context.fillStyle = 'rgb(200, ' + j + ', ' + i + ')';
    context.fill();
    
    if (i > 255) {
        j += 10
    } else {
        i += 10;
    }

    if (j > 255) {
        i = 0;
        j = 0;
    }
})