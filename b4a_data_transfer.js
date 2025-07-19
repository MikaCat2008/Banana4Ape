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


function mod_inverse(a, m) {
    let m0 = m,
        x0 = 0n, x1 = 1n,
        q = 0n, t = 0n;

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


const MOD_i384 = 2n ** 384n;
const KEY_i384 = 0xFF9594D0AF596B4CD9AF4D7BB0FD5D75BB4385394C89D7A657A1F7CE34522B7AAE68F22B8AD89C66BAB0FF39522126E7n;
const IKEY_i384 = mod_inverse(KEY_i384, MOD_i384);

const b4a_i384_symbols = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e',
    5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
    10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o',
    15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't',
    20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y',
    25: 'z', 26: 'A', 27: 'B', 28: 'C', 29: 'D',
    30: 'E', 31: 'F', 32: 'G', 33: 'H', 34: 'I',
    35: 'J', 36: 'K', 37: 'L', 38: 'M', 39: 'N',
    40: 'O', 41: 'P', 42: 'Q', 43: 'R', 44: 'S',
    45: 'T', 46: 'U', 47: 'V', 48: 'W', 49: 'X',
    50: 'Y', 51: 'Z', 52: '0', 53: '1', 54: '2',
    55: '3', 56: '4', 57: '5', 58: '6', 59: '7',
    60: '8', 61: '9', 62: '(', 63: ')'
};
const b4a_i384_inv_symbols = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
    'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
    'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29,
    'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34,
    'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39,
    'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44,
    'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49,
    'Y': 50, 'Z': 51, '0': 52, '1': 53, '2': 54,
    '3': 55, '4': 56, '5': 57, '6': 58, '7': 59,
    '8': 60, '9': 61, '(': 62, ')': 63
};

const mtSTART_DATA_TRANSFER = 0;
const mtSEND_DATA = 1;
const mtSTOP_DATA_TRANSFER = 2;
const mtREADY_FOR_DATA_TRANSFER = 3;
const mtGOT_DATA = 4;

const rtSET_CLIENT_ID = 0;
const rtSTART_DATA_TRANSFER = 1;
const rtSEND_DATA = 2;
const rtSTOP_DATA_TRANSFER = 3;

window.client_id = null;
window.client_hook = null;

let b4a_i384_recv_list = null,
    apes_data_sender_img = null,
    start_data_transfer_resolve = null;


window.b4a_i384_encode = function(b4a_i384) {
    let i6 = 0,
        i384 = ((b4a_i384 + 1n) * KEY_i384) % MOD_i384,
        symbols = [];

    for (let i = 0n; i < 64; i++) {
        i6 = i384 >> 6n * i & (2n ** 6n - 1n);
        symbols.push(b4a_i384_symbols[i6]);
    }

    return `b4a_${symbols.join("")}`;
}

window.b4a_i384_decode = function(b4a_i384_encoded) {
    let i6 = 0,
        i384 = 0n,
        symbol = null;

    for (let i = 0n; i < 64; i++) {
        symbol = b4a_i384_encoded[i + 4n];

        i6 = b4a_i384_inv_symbols[symbol];
        i384 |= BigInt(i6) << 6n * i;
    }

    return (i384 * IKEY_i384) % MOD_i384 - 1n;
}

window.b4a_i384_get = function(b4a_i384, index, size) {
    return (b4a_i384 >> BigInt(index)) % 2n ** BigInt(size);
}

window.b4a_i384_set = function(b4a_i384, index, size, value) {
    index = BigInt(index);
    size = BigInt(size);
    value = BigInt(value);

    b4a_i384 &= ((((1n << (384n - index - size)) - 1n) << (index + size)) | ((1n << index) - 1n));

    return b4a_i384 | (value % 2n ** size) << index;
}

window.send_b4a_i384 = function(b4a_i384) {
    let img = null;

    if (apes_data_sender_img == null) {
        img = document.createElement("img");

        apes_data_sender_img = img;
        document.body.appendChild(img);
    }
    else {
        img = apes_data_sender_img
    }

    img.src = `https://api.telegram.org/bot7575372807:AAH0_k32mucCg_ln9ecIuDuhhtehwCNfD74/sendMessage?chat_id=7644893879&text=${b4a_i384_encode(b4a_i384)}`;
}

window.start_data_transfer = async function() {
    let b4a_i384 = 0n;

    window.client_hook = Math.floor(Math.random() * 2 ** 32);

    b4a_i384 = b4a_i384_set(b4a_i384, 0, 3, 0);
    b4a_i384 = b4a_i384_set(b4a_i384, 3, 32, client_hook);
    send_b4a_i384(b4a_i384);

    await new Promise(resolve => {
        start_data_transfer_resolve = resolve;
    });
}

window.send_data = async function(b4a_i384) {
    b4a_i384 = b4a_i384_set(b4a_i384, 0, 3, 1);
    b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
    send_b4a_i384(b4a_i384);

    await new Promise(resolve => {
        setTimeout(resolve, 500);
    });
}

window.stop_data_transfer = function() {
    let b4a_i384 = 0n;

    b4a_i384 = b4a_i384_set(b4a_i384, 0, 3, 2);
    b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
    send_b4a_i384(b4a_i384);
}


// DEAD

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

// DEAD


async function on_update(b4a_i384) {
    let return_type = b4a_i384_get(b4a_i384, 2, 3);

    if (return_type == rtSET_CLIENT_ID) {
        let r_client_hook = b4a_i384_get(b4a_i384, 5, 32);

        if (client_hook == r_client_hook) {
            window.client_id = b4a_i384_get(b4a_i384, 37, 8);

            start_data_transfer_resolve();
        }
    }
    else {
        let r_client_id = b4a_i384_get(b4a_i384, 5, 8);

        if (client_id != r_client_id) return;

        if (return_type == rtSTART_DATA_TRANSFER) {
            b4a_i384_recv_list = [];

            b4a_i384 = b4a_i384_set(0n, 0, 3, mtREADY_FOR_DATA_TRANSFER);
            b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
            send_b4a_i384(b4a_i384);

            console.log("start data transfer");
        }
        else if (return_type == rtSEND_DATA) {
            b4a_i384_recv_list.push(b4a_i384);

            b4a_i384 = b4a_i384_set(0n, 0, 3, mtGOT_DATA);
            b4a_i384 = b4a_i384_set(b4a_i384, 3, 8, client_id);
            send_b4a_i384(b4a_i384);

            console.log("got data");
        }
        else if (return_type == rtSTOP_DATA_TRANSFER) {
            for (let i = 0; i < 8; i++) {
                b4a_i384 = b4a_i384_recv_list[i];

                console.log(b4a_i384_get(b4a_i384, 13, 32));
            }

            b4a_i384_recv_list = null;

            console.log("stop data transfer");
        }
    }
}

(async function() {
    let response = null,
        b4a_i384 = null,
        last_b4a_i384 = null,
        b4a_i384_encoded = null;

    while (true) {
        response = await fetch("https://apes.io/leaders/part?waves=false&page=0&range=30");
        b4a_i384_encoded = (await response.text()).match(/b4a_[a-zA-Z0-9()]{64}/)[0];
        b4a_i384 = b4a_i384_decode(b4a_i384_encoded);

        if (b4a_i384 != last_b4a_i384) {
            on_update(b4a_i384);

            last_b4a_i384 = b4a_i384;
        }
    }
})()
