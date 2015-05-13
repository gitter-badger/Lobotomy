<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, pid, commandprocess, commandhistory, application, flags, commandcount, lastadded, lastdisplayed, firstcommand, commandcountmax, processhandle, cmd1, cmd2, cmd3, cmd4 FROM cmdscan";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">pid</div>
</th>
<th>
<div class="th_wrapp">commandprocess</div>
</th>
<th>
<div class="th_wrapp">commandhistory</div>
</th>
<th>
<div class="th_wrapp">application</div>
</th>
<th>
<div class="th_wrapp">flags</div>
</th>
<th>
<div class="th_wrapp">commandcount</div>
</th>
<th>
<div class="th_wrapp">lastadded</div>
</th>
<th>
<div class="th_wrapp">lastdisplayed</div>
</th>
<th>
<div class="th_wrapp">firstcommand</div>
</th>
<th>
<div class="th_wrapp">commandcountmax</div>
</th>
<th>
<div class="th_wrapp">processhandle</div>
</th>
<th>
<div class="th_wrapp">cmd1</div>
</th>
<th>
<div class="th_wrapp">cmd2</div>
</th>
<th>
<div class="th_wrapp">cmd3</div>
</th>
<th>
<div class="th_wrapp">cmd4</div>
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
            <td><?php echo $row['pid']; ?></td>
            <td><?php echo $row['commandprocess']; ?></td>
            <td><?php echo $row['commandhistory']; ?></td>
            <td><?php echo $row['application']; ?></td>
            <td><?php echo $row['flags']; ?></td>
            <td><?php echo $row['commandcount']; ?></td>
            <td><?php echo $row['lastadded']; ?></td>
            <td><?php echo $row['lastdisplayed']; ?></td>
            <td><?php echo $row['firstcommand']; ?></td>
            <td><?php echo $row['commandcountmax']; ?></td>
            <td><?php echo $row['processhandle']; ?></td>
            <td><?php echo $row['cmd1']; ?></td>
            <td><?php echo $row['cmd2']; ?></td>
            <td><?php echo $row['cmd3']; ?></td>
            <td><?php echo $row['cmd4']; ?></td>			
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>