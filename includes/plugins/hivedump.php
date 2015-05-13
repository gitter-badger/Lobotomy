<?php
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, `lastwritten`, `key` FROM hivedump";
$result = mysqli_query($sqldb, $query);
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
    while ($row = mysqli_fetch_assoc($result)) {
        $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'">';
        if (is_marked($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'" class="marked">';
        }
        if (is_done($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-key="'.$row['key'].'" class="done">';
        }
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='".$plugin."' AND row_id=".$row['id'];
        $_result = mysqli_query($sqldb, $_query);
        $_row = mysqli_fetch_assoc($_result);
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
mysqli_select_db($sqldb, "lobotomy");
?>