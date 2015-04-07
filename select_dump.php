<?php session_start(); ?>
<?php
$_SESSION['dump']['selected'] = True;
$_SESSION['dump']['id'] = $_GET['id'];
header('location: case.php');
?>