<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT `id`, `cpu`, `index`, `selector`, `value`, `module`, `section` FROM idt";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">CPU</div>
</th>
<th>
<div class="th_wrapp">Index</div>
</th>
<th>
<div class="th_wrapp">Selector</div>
</th>
<th>
<div class="th_wrapp">Value</div>
</th>
<th>
<div class="th_wrapp">Module</div>
</th>
<th>
<div class="th_wrapp">Section</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    while ($row = mysqli_fetch_assoc($result)) {
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND row_id=" . $row['id'];
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
            <td><?php echo $row['cpu']; ?></td>
            <td><?php echo $row['index']; ?></td>
            <td><?php echo $row['selector']; ?></td>
            <td><?php echo $row['value']; ?></td>
            <td><?php echo $row['module']; ?></td>
            <td><?php echo $row['section']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>