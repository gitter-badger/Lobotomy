<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, depth, offset, name, pid, ppid, thds, hnds, plugin_time, audit, cmd, path FROM pstree";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Depth</div>
</th>
<th>
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
<div class="th_wrapp">THDS</div>
</th>
<th>
<div class="th_wrapp">HNDS</div>
</th>
<th>
<div class="th_wrapp">Plugin Time</div>
</th>
<th>
<div class="th_wrapp">audit</div>
</th>
<th>
<div class="th_wrapp">cmd</div>
</th>
<th>
<div class="th_wrapp">path</div>
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
            <td><?php
            while ($row['depth'] > 0) {
                echo '-';
                $row['depth']--;
            }
            ?></td>
            <td><a href="./search.php?q=<?php echo $row['offset']; ?>"><?php echo $row['offset']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['name']; ?>"><?php echo $row['name']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['ppid']; ?>&type=PID"><?php echo $row['ppid']; ?></a></td>
            <td><?php echo $row['thds']; ?></td>
            <td><?php echo $row['hnds']; ?></td>
            <td><?php echo $row['plugin_time']; ?></td>
            <td><?php echo $row['audit']; ?></td>
            <td><?php echo $row['cmd']; ?></td>
            <td><?php echo $row['path']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>