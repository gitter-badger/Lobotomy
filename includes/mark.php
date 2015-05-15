<?php
include 'database.php';
mysqli_select_db($sqldb, $_GET['db']);
if ($_GET['plugin'] == "photorec") {
    $_GET['plugin'] = 'PR_files';
}
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
mysqli_query($sqldb, $query);
?>