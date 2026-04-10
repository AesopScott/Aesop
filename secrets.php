<?php

/**
 * AESOP secret loading helpers.
 *
 * Secrets are resolved in this order:
 * 1. Environment variable
 * 2. secrets.local.php return array
 * 3. Default value (if provided)
 */

$aesopLocalSecrets = [];
$aesopLocalSecretsFile = __DIR__ . '/secrets.local.php';
if (file_exists($aesopLocalSecretsFile)) {
    $loaded = require $aesopLocalSecretsFile;
    if (is_array($loaded)) {
        $aesopLocalSecrets = $loaded;
    }
}

function aesop_secret($key, $default = null) {
    global $aesopLocalSecrets;

    $env = getenv($key);
    if ($env !== false && $env !== '') {
        return $env;
    }

    if (array_key_exists($key, $aesopLocalSecrets) && $aesopLocalSecrets[$key] !== '') {
        return $aesopLocalSecrets[$key];
    }

    return $default;
}

function aesop_require_secret($key) {
    $value = aesop_secret($key);
    if ($value === null || $value === '') {
        throw new RuntimeException('Missing required secret: ' . $key);
    }
    return $value;
}
