<?php session_start(); ?>
<?php
include 'database.php';
mysql_select_db("lobotomy");
if ($_GET['mode'] == 0) {
    $query = "INSERT INTO queue (command, priority, added) VALUES ('python hivedump.py " . $_GET['db'] . " " . $_GET['offset'] . "', 2, NOW())";
    mysql_query($query);
}
if ($_GET['mode'] == 1) {
    mysql_select_db($_GET['db']);
    $query = "SELECT `key` FROM hivedump WHERE id='".$_GET['id']."'";
    $result = mysql_query($query);
    $row = mysql_fetch_assoc($result);
    $query = "INSERT INTO queue (command, priority, added) VALUES ('python printkey.py " . $_GET['db'] . " " . mysql_real_escape_string($row['key']) . "', 2, NOW())";
    mysql_select_db('lobotomy');
    mysql_query($query);
}
?>