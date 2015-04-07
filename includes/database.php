<?php
session_start();
mysql_connect("localhost", "root", "ZPRvLVaZReH5BbNJGCu7OeEO1edBaJzh");
mysql_select_db("lobotomy");

function is_marked($plugin, $id) {
    $query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND action='mark' AND row_id=" . $id;
    $result = mysql_query($query);
    $row = mysql_fetch_assoc($result);
    return $row['marked'];
}

function is_done($plugin, $id) {
    $query = "SELECT COUNT(*) AS done FROM preferences WHERE plugin='" . $plugin . "' AND action='done' AND row_id=" . $id;
    $result = mysql_query($query);
    $row = mysql_fetch_assoc($result);
    return $row['done'];
}

function is_bad_hash($hash) {
    mysql_select_db("lobotomy");
    $query = "SELECT COUNT(*) AS hashes FROM bad_hashes WHERE md5hash='".$hash."'";
    $result = mysql_query($query);
    $row = mysql_fetch_assoc($result);
    return $row['hashes'];
}
?>