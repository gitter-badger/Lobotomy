<?php
session_start();
include_once './includes/database.php';
$query = "SELECT COUNT(*) AS num_tasks FROM queue";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$new_tasks = $row['num_tasks'];

$query = "SELECT COUNT(*) AS num_cases FROM cases";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$cases = $row['num_cases'];

$dirs = 0;
$x = "/home/solvent/dumps/";
$y = scandir($x);
foreach ($y as $z) {
    if ($z != '.' AND $z != '..') {
        if (is_dir($x . $z)) {
            $dirs++;
        }
    }
}

$query = "SELECT COUNT(*) AS num_tasks FROM queue_archive";
$result = mysqli_query($sqldb, $query);
$row = mysqli_fetch_assoc($result);
$old_tasks = $row['num_tasks'];
?>
<ul class="summary_list">
    <li><span><?php echo $new_tasks; ?></span> tasks currently in queue, waiting to be run</li>
    <li><span><?php echo $cases; ?></span> cases are registered at this moment</li>
    <li><span><?php echo $dirs; ?></span> memory dumps in the dumps folder</li>
    <li><span><?php echo $old_tasks; ?></span> tasks executed since the last time I was reset</li>
</ul>