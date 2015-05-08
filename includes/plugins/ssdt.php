<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, ssdt, mem1, entry, mem2, systemcall, owner FROM ssdt";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">SSDT</div>
</th>
<th>
<div class="th_wrapp">SSDT Offset</div>
</th>
<th>
<div class="th_wrapp">Entry</div>
</th>
<th>
<div class="th_wrapp">Offset</div>
</th>
<th>
<div class="th_wrapp">Systemcall</div>
</th>
<th>
<div class="th_wrapp">Owner</div>
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
            <td><?php echo $row['ssdt']; ?></td>
            <td><?php echo $row['mem1']; ?></td>
            <td><?php echo $row['entry']; ?></td>
            <td><?php echo $row['mem2']; ?></td>
            <td><?php echo $row['systemcall']; ?></td>
            <td><?php echo $row['owner']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>