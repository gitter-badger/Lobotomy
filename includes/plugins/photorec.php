<div class="msg_box msg_alert"><strong>Clicking on a hash will submit the clicked hash to VirusTotal!</strong></div>
<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, fullfilename, filename, filemd5 FROM PR_files";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">filename</div>
</th>
<th>
<div class="th_wrapp">filemd5</div>
</th>

</tr>
</thead>
<tbody>
    <?php
    $bad = False;
    while ($row = mysqli_fetch_assoc($result)) {
        if ($row['filemd5'] == "0") {
            $row['filemd5'] = '-';
        } else {
            if (is_bad_hash($row['filemd5'])) {
                $bad = True;
            }
            $row['filemd5'] = '<a href="https://www.virustotal.com/en/search/?query=' . $row['filemd5'] . '" target="_blank">' . $row['filemd5'] . '</a>&nbsp;&nbsp;<img src="./images/icons/alert2.png" title="This will upload the hash to VirusTotal!" alt="This will upload the hash to VirusTotal!" />';
        }
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND row_id=" . $row['id'];
        mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
        $_result = mysqli_query($sqldb, $_query);
        $_row = mysqli_fetch_assoc($_result);
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
            <td><a href="plugin.php?name=xxd&ID=<?php echo $row['id']; ?>&plugin=PR_files"><?php echo $row['filename']; ?></a></td>
            <td<?php if ($bad) { ?> class='bad_hash'<?php } ?>><p><?php echo $row['filemd5']; ?></p></td>
        </tr>
        <?php
        $bad = False;
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>