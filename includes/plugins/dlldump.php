<?php session_start(); ?>
<div class="msg_box msg_alert"><strong>Clicking on a hash will submit the clicked hash to VirusTotal!</strong></div>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, process, name, modulebase, modulename, md5, filename, fullfilename FROM dlldump";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Process</div>
</th>
<th>
<div class="th_wrapp">Name</div>
</th>
<th>
<div class="th_wrapp">Modulebase</div>
</th>
<th>
<div class="th_wrapp">Modulename</div>
</th>
<th>
<div class="th_wrapp">MD5</div>
</th>
<th>
<div class="th_wrapp">Exported filename</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    $bad = False;
    while ($row = mysql_fetch_assoc($result)) {
        if ($row['md5'] == "0") {
            $row['md5'] = '-';
        } else {
            if (is_bad_hash($row['md5'])) {
                $bad = True;
            }
            $row['md5'] = '<a href="https://www.virustotal.com/en/search/?query=' . $row['md5'] . '" target="_blank">' . $row['md5'] . '</a>&nbsp;&nbsp;<img src="./images/icons/alert2.png" title="This will upload the hash to VirusTotal!" alt="This will upload the hash to VirusTotal!" />';
        }
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND row_id=" . $row['id'];
        $_result = mysql_query($_query);
        $_row = mysql_fetch_assoc($_result);
        $filter = apply_filter($row);
        $class = "";
        if (count($filter) > 0) {
            foreach ($filter as $output) {
                $class .= " filter_" . $output;
            }
        }
        ?>
        <tr id="<?php echo $row['id']; ?>" class="<?php echo $class;
    if ($_row['marked']) {
        echo ' marked';
    } ?>">
            <td><a href="./search.php?q=<?php echo $row['process']; ?>"><?php echo $row['process']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['name']; ?>"><?php echo $row['name']; ?></a></td>
            <td><?php echo $row['modulebase']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['modulename']; ?>"><?php echo $row['modulename']; ?></a></td>
            <td<?php if ($bad) { ?> class='bad_hash'<?php } ?>><p><?php echo $row['md5']; ?></p></td>
            <td><a href="plugin.php?name=xxd&ID=<?php echo $row['id']; ?>&plugin=dlldump"><?php echo $row['filename']; ?></a></td>
        </tr>
        <?php
        $bad = False;
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>