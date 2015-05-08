<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, session, windowstation, format, handle, object, data FROM clipboard";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Session</div>
</th>
<th>
<div class="th_wrapp">Windowstation</div>
</th>
<th>
<div class="th_wrapp">Format</div>
</th>
<th>
<div class="th_wrapp">Handle</div>
</th>
<th>
<div class="th_wrapp">Object</div>
</th>
<th>
<div class="th_wrapp">Data</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    while ($row = mysql_fetch_assoc($result)) {
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
            <td><?php echo $row['session']; ?></td>
            <td><?php echo $row['windowstation']; ?></td>
            <td><?php echo $row['format']; ?></td>
            <td><?php echo $row['handle']; ?></td>
            <td><?php echo $row['object']; ?></td>
            <td><?php echo $row['data']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>