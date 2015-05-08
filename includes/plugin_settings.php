<?php

$allowed_plugins = array(
    'atoms',
    'atomscan',
    'callbacks',
    'clipboard',
    'cmdscan',
    'consoles',
    'dlldump',
    'dlllist',
    'driverscan',
    'envars',
    'filescan',
    'gahti',
    'gditimers',
    'gdt',
    'getservicesids',
    'getsids',
    'handles',
    'hivelist',
    'idt',
    'joblinks',
    'ldrmodules',
    'netscan',
    'memmap',
    'modscan',
    'modules',
    'mutantscan',
    'objtypescan',
    'prefetchparser',
    'privs',
    'procdump',
    'pslist',
    'psscan',
    'pstree',
    'psxview',
    'shimcache',
    'sockets',
    'sockscan',
    'ssdt',
    'symlinkscan',
    'thrdscan',
    'timers',
    'unloadmodules',
    'userhandles',
    'vadwalk');

if (isset($_GET['name']) && !empty($_GET['name'])) {
    $plugin = filter_input(INPUT_GET, 'name', FILTER_SANITIZE_STRING);
} else {
    $plugin = 'NON-EMPTY-STRING';
}

function plugin_submenu($plugin, $x = 0) {
    global $allowed_plugins;
    if ($x) {
        echo '<li class="active">&nbsp;&nbsp;&nbsp;&nbsp;<a href="search.php">Search</a></li>';
    } else {
        echo '<li>&nbsp;&nbsp;&nbsp;&nbsp;<a href="search.php">Search</a></li>';
    }
    $filename = $_SESSION['dump']['location'].'-mactime.txt';
    if (file_exists($filename)) {
        echo '<li>&nbsp;&nbsp;&nbsp;&nbsp;<a href="download.php" target="_blank">Download timeline</a><br />&nbsp;&nbsp;&nbsp;&nbsp;(CSV format, .txt)</li>';
    }
    if ($_SERVER['SCRIPT_NAME'] == '/selected.php') {
    echo '<li class="active">&nbsp;&nbsp;&nbsp;&nbsp;<a href="selected.php">Custom selections</a></li>';
    }
    else {
        echo '<li>&nbsp;&nbsp;&nbsp;&nbsp;<a href="selected.php">Custom selections</a></li>';
    }
    echo '<hr />';
    foreach ($allowed_plugins as $name) {
        if ($name == $plugin) {
            $xtra = ' class="active"';
        } else {
            $xtra = '';
        }
        echo '<li' . $xtra . '><a href="plugin.php?name=' . $name . '">' . $name . '</a></li>';
    }
}

function plugin_include($plugin) {
    if (file_exists('./includes/plugins/' . $plugin . '.php')) {
        include('./includes/plugins/' . $plugin . '.php');
    } else {
        echo '<h5>No suitable template for this plugin yet.</h5>';
    }
}

?>