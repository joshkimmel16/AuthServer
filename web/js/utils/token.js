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
        var sigCheck = b64Encode(encryptHmac(comps.header + '.' + comps.payload, secret));
        debugger;
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
//SEEMS LIKE THE OUTPUT OF THIS DOES NOT MATCH THE OUTPUT OF THE PYTHON ENCRYPTION FUNCTION!!! LOOKS LIKE THE SPECIFIC ISSUE IS THAT APPLICATION SECRETS DO NOT CONFORM TO VALID UTF8 STANDARDS AND JAVASCRIPT DOES NOT ACCEPT BYTES AS INPUTS. NOT SURE HOW TO FIX THIS ONE....
function encryptHmac (msg, secret) {
    //return crypto.HmacSHA256(msg, secret);
    return crypto.HmacSHA256(msg, secret).toString(crypto.enc.Hex);
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
var s1 = "yYvItsOW4ZuPw7fGqcSC4rGlyL/Gp+GausOHx6bhm5k0xpDFkOGblmjGjsiGwrvisaHGojrCquGbiMOBwrzCtsOLyYXhmr/Ik0ThmrnHjcaew5/Oh8iVxKXEncOP4Zqgx6Bv4Zulw6/CpeKxt3sjx4/Gn8Sn4Zuqx5TGjMOUw6HHnMi0OcKjSsWwyYXHg8Sz4Zus4ZqzyKvhmqXhm6Xhm4XGgOKxo8O/xZnhmq/GseKxvuGbmMazdMSWJca0w5XGvMWi4ZuM4Zq3yInFn+KxqMmI4Zq3xpA=";
var secret = b64Decode(s1);
var jwt = 'eyJ0eXBlIjogImp3dCIsICJhbGciOiAiSFMyNTYifQ==.eyJleHAiOiAiNC8yOS8yMDE4IDk6MjU6NTMiLCAidXNlcmlkIjogNCwgInVzZXJuYW1lIjogInNpZC50aGVraWQiLCAidXNlcm1ldGFkYXRhIjogeyJmaXJzdE5hbWUiOiAiU2lkbmV5IiwgImxhc3ROYW1lIjogIkNyb3NieSIsICJlbWFpbCI6ICJzaWR0aGVraWRAZ21haWwuY29tIiwgInJpZ2h0cyI6IDF9fQ==.ZXlKMGVYQmxJam9nSW1wM2RDSXNJQ0poYkdjaU9pQWlTRk15TlRZaWZRPT0uZXlKbGVIQWlPaUFpTkM4eU9TOHlNREU0SURrNk1qVTZOVE1pTENBaWRYTmxjbWxrSWpvZ05Dd2dJblZ6WlhKdVlXMWxJam9nSW5OcFpDNTBhR1ZyYVdRaUxDQWlkWE5sY20xbGRHRmtZWFJoSWpvZ2V5Sm1hWEp6ZEU1aGJXVWlPaUFpVTJsa2JtVjVJaXdnSW14aGMzUk9ZVzFsSWpvZ0lrTnliM05pZVNJc0lDSmxiV0ZwYkNJNklDSnphV1IwYUdWcmFXUkFaMjFoYVd3dVkyOXRJaXdnSW5KcFoyaDBjeUk2SURGOWZRPT0=';
var alg = "HMAC";

var result = decryptToken(jwt, secret, alg);
console.log(result);