function draw_neural(neural)
{
    var c = document.getElementById("neural");
    var ctx = c.getContext("2d");

    ctx.lineWidth = 3;
    ctx.canvas.width  = 1800;
    ctx.canvas.height  = 1080;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    console.log(neural);
    size = 12;

    // Plot graph edges
    neural.edges.forEach(
        function(edge){
            rgb = Math.round(255*(edge.link+ 0.25));
            ctx.strokeStyle = "rgb("+rgb+","+rgb+","+rgb+")";
            ctx.beginPath();
            ctx.moveTo(edge.from.point[0], edge.from.point[1]);
            ctx.lineTo(edge.to.point[0], edge.to.point[1]);
            ctx.stroke();
        }
    );

    // Plot graph points
    neural.points.forEach(
        function(point){
            ctx.strokeStyle = 'white';
            ctx.fillStyle = colors[point.cluster - 1];
            ctx.fillRect(point.point[0], point.point[1],size,size);
            ctx.strokeRect(point.point[0], point.point[1],size,size);
            ctx.strokeText(point.id, point.point[0] + size, point.point[1] + size);
        }
    );
}
var colors = ['red', 'green', 'blue', 'orange', 'yellow', 'purple', 'fuchsia'];
function load_move(e) {
  var x = e.clientX;
  var y = e.clientY;
  load_graph(x - 50, y - 50);
}

var perc = 0;

function expand(){
    perc++;
    if(perc < 600){
        expand_data(perc);
    }
}
setInterval(expand, 100);