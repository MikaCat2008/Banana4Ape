// [SECTION VARS BEGIN]
let m_ticks = 0, 
    m_last_ticks = 0,
    m_game_canvas_element = null, 
    m_requestAnimationFrame = window.requestAnimationFrame;
// [SECTION VARS END]



// [SECTION API BEGIN]

// [SECTION API END]



// [SECTION INIT BEGIN]

setInterval(() => {
    console.log(`${m_ticks - m_last_ticks} UPS`);

    m_last_ticks = m_ticks;
}, 1000);

window.requestAnimationFrame = rt => {
    // eo_clientX = window.innerWidth / 2 + Math.sin(m_ticks / 5) * 200;
    // eo_clientY = window.innerHeight / 2 + Math.cos(m_ticks / 5) * 200;

    if (eo_ui_is_active != eo_last_ui_is_active)
    {
        if (eo_ui_is_active)
            uimm_menu_show();
        else 
            uimm_menu_hide();
    }

    eo_update();

    m_ticks++;

    return m_requestAnimationFrame(rt);
};

document.addEventListener("DOMContentLoaded", () => {    
    m_game_canvas_element = document.querySelector("#game-canvas");
});
// [SECTION INIT END]
