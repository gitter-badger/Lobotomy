<?php session_start(); ?>
<div class="msg_box msg_alert"><strong>Clicking on a hash will submit the clicked hash to VirusTotal!</strong></div>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, process, imagebase, name, result, md5, filename, fullfilename FROM procdump";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Process</div>
</th>
<th>
<div class="th_wrapp">ImageBase</div>
</th>
<th>
<div class="th_wrapp">Name</div>
</th>
<th>
<div class="th_wrapp">Result</div>
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
            <td><?php echo $row['process']; ?></td>
            <td><?php echo $row['imagebase']; ?></td>
            <td><?php echo $row['name']; ?></td>
            <td><?php echo $row['result']; ?></td>
            <td<?php if ($bad) { ?> class='bad_hash'<?php } ?>><?php echo $row['md5']; ?></td>
            <td><a href="plugin.php?name=xxd&ID=<?php echo $row['id']; ?>&plugin=procdump"><?php echo $row['filename']; ?></a></td>
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