<?php session_start(); ?>
<?php
include 'database.php';
mysqli_select_db($sqldb, "lobotomy");
if ($_GET['mode'] == 0) {
    $query = "INSERT INTO queue (command, priority, added) VALUES ('python hivedump.py " . $_GET['db'] . " " . $_GET['offset'] . "', 2, NOW())";
    mysqli_query($sqldb, $query);
}
if ($_GET['mode'] == 1) {
    mysqli_select_db($sqldb, $_GET['db']);
    $query = "SELECT `key` FROM hivedump WHERE id='".$_GET['id']."'";
    $result = mysqli_query($sqldb, $query);
    $row = mysqli_fetch_assoc($result);
    $query = "INSERT INTO queue (command, priority, added) VALUES ('python printkey.py " . $_GET['db'] . " " . mysqli_real_escape_string($sqldb, $row['key']) . "', 2, NOW())";
    mysqli_select_db($sqldb, 'lobotomy');
    mysqli_query($sqldb, $query);
}
?>