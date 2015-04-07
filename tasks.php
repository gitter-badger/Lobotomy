<?php
session_start();
include_once './includes/database.php';
$query = "SELECT id, command, priority, added FROM queue ORDER BY priority ASC, id ASC LIMIT 10";
$result = mysql_query($query);
$tasks = mysql_num_rows($result);
if ($tasks == 0) {
    echo '<h3 class="sepH_c">No remaining tasks</h1>';
} else {
    ?>
    <table class="display" id="content_table" width="100%">
        <thead>
            <tr>
                <th style="text-align: left">Database</th>
                <th style="text-align: left">Plugin</th>
                <th style="text-align: center" width="150">Priority</th>
                <th style="text-align: right" width="120">Added</th>
            </tr>
        </thead>
        <tbody>
            <?php
            while ($row = mysql_fetch_assoc($result)) {
                switch ($row['priority']) {
                    case 1:
                        $style = 'error_bg';
                        break;
                    case 2:
                        $style = 'alert_bg';
                        break;
                    case 3:
                        $style = 'ok_bg';
                        break;
                    case 4:
                        $style = 'info_bg';
                        break;
                    case 5:
                        $style = 'neutral_bg';
                        break;
                    default:
                        $style = 'neutral_bg';
                        break;
                }
                $parts = explode(' ', $row['command']);
                $db = $parts[2];
                if ($parts[1] == "multiparser.py") {
                    $plugin = $parts[3];
                } else {
                    $plugin = str_replace('.py', '', $parts[1]);
                }
                ?>
                <tr>
                    <td style="text-align: left"><?php echo $db; ?></td>
                    <td style="text-align: left"><?php echo $plugin; ?></td>
                    <td style="text-align: left"><span class="fr notification <?php echo $style; ?>">Prio: <?php echo $row['priority']; ?></span></td>
                    <td style="text-align: right"><span class="small"><?php echo $row['added']; ?></span></td>
                </tr>
                <?php
            }
            ?>
        </tbody>
    </table>
    <?php
}
?>