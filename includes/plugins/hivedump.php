<?php session_start(); ?>
<?php
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, `lastwritten`, `key` FROM hivedump";
$result = mysql_query($query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
<thead>
<tr>
<th class="chb_col">
<div class="th_wrapp">Last Written</div>
</th>
<th>
<div class="th_wrapp">Key</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    while ($row = mysql_fetch_assoc($result)) {
        $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'">';
        if (is_marked($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'" class="marked">';
        }
        if (is_done($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'" class="done">';
        }
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='".$plugin."' AND row_id=".$row['id'];
        $_result = mysql_query($_query);
        $_row = mysql_fetch_assoc($_result);
        echo $tr;
        ?>
            <td><?php echo $row['lastwritten']; ?></td>
            <td><?php echo $row['key']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<a id="printkey" class="btn btn_aL fl sepV_a"><span class="btnImg" style="background-image: url('images/icons/sign_post.png');">Run printkey for selected hives</span></a>
<?php
mysql_select_db("lobotomy");
?>