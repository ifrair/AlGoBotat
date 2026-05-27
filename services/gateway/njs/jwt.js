/**
 * JWT verification module for nginx njs.
 *
 * Validates HS256 JWTs using a shared secret from environment variable.
 * The secret is loaded at nginx startup via env JWT_SECRET.
 *
 * Usage in nginx.conf:
 *   js_import /etc/nginx/njs/jwt.js;
 *   js_set $jwt_payload jwt_verify_token;
 *   js_set $jwt_user_id jwt_get_user_id;
 */

// Base64url decode (RFC 4648 §5)
function base64url_decode(str) {
    // Replace URL-safe characters and add padding
    str = str.replace(/-/g, '+').replace(/_/g, '/');
    while (str.length % 4) {
        str += '=';
    }
    try {
        return Buffer.from(str, 'base64').toString('utf8');
    } catch (e) {
        return null;
    }
}

// HMAC-SHA256 signature verification using njs crypto
function hmac_sha256_verify(data, signature_b64url, secret) {
    try {
        var crypto = require('crypto');
        var expected_sig = crypto.createHmac('sha256', secret)
            .update(data)
            .digest('base64');

        // Convert expected signature to base64url
        expected_sig = expected_sig.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

        // Constant-time comparison
        if (expected_sig.length !== signature_b64url.length) {
            return false;
        }
        var result = 0;
        for (var i = 0; i < expected_sig.length; i++) {
            result |= expected_sig.charCodeAt(i) ^ signature_b64url.charCodeAt(i);
        }
        return result === 0;
    } catch (e) {
        return false;
    }
}

/**
 * Verifies the JWT from the Authorization header.
 * Returns the decoded payload as a JSON string on success, or "0" on failure.
 */
function jwt_verify_token(r) {
    var auth_header = r.headersIn['Authorization'];
    if (!auth_header) {
        return "0";
    }

    // Expect "Bearer <token>"
    var parts = auth_header.split(' ');
    if (parts.length !== 2 || parts[0] !== 'Bearer') {
        return "0";
    }

    var token = parts[1];
    var token_parts = token.split('.');
    if (token_parts.length !== 3) {
        return "0";
    }

    var header_b64url  = token_parts[0];
    var payload_b64url = token_parts[1];
    var signature_b64url = token_parts[2];

    // Decode header to check algorithm
    var header_json = base64url_decode(header_b64url);
    if (!header_json) {
        return "0";
    }

    var header;
    try {
        header = JSON.parse(header_json);
    } catch (e) {
        return "0";
    }

    // We only support HS256
    if (header.alg !== 'HS256') {
        return "0";
    }

    // Get secret from environment variable
    var secret = process.env.JWT_SECRET;
    if (!secret) {
        r.error('JWT_SECRET environment variable is not set');
        return "0";
    }

    // Verify signature
    var signing_input = header_b64url + '.' + payload_b64url;
    if (!hmac_sha256_verify(signing_input, signature_b64url, secret)) {
        return "0";
    }

    // Decode payload
    var payload_json = base64url_decode(payload_b64url);
    if (!payload_json) {
        return "0";
    }

    var payload;
    try {
        payload = JSON.parse(payload_json);
    } catch (e) {
        return "0";
    }

    // Check expiration
    var now = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < now) {
        return "0";
    }

    // Check not before
    if (payload.nbf && payload.nbf > now) {
        return "0";
    }

    return JSON.stringify(payload);
}

/**
 * Extracts user_id from the verified JWT payload.
 */
function jwt_get_user_id(r) {
    var payload_str = jwt_verify_token(r);
    if (payload_str === "0") {
        return "";
    }
    try {
        var payload = JSON.parse(payload_str);
        return payload.user_id ? String(payload.user_id) : "";
    } catch (e) {
        return "";
    }
}

/**
 * Extracts role from the verified JWT payload.
 */
function jwt_get_role(r) {
    var payload_str = jwt_verify_token(r);
    if (payload_str === "0") {
        return "";
    }
    try {
        var payload = JSON.parse(payload_str);
        return payload.role ? String(payload.role) : "USER";
    } catch (e) {
        return "";
    }
}

/**
 * Validates admin credentials from Basic Auth against ADMIN_LOGIN/ADMIN_PASSWORD env vars.
 * Returns "1" if valid, "0" if invalid.
 */
function validate_admin(r) {
    var auth_header = r.headersIn['Authorization'];
    if (!auth_header) {
        return "0";
    }

    // Expect "Basic <base64>"
    var parts = auth_header.split(' ');
    if (parts.length !== 2 || parts[0] !== 'Basic') {
        return "0";
    }

    // Decode base64 credentials
    var decoded;
    try {
        decoded = Buffer.from(parts[1], 'base64').toString('utf8');
    } catch (e) {
        return "0";
    }

    // Split into login:password
    var colon_pos = decoded.indexOf(':');
    if (colon_pos === -1) {
        return "0";
    }

    var login = decoded.substring(0, colon_pos);
    var password = decoded.substring(colon_pos + 1);

    // Get admin credentials from environment variables
    var admin_login = process.env.ADMIN_LOGIN;
    var admin_password = process.env.ADMIN_PASSWORD;

    if (!admin_login || !admin_password) {
        r.error('ADMIN_LOGIN or ADMIN_PASSWORD environment variable is not set');
        return "0";
    }

    // avoid oversize string attack
    if (login.length !== admin_login.length) {
        return "0";
    }
    var result = 0;
    for (var i = 0; i < login.length; i++) {
        result |= login.charCodeAt(i) ^ admin_login.charCodeAt(i);
    }

    if (password.length !== admin_password.length) {
        return "0";
    }
    for (var j = 0; j < password.length; j++) {
        result |= password.charCodeAt(j) ^ admin_password.charCodeAt(j);
    }

    return result === 0 ? "1" : "0";
}

// Export functions for nginx
export default {jwt_verify_token, jwt_get_user_id, jwt_get_role, validate_admin};