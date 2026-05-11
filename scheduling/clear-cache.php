<?php
// Clear OPcache if available
if (function_exists('opcache_reset')) {
    opcache_reset();
    echo "OPcache cleared\n";
}

// Clear APCu if available
if (function_exists('apcu_clear_cache')) {
    apcu_clear_cache();
    echo "APCu cleared\n";
}

echo "Cache clearing attempt completed\n";
echo "If errors persist, restart PHP via cPanel\n";
?>
