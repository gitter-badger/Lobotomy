<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, offset, ptr, hnd, creationtime, `from`, `to` FROM symlinkscan";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset</div>
</th>
<th>
<div class="th_wrapp">Pointer</div>
</th>
<th>
<div class="th_wrapp">Handle</div>
</th>
<th>
<div class="th_wrapp">Creationtime</div>
</th>
<th>
<div class="th_wrapp">From</div>
</th>
<th>
<div class="th_wrapp">To</div>
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
            <td><?php echo $row['ptr']; ?></td>
            <td><?php echo $row['hnd']; ?></td>
            <td><?php echo $row['creationtime']; ?></td>
            <td><?php echo $row['from']; ?></td>
            <td><?php echo $row['to']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>