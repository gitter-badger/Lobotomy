<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, offset, atomofs, atom, refs, pinned, name FROM atomscan";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset</div>
</th>
<th>
<div class="th_wrapp">AtomOfs</div>
</th>
<th>
<div class="th_wrapp">Atom</div>
</th>
<th>
<div class="th_wrapp">Refs</div>
</th>
<th>
<div class="th_wrapp">Pinned</div>
</th>
<th>
<div class="th_wrapp">Name</div>
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
            <td><?php echo $row['atomofs']; ?></td>
            <td><?php echo $row['atom']; ?></td>
            <td><?php echo $row['refs']; ?></td>
            <td><?php echo $row['pinned']; ?></td>
            <td><?php echo $row['name']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>