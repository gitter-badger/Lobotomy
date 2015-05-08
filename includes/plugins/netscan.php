<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT `id`, `offset`, `proto`, `localaddress`, `foreignaddress`, `state`, `pid`, `owner`, `createtime` FROM netscan";
$result = mysql_query($query);
?>
<h4><?php echo $dbase; ?></h4>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">Offset</div>
</th><th>
<div class="th_wrapp">proto</div>
</th><th>
<div class="th_wrapp">localaddress</div>
</th><th>
<div class="th_wrapp">foreignaddress</div>
</th><th>
<div class="th_wrapp">state</div>
</th><th>
<div class="th_wrapp">pid</div>
</th><th>
<div class="th_wrapp">owner</div>
</th><th>
<div class="th_wrapp">Createtime</div>
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
        if (!$filter) {
            $class = "filter_none";
        } else {
            $class = "filter_" . $filter;
        }
        ?>
        <tr id="<?php echo $row['id']; ?>" class="<?php
        echo $class;
        if ($_row['marked']) {
            echo ' marked';
        }
        ?>" >
            <td><a href="./search.php?q=<?php echo $row['offset']; ?>"><?php echo $row['offset']; ?></a></td>
            <td><?php echo $row['proto']; ?></td>
            <td><?php echo $row['localaddress']; ?></td>
            <td><?php echo $row['foreignaddress']; ?></td>
            <td><?php echo $row['state']; ?></td>
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['owner']; ?></td>
            <td>
                <?php
                if ($row['createtime'] == "0000-00-00 00:00:00") {
                    echo '';
                } else {
                    echo $row['createtime'];
                }
                ?>
            </td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>