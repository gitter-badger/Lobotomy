<?php session_start(); ?>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
mysql_select_db($dbase);
$query = "SELECT id, pid, address, parent, left, right, start, end, tag FROM vadwalk";
$result = mysql_query($query);
?>
<h4><?php echo $dbase; ?></h4>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Pid</div>
</th>
<th>
<div class="th_wrapp">Address</div>
</th>
<th>
<div class="th_wrapp">Parent</div>
</th>
<th>
<div class="th_wrapp">Left</div>
</th>
<th>
<div class="th_wrapp">Right</div>
</th>
<th>
<div class="th_wrapp">Start</div>
</th>
<th>
<div class="th_wrapp">End</div>
</th>
<th>
<div class="th_wrapp">Tag</div>
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
            <td><?php echo $row['pid']; ?></td>
            <td><?php echo $row['address']; ?></td>
            <td><?php echo $row['parent']; ?></td>
            <td><?php echo $row['left']; ?></td>
            <td><?php echo $row['right']; ?></td>
            <td><?php echo $row['start']; ?></td>
            <td><?php echo $row['end']; ?></td>
            <td><?php echo $row['tag']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>