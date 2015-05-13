<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, id, aaa, bbb, ccc, ddd, eee, fff, ggg, hhh,  iii, jjj, kkk, lll FROM xxxxxx";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">aaa</div>
</th>
<th>
<div class="th_wrapp">bbb</div>
</th>
<th>
<div class="th_wrapp">ccc</div>
</th>
<th>
<div class="th_wrapp">ddd</div>
</th>
<th>
<div class="th_wrapp">eee</div>
</th>
<th>
<div class="th_wrapp">fff</div>
</th>
<th>
<div class="th_wrapp">ggg</div>
</th>
<th>
<div class="th_wrapp">hhh</div>
</th>
<th>
<div class="th_wrapp">iii</div>
</th>
<th>
<div class="th_wrapp">jjj</div>
</th>
<th>
<div class="th_wrapp">kkk</div>
</th>
<th>
<div class="th_wrapp">lll</div>
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
            <td><?php echo $row['aaa']; ?></td>
            <td><?php echo $row['bbb']; ?></td>
            <td><?php echo $row['ccc']; ?></td>
            <td><?php echo $row['ddd']; ?></td>
            <td><?php echo $row['eee']; ?></td>
            <td><?php echo $row['fff']; ?></td>
            <td><?php echo $row['ggg']; ?></td>
            <td><?php echo $row['hhh']; ?></td>
            <td><?php echo $row['iii']; ?></td>
            <td><?php echo $row['jjj']; ?></td>
            <td><?php echo $row['kkk']; ?></td>
            <td><?php echo $row['lll']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>