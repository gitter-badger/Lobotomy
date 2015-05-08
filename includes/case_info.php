<?php
include_once './includes/database.php';
$query = "SELECT id, name, description, creator, added FROM cases WHERE id=" . $_SESSION['case']['id'];
$result = mysql_query($query);
$row = mysql_fetch_assoc($result);

$case['id'] = $row['id'];
$case['name'] = $row['name'];
$case['description'] = $row['description'];
$case['creator'] = $row['creator'];
$case['added'] = $row['added'];

$query = "SELECT dbase FROM dumps WHERE case_assigned=" . $case['id'];
$result = mysql_query($query);
$case['num_dumps'] = mysql_num_rows($result);
if ($case['num_dumps'] > 0) {
    while ($row = mysql_fetch_assoc($result)) {
        $case['dumps'][] = $row['dbase'];
    }
}
$_SESSION['case'] = $case;
$_SESSION['case']['selected'] = True;
?>