<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, offset, name, pid, ppid, sess, jobsess, wow64, total,  active, term, joblink, process FROM joblinks";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">offset</div>
</th>
<th>
<div class="th_wrapp">name</div>
</th>
<th>
<div class="th_wrapp">pid</div>
</th>
<th>
<div class="th_wrapp">ppid</div>
</th>
<th>
<div class="th_wrapp">sess</div>
</th>
<th>
<div class="th_wrapp">jobsess</div>
</th>
<th>
<div class="th_wrapp">wow64</div>
</th>
<th>
<div class="th_wrapp">total</div>
</th>
<th>
<div class="th_wrapp">active</div>
</th>
<th>
<div class="th_wrapp">term</div>
</th>
<th>
<div class="th_wrapp">joblink</div>
</th>
<th>
<div class="th_wrapp">process</div>
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
            <td><?php echo $row['pid']; ?></td>
            <td><?php echo $row['ppid']; ?></td>
            <td><?php echo $row['sess']; ?></td>
            <td><?php echo $row['jobsess']; ?></td>
            <td><?php echo $row['wow64']; ?></td>
            <td><?php echo $row['total']; ?></td>
            <td><?php echo $row['active']; ?></td>
            <td><?php echo $row['term']; ?></td>
            <td><?php echo $row['joblink']; ?></td>
            <td><?php echo $row['process']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>