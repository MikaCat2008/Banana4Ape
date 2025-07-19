// [SECTION VARS BEGIN]
let uimm_menu_element = null;
// [SECTION VARS END]



// [SECTION API BEGIN]

function uimm_menu_create_styles() {
    uimm_menu_styles = document.createElement("style");
    uimm_menu_styles.innerHTML = // [LOAD "src/ui/uimm_styles.css"];

    document.head.appendChild(uimm_menu_styles);
}

function uimm_menu_create_element() {
    uimm_menu_element = document.createElement("div");
    uimm_menu_element.innerHTML = // [LOAD "src/ui/uimm_template.html"];
 
    document.body.appendChild(uimm_menu_element);
}

function uimm_menu_show() {
    uimm_menu_element.style.display = "block";
}

function uimm_menu_hide() {
    uimm_menu_element.style.display = "none";
}

// [SECTION API END]



// [SECTION INIT BEGIN]

document.addEventListener("DOMContentLoaded", () => {    
    uimm_menu_create_styles();
    uimm_menu_create_element();
});

// [SECTION INIT END]
