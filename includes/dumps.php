<?php
$query = "SELECT id, location, dbase, added FROM dumps WHERE case_assigned=" . $_SESSION['case']['id'];
$result = mysqli_query($sqldb, $query);
$num = mysqli_num_rows($result);
if ($num > 0) {
    while ($row = mysqli_fetch_assoc($result)) {
        if ($_SESSION['dump']['id'] == $row['id']) {
            $style = 'pricing_promoted';
            $btn = False;
        } else {
            $style = 'pricing_panel';
            $btn = True;
        }
        
        $pcquery = "SELECT COUNT(*) AS num FROM queue_archive WHERE command LIKE '%" . $row['dbase'] . "%'";
        $pcresult = mysqli_query($sqldb, $pcquery);
        $pcrow = mysqli_fetch_assoc($pcresult);

        $pqquery = "SELECT COUNT(*) AS num FROM queue WHERE command LIKE '%" . $row['dbase'] . "%'";
        $pqresult = mysqli_query($sqldb, $pqquery);
        $pqrow = mysqli_fetch_assoc($pqresult);
        ?>
        <div class="<?php echo $style; ?>">
            <div class="header">
                <h2 style="overflow: hidden" title="<?php echo $row['dbase']; ?>"><?php echo $row['dbase']; ?></h2>
                <h5><?php echo $row['added']; ?></h5>
            </div>
            <div class="pricing_row"><strong><?php echo $pcrow['num']; ?></strong> plugins completed</div>
            <div class="pricing_row"><strong><?php echo $pqrow['num']; ?></strong> plugins queued</div>
            <div class="pricing_action tac">
                <?php
                if ($btn) {
                    ?>
                    <a href="select_dump.php?id=<?php echo $row['id']; ?>" class="btn btn_b">Select image</a>
                    <?php
                }
                ?>
            </div>
        </div>
        <?php
        unset($pcrow);
        unset($pqrow);
    }
}
?>