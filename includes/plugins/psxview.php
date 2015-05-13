<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, offset, name, pid, pslist, psscan, thrdproc, pspcid, csrss, session, deskthrd, exittime FROM psxview";
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
<div class="th_wrapp">PsList</div>
</th>
<th>
<div class="th_wrapp">PsScan</div>
</th>
<th>
<div class="th_wrapp">ThrdProc</div>
</th>
<th>
<div class="th_wrapp">Pspcid</div>
</th>
<th>
<div class="th_wrapp">csrss</div>
</th>
<th>
<div class="th_wrapp">Session</div>
</th>
<th>
<div class="th_wrapp">Deskthrd</div>
</th>
<th>
<div class="th_wrapp">ExitTime</div>
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
            <td><?php echo $row['pslist']; ?></td>
            <td><?php echo $row['psscan']; ?></td>
            <td><?php echo $row['thrdproc']; ?></td>
            <td><?php echo $row['pspcid']; ?></td>
            <td><?php echo $row['csrss']; ?></td>
            <td><?php echo $row['session']; ?></td>
            <td><?php echo $row['deskthrd']; ?></td>
            <td><?php echo $row['exittime']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>