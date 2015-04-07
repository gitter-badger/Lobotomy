<?php

mysql_select_db($_SESSION['dump']['dbase']);
$query = "SELECT id, filename, fullfilename FROM " . mysql_real_escape_string($_GET['plugin']) . " where id = " . mysql_real_escape_string($_GET['ID']);
$result = mysql_query($query) or die(mysql_error());
$query1 = "SELECT id, filename, fullfilename FROM " . mysql_real_escape_string($_GET['plugin']);
$result1 = mysql_query($query1);

echo '<select id="dropdown">' . PHP_EOL;
$row = mysql_fetch_assoc($result);
while ($r = mysql_fetch_array($result1)) {
    if ($r['filename'] != "") {
        if ($r['filename'] == $row['filename']) {
            echo '<option value="' . $r['id'] . '" selected="selected"> ' . $r['filename'] . '</option>' . PHP_EOL;
        } else {
            echo '<option value="' . $r['id'] . '"> ' . $r['filename'] . '</option>' . PHP_EOL;
        }
    }
}
echo "</select>";

echo '<code>' . $row['filename'] . '</code>' . PHP_EOL;
echo '<br /><br />';
echo '<a href="#strings"><strong>Jump to strings</strong></a>';
echo '<br />';
echo '<a name="hex"></a>';
echo '<pre>';
$xxd = passthru('xxd -c 32 ' . $row['fullfilename']);
echo htmlspecialchars($xxd);
echo '</pre>';
echo '<br /><br />';
echo '<a href="#hex"><strong>Jump to hex</strong></a>';
echo '<a name="strings"></a>';
echo '<pre>';
passthru('strings '.$row['fullfilename']);
echo '</pre>';
mysql_select_db("lobotomy");
?>