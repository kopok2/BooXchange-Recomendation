comm_interval = 500;
setInterval(check_comm, comm_interval); //enable form asynchronous communication
set_focus();
function load_js_script(path)
{
    var script = document.createElement('script');
    script.src = path;
    document.head.appendChild(script);
}
