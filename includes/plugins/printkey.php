<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, `register`, keyname, keylegend, lastupdated, subkeys, type, `values`, legend, model FROM printkey";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">register</div>
</th>
<th>
<div class="th_wrapp">keyname</div>
</th>
<th>
<div class="th_wrapp">keylegend</div>
</th>
<th>
<div class="th_wrapp">lastupdated</div>
</th>
<th>
<div class="th_wrapp">subkeys</div>
</th>
<th>
<div class="th_wrapp">type</div>
</th>
<th>
<div class="th_wrapp">values</div>
</th>
<th>
<div class="th_wrapp">legend</div>
</th>
<th>
<div class="th_wrapp">model</div>
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
            <td><?php echo $row['register']; ?></td>
            <td><?php echo $row['keyname']; ?></td>
            <td><?php echo $row['keylegend']; ?></td>
            <td><?php echo $row['lastupdated']; ?></td>
            <td><?php echo $row['subkeys']; ?></td>
            <td><?php echo $row['type']; ?></td>
            <td><?php echo $row['values']; ?></td>
            <td><?php echo $row['legend']; ?></td>
            <td><?php echo $row['model']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>