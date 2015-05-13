<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, process, pid, sid, user, comment FROM getsids";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Process</div>
</th>
<th>
<div class="th_wrapp">PID</div>
</th>
<th>
<div class="th_wrapp">SID</div>
</th>
<th>
<div class="th_wrapp">User</div>
</th>
<th>
<div class="th_wrapp">Comment</div>
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
            <td><?php echo $row['process']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['sid']; ?></td>
            <td><?php echo $row['user']; ?></td>
            <td><?php echo $row['comment']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>