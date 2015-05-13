<?php
function search_image($srch, $timeline = 0, $dbase = null) {
    $matches = array();
    if ($srch == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $result = mysqli_list_tables($dbase) or die(mysqli_error());
    $num_rows = mysqli_num_rows($result) or die(mysqli_error());
    for ($i = 0; $i < $num_rows; $i++) {
        $table = mysqli_tablename($result, $i) or die(mysqli_error());
        if ($table != 'settings' && $table != 'plugins' && $table != 'preferences') {
            if ($table == 'memtimeliner') {
                if ($timeline != 1) {
                    break;
                }
            }
            $result2 = mysqli_query($sqldb, "SHOW COLUMNS FROM " . $table) or die(mysqli_error());
            if (mysqli_num_rows($result2) > 0) {
                while ($row2 = mysqli_fetch_assoc($result2)) {
                    $_query = "SELECT id FROM `" . $table . "` WHERE `" . $row2['Field'] . "` LIKE CONCAT('%', CAST('" . mysqli_real_escape_string($sqldb, $srch) . "' as CHAR),'%')";
                    $_result = mysqli_query($sqldb, $_query) or die(mysqli_error());
                    if (mysqli_num_rows($_result) > 0) {
                        while ($_row = mysqli_fetch_assoc($_result)) {
                            $matches[$dbase][$table][] = $_row['id'];
                        }
                    }
                }
            }
        }
    }
    mysqli_free_result($result);
    return $matches;
}

function search_strings($srch, $dbase = null) {
    $matches = array();
    if ($srch == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $table = 'strings';
    $result2 = mysqli_query($sqldb, "SHOW COLUMNS FROM " . $table) or die(mysqli_error());
    if (mysqli_num_rows($result2) > 0) {
        while ($row2 = mysqli_fetch_assoc($result2)) {
            $_query = "SELECT id FROM `" . $table . "` WHERE `" . $row2['Field'] . "` LIKE CONCAT('%', CAST('" . mysqli_real_escape_string($sqldb, $srch) . "' as CHAR),'%')";
            $_result = mysqli_query($sqldb, $_query) or die(mysqli_error());
            if (mysqli_num_rows($_result) > 0) {
                while ($_row = mysqli_fetch_assoc($_result)) {
                    $matches[$dbase][$table][] = $_row['id'];
                }
            }
        }
    }
    mysqli_free_result($result);
    return $matches;
}

function search_pid($pid, $dbase = null) {
    $matches = array();
    if ($pid == '') {
        return $matches;
    }
    $dbase = isset($dbase) ? $dbase : $_SESSION['dump']['dbase'];
    $result = mysqli_list_tables($dbase) or die(mysqli_error());
    $num_rows = mysqli_num_rows($result) or die(mysqli_error());
    for ($i = 0; $i < $num_rows; $i++) {
        $table = mysqli_tablename($result, $i) or die(mysqli_error());
        if ($table != 'settings' && $table != 'memtimeliner' && $table != 'preferences') {
            $result2 = mysqli_query($sqldb, "SHOW COLUMNS FROM " . $table) or die(mysqli_error());
            if (mysqli_num_rows($result2) > 0) {
                while ($row2 = mysqli_fetch_assoc($result2)) {
                    if ($row2['Field'] == 'pid') {
                        $_query = "SELECT id FROM `" . $table . "` WHERE `pid` = '" . mysqli_real_escape_string($sqldb, $pid) . "'";
                        $_result = mysqli_query($sqldb, $_query) or die(mysqli_error());
                        if (mysqli_num_rows($_result) > 0) {
                            while ($_row = mysqli_fetch_assoc($_result)) {
                                $matches[$dbase][$table][] = $_row['id'];
                            }
                        }
                    }
                }
            }
        }
    }
    mysqli_free_result($result);
    return $matches;
}

?>