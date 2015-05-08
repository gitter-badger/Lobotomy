<?php
mysql_select_db($_SESSION['dump']['dbase']);
mysql_select_db($dbase);
$query = "SELECT id, offset, duetime, period, signaled, routine, module FROM timers";
$result = mysql_query($query);
?>
<h4><?php echo $dbase; ?></h4>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset</div>
</th>
<th>
<div class="th_wrapp">Duetime</div>
</th>
<th>
<div class="th_wrapp">Period</div>
</th>
<th>
<div class="th_wrapp">Signaled</div>
</th>
<th>
<div class="th_wrapp">Routine</div>
</th>
<th>
<div class="th_wrapp">Module</div>
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
            <td><?php echo $row['offset']; ?></td>
            <td><?php echo $row['duetime']; ?></td>
            <td><?php echo $row['period']; ?></td>
            <td><?php echo $row['signaled']; ?></td>
            <td><?php echo $row['routine']; ?></td>
            <td><?php echo $row['module']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>