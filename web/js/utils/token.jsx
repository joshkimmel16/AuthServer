const crypto = require('crypto-js');

//jwt: JSON web token as string
//secret: application secret as string
//alg: algorithm used for encryption by application as string
function decryptToken (jwt, secret, alg) {
    var parts = jwt.split('.');
    if (parts.length !== 3) {
        throw {code: -1, message: "Invalid JWT! Does not contain 3 components."};
    }
    var comps = {header: parts[0], payload: parts[1], signature: parts[2]};
    
    //check that signature is valid
    var check = true;
    if (alg === "HMAC") {
        var sigCheck = b64Encode(encryptHmac(comps.header + '.' + comps.payload, secret), true);
        check = (sigCheck === comps.signature);
    }
    else {
        throw {code: -3, message: "Unrecognized algorithm provided for encryption!"};
    }
    
    //if valid, return header and payload
    if (check === true) {
        return {header: JSON.parse(b64Decode(comps.header)), payload: JSON.parse(b64Decode(comps.payload))};
    }
    else {
        throw {code: -2, message: "The given JWT's signature could not be validated!"};
    }
}

//msg: string to be encrypted
//secret: string of secret
function encryptHmac (msg, secret) {
    return crypto.HmacSHA256(msg, secret);
}

//input: unencoded string OR WordArray
//inWords: boolean for whether the input needs to be converted to Word array first
function b64Encode (input, inWords) {
    var words = (inWords ? input : crypto.enc.Utf8.parse(input));
    return crypto.enc.Base64.stringify(words);
}

//input: Base64-encoded string OR WordArray
//inWords: boolean for whether the input needs to be converted to Word array first
function b64Decode (input, inWords) {
    var words = (inWords ? input : crypto.enc.Base64.parse(input));
    return crypto.enc.Utf8.stringify(words);
}

//FOR TESTING
var secret = "h0XlcL5KFX0eU8b9a92mht5dChFALIECEUC9Fb21t3hhIMEuUbDHh14X4TEj7r9UAdHKLWqO1MnZuTGQYQcTPT6VG7lkWAHP1h6SZYxONv/yoUDXsopN5XnZoEh3VSc14z23xw==";
var jwt = "eyJ0eXBlIjogImp3dCIsICJhbGciOiAiSFMyNTYifQ==.eyJleHAiOiAiNC8yNy8yMDE4IDE0OjY6MzgiLCAidXNlcmlkIjogMSwgInVzZXJuYW1lIjogImpvc2gua2ltbWVsIiwgInVzZXJtZXRhZGF0YSI6IHsiZW1haWwiOiAiam9zaC5raW1tZWxAbGFzZXJmaWNoZS5jb20ifX0=.ZXlKMGVYQmxJam9nSW1wM2RDSXNJQ0poYkdjaU9pQWlTRk15TlRZaWZRPT0uZXlKbGVIQWlPaUFpTkM4eU55OHlNREU0SURFME9qWTZNemdpTENBaWRYTmxjbWxrSWpvZ01Td2dJblZ6WlhKdVlXMWxJam9nSW1wdmMyZ3VhMmx0YldWc0lpd2dJblZ6WlhKdFpYUmhaR0YwWVNJNklIc2laVzFoYVd3aU9pQWlhbTl6YUM1cmFXMXRaV3hBYkdGelpYSm1hV05vWlM1amIyMGlmWDA9";
var alg = "HMAC";

var result = decryptToken(jwt, secret, alg);
console.log(result);