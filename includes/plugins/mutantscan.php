<?php session_start(); ?>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, offset, ptr, hnd, signal, thread, cid, name FROM mutantscan";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset(P)</div>
</th>
<th>
<div class="th_wrapp">#Ptr</div>
</th>
<th>
<div class="th_wrapp">#Hnd</div>
</th>
<th>
<div class="th_wrapp">Signal</div>
</th>
<th>
<div class="th_wrapp">Thread</div>
</th>
<th>
<div class="th_wrapp">CID</div>
</th>
<th>
<div class="th_wrapp">Name</div>
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
            <td><?php echo $row['ptr']; ?></td>
            <td><?php echo $row['hnd']; ?></td>
            <td><?php echo $row['signal']; ?></td>
            <td><?php echo $row['thread']; ?></td>
            <td><?php echo $row['cid']; ?></td>
            <td><?php echo $row['name']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>