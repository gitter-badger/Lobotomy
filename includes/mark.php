<?php
include 'database.php';
mysql_select_db($_GET['db']);
switch ($_GET['mode']) {
    case 0:
        $query = "DELETE FROM preferences WHERE `plugin`='".$_GET['plugin']."' AND action='mark' AND `row_id`='".$_GET['id']."'";
        break;
    case 1:
        $query = "INSERT INTO preferences (`plugin`, `row_id`, `action`) VALUES ('".$_GET['plugin']."', '".$_GET['id']."', 'mark')";
        break;
    case 2:
        $query = "UPDATE preferences SET action='done' WHERE plugin='".$_GET['plugin']."' AND row_id=".$_GET['id'];
        break;
}
mysql_query($query);
?>