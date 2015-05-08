<?php
mysql_select_db($_SESSION['dump']['dbase']);
mysql_select_db($dbase);
$query = "SELECT id, sharedinfo, sessionid, shareddelta, ahelist, tablesize, enrtysize, object, handle, btype, flags, threats, process FROM userhandles";
$result = mysql_query($query);
?>
<h4><?php echo $dbase; ?></h4>
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
            <td><?php echo $row['sharedinfo']; ?></td>
            <td><?php echo $row['sessionid']; ?></td>
            <td><?php echo $row['shareddelta']; ?></td>
            <td><?php echo $row['ahelist']; ?></td>
            <td><?php echo $row['tablesize']; ?></td>
            <td><?php echo $row['enrtysize']; ?></td>
            <td><?php echo $row['object']; ?></td>
            <td><?php echo $row['handle']; ?></td>
            <td><?php echo $row['btype']; ?></td>
            <td><?php echo $row['flags']; ?></td>
            <td><?php echo $row['threats']; ?></td>
            <td><?php echo $row['process']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>
