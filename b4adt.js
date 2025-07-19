// ==UserScript==
// @name         Banana4Ape data transfer
// @namespace    http://tampermonkey.net/
// @version      18.07.25
// @description  try to take over the world!
// @author       APES_COMMUNITY
// @match        https://apes.io/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=apes.io
// @grant        none
// @run-at       document-start
// ==/UserScript==


function modInverse(a, m) {
    let m0 = m,
        x0 = BigInt(0), x1 = BigInt(1),
        q = BigInt(0), t = BigInt(0);

    if (m === 1) return 0;

    while (a > 1) {
        q = a / m;
        t = m;

        m = a % m;
        a = t;
        t = x0;

        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0) {
        x1 += m0;
    }

    return x1;
}


const MOD = 2n ** 128n;
const KEY = 0x1F123AB1_AB428BA5_BF123BC1_4A7273BDn;
const IKEY = modInverse(KEY, MOD);

window.SYMBOLS = {
    1: 'а', 2: 'б', 3: 'в', 4: 'г', 5: 'д',
    6: 'е', 7: 'ё', 8: 'ж', 9: 'з', 10: 'и',
    11: 'й', 12: 'к', 13: 'л', 14: 'м', 15: 'н',
    16: 'о', 17: 'п', 18: 'р', 19: 'с', 20: 'т',
    21: 'у', 22: 'ф', 23: 'х', 24: 'ц', 25: 'ч',
    26: 'ш', 27: 'щ', 28: 'ъ', 29: 'ы', 30: 'ь',
    31: 'э', 32: 'ю', 33: 'я', 34: ' ', 35: ',',
    36: '.', 37: '?', 38: 'a', 39: 'b', 40: 'c',
    41: 'd', 42: 'e', 43: 'f', 44: 'g', 45: 'h',
    46: 'i', 47: 'j', 48: 'k', 49: 'l', 50: 'm',
    51: 'n', 52: 'o', 53: 'p', 54: 'q', 55: 'r',
    56: 's', 57: 't', 58: 'u', 59: 'v', 60: 'w',
    61: 'x', 62: 'y', 63: 'z'
}
window.ISYMBOLS = {
    'а': 1, 'б': 2, 'в': 3, 'г': 4, 'д': 5,
    'е': 6, 'ё': 7, 'ж': 8, 'з': 9, 'и': 10,
    'й': 11, 'к': 12, 'л': 13, 'м': 14, 'н': 15,
    'о': 16, 'п': 17, 'р': 18, 'с': 19, 'т': 20,
    'у': 21, 'ф': 22, 'х': 23, 'ц': 24, 'ч': 25,
    'ш': 26, 'щ': 27, 'ъ': 28, 'ы': 29, 'ь': 30,
    'э': 31, 'ю': 32, 'я': 33, ' ': 34, ',': 35,
    '.': 36, '?': 37, 'a': 38, 'b': 39, 'c': 40,
    'd': 41, 'e': 42, 'f': 43, 'g': 44, 'h': 45,
    'i': 46, 'j': 47, 'k': 48, 'l': 49, 'm': 50,
    'n': 51, 'o': 52, 'p': 53, 'q': 54, 'r': 55,
    's': 56, 't': 57, 'u': 58, 'v': 59, 'w': 60,
    'x': 61, 'y': 62, 'z': 63
}

window.mtREQUEST_CLIENT_ID = 0
window.mtSEND_MESSAGE = 1
window.mtCONTINUE_BOD = 2

window.rtRET_CLIENT_ID = 0
window.rtCONTINUE_BOD = 1

window.csNONE = 0
window.csSEND_MESSAGE = 1

let last_b4a = null,
    apes_data_sender_img = null,
    client_id = null,
    client_hook = null,
    client_status = null,
    send_message_text = null,
    send_message_start = null;


window.b4a_encode = function(b4a) {
    let i4 = 0,
        i128 = ((b4a + 1n) * KEY) % MOD,
        data_list = new Array(32).fill("");

    for (let i = 0n; i < 32; i++) {
        i4 = Number(i128 >> 4n * i & 0xFn);
        data_list[i] = String.fromCharCode(97 + i4);
    }

    let data = data_list.join("");

    return `b4a_${data.slice(0, 8)}_${data.slice(8, 14)}_${data.slice(14, 16)}_${data.slice(16, 18)}_${data.slice(18, 24)}_${data.slice(24, 32)}`;
}

window.b4a_decode = function(data) {
    let i4 = 0,
        i128 = 0n,
        data_list = [];

    for (let i = 0; i < data.length; i++) {
        if (i > 3 && data[i] != "_") {
            data_list.push(data[i]);
        }
    }

    for (let i = 0n; i < 32; i++) {
        i4 = data_list[i].codePointAt(0) - 97;
        i128 |= BigInt(i4) << 4n * i;
    }

    return (i128 * IKEY) % MOD - 1n;
}

window.b4a_get = function(b4a, index, size) {
    return (b4a >> BigInt(index)) % 2n ** BigInt(size);
}

window.b4a_set = function(b4a, index, size, value) {
    index = BigInt(index);
    size = BigInt(size);
    value = BigInt(value);

    b4a &= ((((1n << (128n - index - size)) - 1n) << (index + size)) | ((1n << index) - 1n));

    return b4a | (value % 2n ** size) << index;
}

window.bod_from_i6_text = function(i6_text, start) {
    let is_finished = i6_text.length - start <= 19,
        bod = 0n,
        index = 0;

    for (let i = 0; i < 19; i++) {
        index = start + i;

        if (index == i6_text.length) break;

        bod |= BigInt(ISYMBOLS[i6_text[index]]) << BigInt(i) * 6n;
    }

    return [bod, is_finished];
}

window.send_b4a = function(b4a) {
    let img = null;

    if (window.apes_data_sender_img == null) {
        img = document.createElement("img");

        window.apes_data_sender_img = img;
        document.body.appendChild(img);
    }
    else {
        img = window.apes_data_sender_img
    }

    img.src = `https://api.telegram.org/bot7575372807:AAH0_k32mucCg_ln9ecIuDuhhtehwCNfD74/sendMessage?chat_id=7644893879&text=${b4a_encode(b4a)}`;
}

window.request_client_id = async function() {
    client_hook = Math.floor(Math.random() * 2 ** 32);

    let b4a = b4a_set(0n, 0, 3, mtREQUEST_CLIENT_ID);
    b4a = b4a_set(b4a, 3, 32, client_hook);

    await send_b4a(b4a);
}

window.send_message = async function(text) {
    client_status = csSEND_MESSAGE;
    send_message_text = text;
    send_message_start = 0;

    let [bod, is_finished] = bod_from_i6_text(text, 0);

    let b4a = b4a_set(0n, 0, 3, mtSEND_MESSAGE);
    b4a = b4a_set(b4a, 3, 8, client_id);
    b4a = b4a_set(b4a, 11, 1, is_finished);
    b4a = b4a_set(b4a, 12, 114, bod);

    await send_b4a(b4a);
}

window.continue_bod = async function() {
    let b4a = null;

    if (client_status == csSEND_MESSAGE) {
        send_message_start += 19;

        let [bod, is_finished] = bod_from_i6_text(send_message_text, send_message_start);

        b4a = b4a_set(0n, 0, 3, mtCONTINUE_BOD);
        b4a = b4a_set(b4a, 3, 8, client_id);
        b4a = b4a_set(b4a, 11, 1, is_finished);
        b4a = b4a_set(b4a, 12, 114, bod);

        if (is_finished) {
            client_status = csNONE;
            send_message_text = null;
            send_message_start = null;
        }
    }

    await send_b4a(b4a);
}


function on_update(b4a_i384) {
    let return_type = b4a_i384_get(b4a_i384, 2, 3);

    if (return_type == rtSET_CLIENT_ID) {
        let r_client_hook = b4a_i384_get(b4a_i384, 5, 32);

        if (client_hook == r_client_hook) {
            client_id = b4a_i384_get(b4a_i384, 37, 8);
        }
    }
    else {
        let r_client_id = b4a_i384_get(b4a_i384, 5, 8),
            b4a_i384 = null;

        if (client_id != r_client_id) return;

        if (return_type == rtSTART_DATA_TRANSFER) {
            ready_for_data_transfer();

            b4a_i384 = b4a_i384_set(0n, 0, 3, mtREADY_FOR_DATA_TRANSFER);
            b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
            send_b4a_i384(b4a_i384);
        }
        else if (return_type == rtSEND_DATA) {
            b4a_i384 = b4a_i384_set(0n, 0, 3, mtGOT_DATA);
            b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
            send_b4a_i384(b4a_i384);
        }
        else if (return_type == rtSTOP_DATA_TRANSFER) {
            console.log("stop_data_transfer lol")
        }
    }
}

(async function() {
    let response = null,
        b4a_i384 = null,
        b4a_i384_encoded = null,
        last_b4a_i384_encoded = null;

    while (true) {
        response = await fetch("https://apes.io/leaders/part?waves=false&page=0&range=30");
        b4a_i384_encoded = (await response.text()).match(/b4a_[a-zA-Z0-9()]{64}/)[0];
        b4a_i384 = b4a_i384_decode(b4a_i384_encoded);

        if (b4a_i384 != last_b4a_i384) {
            on_update();

            last_b4a_i384 = b4a_i384;
        }
    }
})()
