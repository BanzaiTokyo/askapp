var token_field;
function generateUID(length)
{
    return window.btoa(Array.from(window.crypto.getRandomValues(new Uint8Array(length * 2))).map((b) => String.fromCharCode(b)).join("")).replace(/[+/]/g, "").substring(0, length);
}
jQuery(document).ready(function() {
    token_field = window.django.jQuery('#id_token-0-key')
    token_field.after('<button onclick="token_field.val(generateUID(40)); return false">Generate new</button>')
})