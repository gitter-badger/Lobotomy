<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, pid, name, virtual, physical, size, dumpfileoffset FROM memmap";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">pid</div>
</th>
<th>
<div class="th_wrapp">name</div>
</th>
<th>
<div class="th_wrapp">virtual</div>
</th>
<th>
<div class="th_wrapp">physical</div>
</th>
<th>
<div class="th_wrapp">size</div>
</th>
<th>
<div class="th_wrapp">dumpfileoffset</div>
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
            <td><a href="./search.php?q=<?php echo $row['pid']; ?>&type=PID"><?php echo $row['pid']; ?></a></td>
            <td><?php echo $row['name']; ?></td>
            <td><?php echo $row['virtual']; ?></td>
            <td><?php echo $row['physical']; ?></td>
            <td><?php echo $row['size']; ?></td>
            <td><?php echo $row['dumpfileoffset']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>