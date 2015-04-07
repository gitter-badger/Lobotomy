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
?>
<ul class="tabsB cf">
<li><a href="#hex">HEX-view</a></li>
<li><a href="#strings">Strings</a></li>
</ul>
<div class="content_panes">
<div id="hex">
<pre>
<?php
exec('xxd -c 32 ' . $row['fullfilename'], $xxd);
foreach ($xxd as $line) {
echo htmlspecialchars($line) . PHP_EOL;
}
unset($line);
?>
</pre>
</div>
<div id="strings">
<pre>
<?php
exec('strings ' . $row['fullfilename'], $strings);
foreach ($strings as $line) {
echo htmlspecialchars($line) . PHP_EOL;
}
?>
</pre>
</div>
</div>
<?php
mysql_select_db("lobotomy");
?>