<?php
//include_once './includes/database.php';
if (isset($_SESSION['dump']['id'])) {
    $query = "SELECT id, location, dbase, added, case_assigned FROM dumps WHERE id=" . $_SESSION['dump']['id'];
    $result = mysqli_query($sqldb, $query);
    $row = mysqli_fetch_assoc($result);

    $dump['id'] = $row['id'];
    $dump['location'] = $row['location'];
    $dump['dbase'] = $row['dbase'];
    $dump['added'] = $row['added'];
    $dump['case_assigned'] = $row['case_assigned'];

    $_SESSION['dump'] = $dump;
    $_SESSION['dump']['selected'] = True;
}
?>