<?php
$query = "SELECT id, name, description, creator, added FROM cases ORDER BY added DESC";
$result = mysqli_query($sqldb, $query);
$num = mysqli_num_rows($result);
if ($num > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        $imquery = "SELECT COUNT(*) as dumps FROM dumps WHERE case_assigned=" . $row['id'];
        $i_mquery = "SELECT dbase FROM dumps WHERE case_assigned=" . $row['id'];
        $imresult = mysqli_query($sqldb, $imquery);
        $i_mresult = mysqli_query($sqldb, $i_mquery);
        $imrow = mysqli_fetch_assoc($imresult);

        $done = 0;
        $queued = 0;
        $running = 0;
        while ($psrow = mysqli_fetch_assoc($i_mresult)) {
            mysqli_select_db($sqldb, $psrow['dbase']);
            $zquery = "SELECT (SELECT COUNT(*) FROM plugins WHERE status=1) done,"
                    . "(SELECT COUNT(*) FROM plugins WHERE status=2) running";
            $zresult = mysqli_query($sqldb, $zquery);
            $zrow = mysqli_fetch_assoc($zresult);
            $done = $done + $zrow['done'];
            $running = $running + $zrow['running'];
            mysqli_select_db($sqldb, "lobotomy");
            $qquery = "SELECT COUNT(*) AS queued FROM queue WHERE command LIKE '%".$psrow['dbase']."%'";
            $qresult = mysqli_query($sqldb, $qquery);
            $qrow = mysqli_fetch_assoc($qresult);
            $queued = $queued + $qrow['queued'];
        }
        ?>
        <div class="pricing_panel">
            <div class="header">
                <h2><?php echo $row['name']; ?></h2>
                <h4><?php echo $row['creator']; ?></h4>
                <h5><?php echo $row['added']; ?></h5>
            </div>
            <div class="pricing_row"><strong><?php echo $imrow['dumps']; ?></strong> image(s) assigned</div>
            <div class="pricing_row"><strong><?php echo $running; ?></strong> tasks running</div>
            <div class="pricing_row"><strong><?php echo $queued; ?></strong> tasks in queue</div>
            <div class="pricing_row"><strong><?php echo $done; ?></strong> tasks completed</div>
            <div class="pricing_action tac">
                <a href="select_case.php?id=<?php echo $row['id']; ?>" class="btn btn_b">Open case</a>
            </div>
        </div>
        <?php
    }
}
?>
<div class="sepH_a_line"></div>
<a href="new_case.php" class="btn btn_bL fl sepV_a"><span class="btnImg" style="background-image: url('images/icons/tag.png');">Create new case</span></a>