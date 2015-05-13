<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, cpu, sel, base, `limit`, `type`, dpl, gr, pr FROM gdt";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">CPU</div>
</th>
<th>
<div class="th_wrapp">Sel</div>
</th>
<th>
<div class="th_wrapp">Base</div>
</th>
<th>
<div class="th_wrapp">Limit</div>
</th>
<th>
<div class="th_wrapp">Type</div>
</th>
<th>
<div class="th_wrapp">DPL</div>
</th>
<th>
<div class="th_wrapp">Gr</div>
</th>
<th>
<div class="th_wrapp">Pr</div>
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
            <td><?php echo $row['sel']; ?></td>
            <td><?php echo $row['base']; ?></td>
            <td><?php echo $row['limit']; ?></td>
            <td><?php echo $row['type']; ?></td>
            <td><?php echo $row['dpl']; ?></td>
            <td><?php echo $row['gr']; ?></td>
            <td><?php echo $row['pr']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>