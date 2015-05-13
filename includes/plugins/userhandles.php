<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, sharedinfo, sessionid, shareddelta, ahelist, tablesize, entrysize, object, handle, btype, flags, thread, PROCESS FROM userhandles";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">sharedinfo</div>
</th>
<th>
<div class="th_wrapp">sessionid</div>
</th>
<th>
<div class="th_wrapp">shareddelta</div>
</th>
<th>
<div class="th_wrapp">ahelist</div>
</th>
<th>
<div class="th_wrapp">tablesize</div>
</th>
<th>
<div class="th_wrapp">enrtysize</div>
</th>
<th>
<div class="th_wrapp">object</div>
</th>
<th>
<div class="th_wrapp">handle</div>
</th>
<th>
<div class="th_wrapp">btype</div>
</th>
<th>
<div class="th_wrapp">flags</div>
</th>
<th>
<div class="th_wrapp">threats</div>
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
            <td><?php echo $row['sharedinfo']; ?></td>
            <td><?php echo $row['sessionid']; ?></td>
            <td><?php echo $row['shareddelta']; ?></td>
            <td><?php echo $row['ahelist']; ?></td>
            <td><?php echo $row['tablesize']; ?></td>
            <td><?php echo $row['entrysize']; ?></td>
            <td><?php echo $row['object']; ?></td>
            <td><?php echo $row['handle']; ?></td>
            <td><?php echo $row['btype']; ?></td>
            <td><?php echo $row['flags']; ?></td>
            <td><?php echo $row['thread']; ?></td>
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
