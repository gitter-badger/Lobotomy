<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, `offset`, `name`, pid, ppid, thds, hnds, sess, wow64, `start`, `exit` FROM pslist";
$result = mysqli_query($sqldb, $query);
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
<div class="th_wrapp">Thds</div>
</th>
<th>
<div class="th_wrapp">Hnds</div>
</th>
<th>
<div class="th_wrapp">Sess</div>
</th>
<th>
<div class="th_wrapp">Wow64</div>
</th>
<th>
<div class="th_wrapp">Start</div>
</th>
<th>
<div class="th_wrapp">Exit</div>
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
            <td><?php echo $row['offset']; ?></td>
            <td><?php echo $row['name']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['ppid']; ?></td>
            <td><?php echo $row['thds']; ?></td>
            <td><?php echo $row['hnds']; ?></td>
            <td><?php echo $row['sess']; ?></td>
            <td><?php echo $row['wow64']; ?></td>
            <td><?php echo $row['start']; ?></td>
            <td><?php echo $row['exit']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>