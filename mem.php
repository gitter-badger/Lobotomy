<?php
session_start();
?>
<pre>
    <?php
    error_reporting(-1);
    $command = escapeshellcmd('vol.py -f /dumps/stuxnet.vmem imageinfo');
    $output = shell_exec($command);
    $arr = preg_split('/\n|\r\n?/', $output);
    var_dump($arr);
    ?>
</pre>