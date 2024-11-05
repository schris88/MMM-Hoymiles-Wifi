/* Magic Mirror
 * Module: MMM-Hoymiles-Wifi
 *
 * By ulrichwisser
 */

Module.register("MMM-Hoymiles-Wifi", {

    start: function() {
        // send config to node helper
        this.sendSocketNotification("INIT", this.config)
    },

    scheduleUpdate: function(delay) {
        let self = this;
        let nextLoad = this.config.updateInterval;
        if (typeof delay !== "undefined" && delay >= 0) {
            nextLoad = delay;
        }
        if (nextLoad == 0) {
            return;
        }
        setTimeout(function() {
            self.updateDom();
            self.scheduleUpdate();
        }, nextLoad);
    },

    getDom: function() {
        var wrapper = document.createElement("div");
        wrapper.setAttribute("timestamp", new Date().getTime()); // make element unique so mm doesn't ignore our update

        if (!this.loaded) {
            wrapper.innerHTML = "Loading connections ...";
            wrapper.className = "dimmed light small";
            return wrapper;
        }

        // add iframes
        for (var i = 0; i < this.config.frames.length; i++) {

            // initialize iframe
            var iframe = document.createElement("iframe")
            iframe.id = "HOYMILES-" + this.config.ident + "-" + i;
            iframe.className = "hoymiles module";
            iframe.style.width = this.config.width;
            iframe.style.height = this.config.height;
            iframe.style.border = "none";
            iframe.style.overflow = "hidden";
            iframe.style.backgroundColor = this.config.backgroundColor;
            iframe.style.color = this.config.color;
            iframe.scrolling = "no";

            // depending on info given we need to set different src
            if (this.config.frames[i].src !== undefined) {
                iframe.src = this.config.frames[i].src;
            } else if (this.config.frames[i].html !== undefined) {
                iframe.src = '/' + iframe.id;
            } else {
                console.log("Error: frame " + i + " has neither src nor html.");
                wrapper.innerHTML = "<h1>Frame " + i + " has neither src nor html.</h1>";
                return wrapper;
            }
            wrapper.appendChild(iframe);
        }
        // done
        return wrapper;
    },

    suspend: function() {
        var doms = document.getElementsByClassName("hoymiles")
        if (doms.length > 0) {
            for (let dom of doms) {
                dom.style.display = "none"
            }
        }
    },

    resume: function() {
        var doms = document.getElementsByClassName("hoymiles")
        if (doms.length > 0) {
            for (let dom of doms) {
                dom.style.display = "block"
            }
        }
    },

    socketNotificationReceived: function(notification, payload) {
        if (notification === "INIT_DONE") {
            this.loaded = true;
            this.updateDom(); // update page
            this.scheduleUpdate(); // start update schedule
        }
    }
})
