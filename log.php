<?php
session_start();
?>
<pre>
    <?php
    $log = file_get_contents('/home/solvent/lobotomy.log');
    echo $log;
    ?>
</pre>
