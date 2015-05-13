<?php
$query = "SELECT COUNT(*) AS unass_dump FROM dumps WHERE case_assigned=0";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$counter['unassigned_dumps'] = $row['unass_dump'];
unset($query, $result, $row);

$query = "SELECT COUNT(*) AS tsk_pend FROM queue";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$counter['tasks_pending'] = $row['tsk_pend'];
unset($query, $result, $row);

$query = "SELECT FORMAT(COUNT(*),0) AS good_hashes FROM good_hashes";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$counter['good_hashes'] = $row['good_hashes'];
unset($query, $result, $row);

$query = "SELECT FORMAT(COUNT(*),0) AS bad_hashes FROM bad_hashes";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$counter['bad_hashes'] = str_replace(',', '.', $row['bad_hashes']);
unset($query, $result, $row);
?>