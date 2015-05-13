<?php
global $sqldb;
mysqli_select_db($sqldb, $_SESSION['dump']['dbase']);
$query = "SELECT id, virtual, physical, name FROM hivelist";
$result = mysqli_query($sqldb, $query);
?>
<table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
    <thead>
        <tr>
            <th class="chb_col">
    <div class="th_wrapp">virtual</div>
</th>
<th>
<div class="th_wrapp">physical</div>
</th>
<th>
<div class="th_wrapp">name</div>
</th>
</tr>
</thead>
<tbody>
    <?php
    while ($row = mysqli_fetch_assoc($result)) {
        $tr = '<tr id="'.$row['id'].'" data-offset="'.$row['virtual'].'">';
        if (is_marked($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-offset="'.$row['virtual'].'" class="marked">';
        }
        if (is_done($plugin, $row['id'])) {
            $tr = '<tr id="'.$row['id'].'" data-offset="'.$row['virtual'].'" class="done">';
        }
        $_query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND row_id=" . $row['id'];
        $_result = mysqli_query($sqldb, $_query);
        $_row = mysqli_fetch_assoc($_result);
        echo $tr;
        ?>
            <td><?php echo $row['virtual']; ?></td>
            <td><?php echo $row['physical']; ?></td>
            <td><?php echo $row['name']; ?></td>
        </tr>
        <?php
    }
    ?>
</tbody>
</table>
<a id="hivedump" class="btn btn_aL fl sepV_a"><span class="btnImg" style="background-image: url('images/icons/sign_post.png');">Run hivedump for selected hives</span></a>
<?php
mysqli_select_db($sqldb, "lobotomy");
?>