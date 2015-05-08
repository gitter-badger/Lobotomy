<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, memtype, offset, pid, port, proto, protocol, address, createtime FROM sockets";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Memtype</div>
</th>
<th>
<div class="th_wrapp">Offset(V/P)</div>
</th>
<th>
<div class="th_wrapp">PID</div>
</th>
<th>
<div class="th_wrapp">Port</div>
</th>
<th>
<div class="th_wrapp">Proto</div>
</th>
<th>
<div class="th_wrapp">Protocol</div>
</th>
<th>
<div class="th_wrapp">Address</div>
</th>
<th>
<div class="th_wrapp">Create Time</div>
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
            <td><?php echo $row['memtype']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['offset']; ?>"><?php echo $row['offset']; ?></a></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['port']; ?></td>
            <td><?php echo $row['proto']; ?></td>
            <td><?php echo $row['protocol']; ?></td>
            <td><?php echo $row['address']; ?></td>
            <td><?php echo $row['createtime']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>