// [SECTION VARS BEGIN]
let eo_clientX = 0, 
    eo_old_clientX = 0, 
    eo_clientY = 0, 
    eo_old_clientY = 0,
    eo_movementX = 0, 
    eo_movementY = 0,
    eo_ui_is_active = false,
    eo_last_ui_is_active = false;
// [SECTION VARS END]



// [SECTION API BEGIN]

function eo_update() {
    eo_last_ui_is_active = eo_ui_is_active;
 
    window.dispatchEvent(new PointerEvent("pointerrawupdate"));
}

// [SECTION API END]



// [SECTION INIT BEGIN]
Object.defineProperty(window, "onpointerrawupdate", {
    enumerable: true,
    configurable: true,
    set(handler) {
        console.log("[INJ] onpointerrawupdate");

        window.addEventListener("pointerrawupdate", event => {
            if (!event.isTrusted)
            {
                event.getCoalescedEvents = () => {
                    eo_movementX = Math.min(100, Math.max(-100, (eo_clientX - eo_old_clientX)));
                    eo_movementY = Math.min(100, Math.max(-100, (eo_clientY - eo_old_clientY)));
                    
                    eo_old_clientX += eo_movementX;
                    eo_old_clientY += eo_movementY;

                    return [{
                        clientX: eo_clientX, 
                        clientY: eo_clientY,
                        movementX: eo_movementX, 
                        movementY: eo_movementY
                    }];
                };
            };

            handler(event);
        });
    }
});

Object.defineProperty(document, "onkeydown", {
    enumerable: true,
    configurable: true,
    set(handler) {
        console.log("[INJ] onkeydown");

        document.addEventListener("keydown", event => {
            if (event.code == "ShiftRight")
                document.exitPointerLock();

            handler(event);
        });
    }
});

Object.defineProperty(document, "onpointerlockchange", {
    enumerable: true,
    configurable: true,
    set(handler) {
        console.log("[INJ] onpointerlockchange");

        document.addEventListener("pointerlockchange", event => {
            eo_ui_is_active = document.pointerLockElement == null;

            handler(event);
        });
    }
});

Object.defineProperty(document, "onmousedown", {
    enumerable: true,
    configurable: true,
    set(handler) {
        console.log("[INJ] onmousedown");

        document.addEventListener("mousedown", event => {
            if (event.target != m_game_canvas_element) return;

            handler(event);
        });
    }
});
// [SECTION INIT END]
