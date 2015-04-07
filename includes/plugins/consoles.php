<?php session_start(); ?>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, `consoles` FROM consoles";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">consoles</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    while ($row = mysql_fetch_assoc($result)) {
        if (trim($row['consoles']) != "") {
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
            <tr id="<?php echo $row['id']; ?>" class="<?php echo $class;
        if ($_row['marked']) {
            echo ' marked';
        } ?>" >
                <td><?php echo str_replace(" ", "&nbsp;", htmlentities($row['consoles'], ENT_QUOTES)); ?></td>
            </tr>
            <?php
        }
    }
    ?>
</tbody>
</table>
<?php
mysql_select_db("lobotomy");
?>