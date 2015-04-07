<?php session_start(); ?>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, pid, process, base, inload, ininit, inmem, mappedpath FROM ldrmodules";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">pid</div>
</th>
<th>
<div class="th_wrapp">process</div>
</th>
<th>
<div class="th_wrapp">base</div>
</th>
<th>
<div class="th_wrapp">inload</div>
</th>
<th>
<div class="th_wrapp">ininit</div>
</th>
<th>
<div class="th_wrapp">inmem</div>
</th>
<th>
<div class="th_wrapp">mappedpath</div>
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
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['process']; ?></td>
            <td><?php echo $row['base']; ?></td>
            <td><?php echo $row['inload']; ?></td>
            <td><?php echo $row['ininit']; ?></td>
            <td><?php echo $row['inmem']; ?></td>
            <td><?php echo $row['mappedpath']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>