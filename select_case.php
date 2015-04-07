<?php session_start(); ?>
<?php
$_SESSION['case']['selected'] = True;
$_SESSION['case']['id'] = $_GET['id'];
header('location: case.php');
?>