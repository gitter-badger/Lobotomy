<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, prefetchfile, executiontime, times, size FROM prefetchparser";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Prefetchfile</div>
</th>
<th>
<div class="th_wrapp">executiontime</div>
</th>
<th>
<div class="th_wrapp">Times</div>
</th>
<th>
<div class="th_wrapp">Size</div>
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
            <td><?php echo $row['prefetchfile']; ?></td>
            <td><?php echo $row['executiontime']; ?></td>
            <td><?php echo $row['times']; ?></td>
            <td><?php echo $row['size']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>