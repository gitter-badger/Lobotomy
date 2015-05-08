<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, pid, process, value, privileges, attributes, description FROM privs";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Pid</div>
</th>
<th>
<div class="th_wrapp">Process</div>
</th>
<th>
<div class="th_wrapp">Value</div>
</th>
<th>
<div class="th_wrapp">Privileges</div>
</th>
<th>
<div class="th_wrapp">Attributes</div>
</th>
<th>
<div class="th_wrapp">Description</div>
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
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['process']; ?></td>
            <td><?php echo $row['value']; ?></td>
            <td><?php echo $row['privileges']; ?></td>
            <td><?php echo $row['attributes']; ?></td>
            <td><?php echo $row['description']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>