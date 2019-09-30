function draw_neural(neural)
{
    var c = document.getElementById("neural");
    var ctx = c.getContext("2d");
    var size = 12;
    var distanceX = 120;
    var distanceY = 40;
    
    ctx.lineWidth = 1;
    ctx.canvas.width  = neural.last_neurons.length*(size + distanceX);
    biggest_count = 0;
    neural.last_neurons.forEach(function(entry) {
        if(entry.length>biggest_count){biggest_count = entry.length;}
    });
    ctx.canvas.height  = biggest_count*(size + distanceY);
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    console.log(neural);
    
    var x = 0;
    neural.weights.forEach(
        function(layer){
        y=0;
            layer.forEach(function(neuron){
            z=0;
                neuron.forEach(function(connection){
                    //console.log(x);
                    //console.log(y);
                    //console.log(z);
                    //console.log(connection);
                    rgb = Math.round(255*connection);
                    if(connection>0)
                    {
                    ctx.strokeStyle = "rgb("+0+","+200+","+rgb+")";}
                    else{
                        rgb = -rgb;
                        ctx.strokeStyle = "rgb("+rgb+","+100+","+0+")";
                    }
                    ctx.beginPath();
                    halfsize = Math.round(size/2);
                    ctx.moveTo(x*(size+distanceX)+halfsize,y*(size+distanceY)+halfsize);
                    ctx.lineTo((x+1)*(size+distanceX)+halfsize,z*(size+distanceY)+halfsize);
                    ctx.stroke(); 
                    z++;
                });
            y++;
            });
        x++;
        }
        );
    x=0;
    neural.last_neurons.forEach(function(entry) {
        var y = 0;
        entry.forEach(function(neuron) {
            console.log(neuron[0]);
            var rgb = Math.round(255*neuron[0]);
            ctx.strokeStyle = 'white';
            ctx.fillStyle = "rgb("+rgb+","+rgb+","+rgb+")";
            ctx.fillRect(x*(size+distanceX),y*(size+distanceY),size,size);
            ctx.strokeRect(x*(size+distanceX),y*(size+distanceY),size,size);
            ctx.strokeText(Math.round(neuron[0] * 100) / 100,x*(size+distanceX)+size,y*(size+distanceY)+size);
            y++;
        });
        x++;
    });
    
    
    //ctx.fillRect();
}
//setInterval(function(){ load_neural(); }, 100);