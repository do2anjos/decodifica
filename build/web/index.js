    globalThis.__canvas_resized = (self, ecw, ech) => {
        console.warn("TODO: panda3d canvas monitor", self, ecw, ech)
    }

    async function custom_onload(debug_hidden) {
        // this is called before anything python is loaded
        // make your js customization here
        console.log("custom_onload")

        pyconsole.hidden = debug_hidden
        system.hidden = debug_hidden
        transfer.hidden = debug_hidden
        info.hidden = debug_hidden
        box.hidden =  debug_hidden

        show_infobox()
    }

    function custom_prerun(){
        // no python main and no (MEMFS + VFS) yet.
        console.log("custom_prerun")

    }

    function custom_postrun(){
        // python main and no VFS filesystem yet.
        console.log("custom_postrun")

    }

    function debug() {
        // allow to gain access to dev tools from js console
        // but only on desktop. difficult to reach when in iframe
        python.config.debug = true
        custom_onload(false)
        Module.PyRun_SimpleString("shell.uptime()")
        window_resize()
    }

    function info_inline(data){
        document.getElementById("info").innerHTML = data
    }

    function info_online(url) {
        // display info about current APK
        fetch( url /*, options */)
            .then((response) => response.text())
            .then((html) => {
                info_inline(html);
        })
        .catch((error) => {
            console.warn(error);
        });
    }

    function frame_online(url) {
        window.frames["iframe"].location = url;
    }
