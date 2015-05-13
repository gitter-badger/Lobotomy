<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, sess, handle, object, thread, process, nid, rate, countdown, func FROM gditimers";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">sess</div>
</th>
<th>
<div class="th_wrapp">handle</div>
</th>
<th>
<div class="th_wrapp">object</div>
</th>
<th>
<div class="th_wrapp">thread</div>
</th>
<th>
<div class="th_wrapp">process</div>
</th>
<th>
<div class="th_wrapp">nid</div>
</th>
<th>
<div class="th_wrapp">rate</div>
</th>
<th>
<div class="th_wrapp">countdown</div>
</th>
<th>
<div class="th_wrapp">func</div>
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
            <td><?php echo $row['sess']; ?></td>
            <td><?php echo $row['handle']; ?></td>
            <td><?php echo $row['object']; ?></td>
            <td><?php echo $row['thread']; ?></td>
            <td><?php echo $row['process']; ?></td>
            <td><?php echo $row['nid']; ?></td>
            <td><?php echo $row['rate']; ?></td>
            <td><?php echo $row['countdown']; ?></td>
            <td><?php echo $row['func']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>