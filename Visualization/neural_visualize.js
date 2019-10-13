function draw_neural(neural)
{
    var c = document.getElementById("neural");
    var ctx = c.getContext("2d");

    ctx.lineWidth = 3;
    ctx.canvas.width  = 1800;
    ctx.canvas.height  = 1080;
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    console.log(neural);
    size = 4;

    // Plot graph edges
    neural.edges.forEach(
        function(edge){
            rgb = Math.round(255*edge.link);
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
            var rgb = 50;
            ctx.fillStyle = "rgb("+rgb+","+rgb+","+rgb+")";
            ctx.fillRect(point.point[0], point.point[1],size,size);
            ctx.strokeRect(point.point[0], point.point[1],size,size);
            ctx.strokeText(point.id, point.point[0] + size, point.point[1] + size);
        }
    );
}
