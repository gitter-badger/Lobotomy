<?php
session_start();
include './includes/database.php';
mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT filepath FROM settings";
$result = mysql_query($query);
$row = mysql_fetch_assoc($result);

$file = $row['filepath'].'-mactime.txt';

if (file_exists($file)) {
    header('Content-Description: File Transfer');
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename='.basename($file));
    header('Content-Transfer-Encoding: binary');
    header('Expires: 0');
    header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
    header('Pragma: public');
    header('Content-Length: ' . filesize($file));
    ob_clean();
    flush();
    readfile($file);
    exit;
}
?>