<?php

session_start();

function search_image($srch, $timeline = 0, $dbase = null) {
    $matches = array();
    if ($srch == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $result = mysql_list_tables($dbase) or die(mysql_error());
    $num_rows = mysql_num_rows($result) or die(mysql_error());
    for ($i = 0; $i < $num_rows; $i++) {
        $table = mysql_tablename($result, $i) or die(mysql_error());
        if ($table != 'settings' && $table != 'plugins' && $table != 'preferences') {
            if ($table == 'memtimeliner') {
                if ($timeline != 1) {
                    break;
                }
            }
            $result2 = mysql_query("SHOW COLUMNS FROM " . $table) or die(mysql_error());
            if (mysql_num_rows($result2) > 0) {
                while ($row2 = mysql_fetch_assoc($result2)) {
                    $_query = "SELECT id FROM `" . $table . "` WHERE `" . $row2['Field'] . "` LIKE CONCAT('%', CAST('" . mysql_real_escape_string($srch) . "' as CHAR),'%')";
                    $_result = mysql_query($_query) or die(mysql_error());
                    if (mysql_num_rows($_result) > 0) {
                        while ($_row = mysql_fetch_assoc($_result)) {
                            $matches[$dbase][$table][] = $_row['id'];
                        }
                    }
                }
            }
        }
    }
    mysql_free_result($result);
    return $matches;
}

function search_strings($srch, $dbase = null) {
    $matches = array();
    if ($srch == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $table = 'strings';
    $result2 = mysql_query("SHOW COLUMNS FROM " . $table) or die(mysql_error());
    if (mysql_num_rows($result2) > 0) {
        while ($row2 = mysql_fetch_assoc($result2)) {
            $_query = "SELECT id FROM `" . $table . "` WHERE `" . $row2['Field'] . "` LIKE CONCAT('%', CAST('" . mysql_real_escape_string($srch) . "' as CHAR),'%')";
            $_result = mysql_query($_query) or die(mysql_error());
            if (mysql_num_rows($_result) > 0) {
                while ($_row = mysql_fetch_assoc($_result)) {
                    $matches[$dbase][$table][] = $_row['id'];
                }
            }
        }
    }
    mysql_free_result($result);
    return $matches;
}

function search_pid($pid, $dbase = null) {
    $matches = array();
    if ($pid == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $result = mysql_list_tables($dbase) or die(mysql_error());
    $num_rows = mysql_num_rows($result) or die(mysql_error());
    for ($i = 0; $i < $num_rows; $i++) {
        $table = mysql_tablename($result, $i) or die(mysql_error());
        if ($table != 'settings' && $table != 'memtimeliner' && $table != 'preferences') {
            $result2 = mysql_query("SHOW COLUMNS FROM " . $table) or die(mysql_error());
            if (mysql_num_rows($result2) > 0) {
                while ($row2 = mysql_fetch_assoc($result2)) {
                    if ($row2['Field'] == 'pid') {
                        $_query = "SELECT id FROM `" . $table . "` WHERE `pid` = '" . mysql_real_escape_string($pid) . "'";
                        $_result = mysql_query($_query) or die(mysql_error());
                        if (mysql_num_rows($_result) > 0) {
                            while ($_row = mysql_fetch_assoc($_result)) {
                                $matches[$dbase][$table][] = $_row['id'];
                            }
                        }
                    }
                }
            }
        }
    }
    mysql_free_result($result);
    return $matches;
}

?>