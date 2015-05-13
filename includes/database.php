<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
$sqldb = mysqli_connect("localhost", "root", "Fwgs91VpfRRH22K", "lobotomy");

function is_marked($plugin, $id) {
    $query = "SELECT COUNT(*) AS marked FROM preferences WHERE plugin='" . $plugin . "' AND action='mark' AND row_id=" . $id;
    $result = mysqli_query($sqldb, $query);
    $row = mysqli_fetch_assoc($result);
    return $row['marked'];
}

function is_done($plugin, $id) {
    $query = "SELECT COUNT(*) AS done FROM preferences WHERE plugin='" . $plugin . "' AND action='done' AND row_id=" . $id;
    $result = mysqli_query($sqldb, $query);
    $row = mysqli_fetch_assoc($result);
    return $row['done'];
}

function is_bad_hash($hash) {
    mysqli_select_db($sqldb, "lobotomy");
    $query = "SELECT COUNT(*) AS hashes FROM bad_hashes WHERE md5hash='".$hash."'";
    $result = mysqli_query($sqldb, $query);
    $row = mysqli_fetch_assoc($result);
    return $row['hashes'];
}
?>