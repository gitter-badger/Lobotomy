<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, offset, name, pid, ppid, pdb, timecreated, timeexited FROM psscan";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset</div>
</th>
<th>
<div class="th_wrapp">Name</div>
</th>
<th>
<div class="th_wrapp">PID</div>
</th>
<th>
<div class="th_wrapp">PPID</div>
</th>
<th>
<div class="th_wrapp">PDB</div>
</th>
<th>
<div class="th_wrapp">TimeCreated</div>
</th>
<th>
<div class="th_wrapp">TimeExited</div>
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
            <td><?php echo $row['name']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['ppid']; ?>&type=PID"><?php echo $row['ppid']; ?></a></td>
            <td><?php echo $row['pdb']; ?></td>
            <td><?php echo $row['timecreated']; ?></td>
            <td><?php echo $row['timeexited']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>