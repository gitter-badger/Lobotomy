<?php session_start(); ?>
<?php
if (!$_SESSION['dump']['selected']) {
    header('location: case.php');
}
include_once './includes/database.php';
include_once './includes/counters.php';
include_once './includes/case_info.php';
include_once './includes/dump_info.php';
include_once './includes/searchengine.php';
include_once './includes/plugin_settings.php';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
        <title>Lobotomy</title>
        <link rel="shortcut icon" href="favicon.ico" />

        <link rel="stylesheet" href="css/style.css" media="all" type="text/css" />
        <link rel="stylesheet" href="lib/datatables/css/table_jui.css" type="text/css" />
        <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans" type="text/css" />

        <script type="text/javascript" src="js/head.load.min.js"></script>
        <script type="text/javascript">
            function copyToClipboard(text) {
                window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
            }
        </script>
    </head>
    <body class="bg_c sidebar">

        <div id="top_bar">
            <div class="wrapper cf">
                <ul class="fl">
                    <li class="sep">Welcome <a href="#">Admin</a></li>
                    <li class="sep"><a href="login.php">Logout</a></li>
                    <li><a href="#">Front End Preview</a></li>
                </ul>
                <ul class="new_items fr">
                    <li class="sep"><span class="count_el"><?php echo $counter['unassigned_dumps']; ?></span> <a href="#">unassigned memory dumps</a></li>
                    <li class="sep"><span class="count_el"><?php echo $counter['tasks_pending']; ?></span> <a href="#">tasks in queue</a></li>
                </ul>
            </div>
        </div>

        <div id="header">
            <div class="wrapper cf">
                <div class="logo fl">
                    <a href="#"><img src="images/logo.png" alt="" /></a>
                </div>
                <ul class="fr cf" id="main_nav">
                    <li class="nav_item" title="Return to the main overview"><a href="dashboard.php" class="main_link"><img class="img_holder" style="background-image: url(images/icons/computer_imac.png)" alt="" src="images/blank.gif"/><span>Dashboard</span></a><img class="tick tick_a" alt="" src="images/blank.gif" /></li>
                    <li class="nav_item" title="Cases overview"><a href="case_list.php" class="main_link"><img class="img_holder" style="background-image: url(images/icons/file_cabinet.png)" alt="" src="images/blank.gif"/><span>Cases</span></a></li>
                </ul>
            </div>
        </div>

        <div id="main">
            <div class="wrapper">
                <div id="main_section" class="cf brdrrad_a">

                    <ul id="breadcrumbs" class="xbreadcrumbs cf">
                        <li class="parent">
                            <img src="images/blank.gif" alt="" class="sepV_a vam home_ico" />
                            <a href="dashboard.php" class="vam">Lobotomy</a>
                        </li>
                        <li class="parent">
                            <a href="case_list.php">Cases</a>
                        </li>
                        <li class="parent">
                            <a href="case.php"><?php echo $case['name']; ?></a>
                        </li>
                    </ul>

                    <div id="content_wrapper">
                        <div id="main_content" class="cf">
                            <div class="cf">
                                <h1 class="sepH_a">Search results</h1>
                                <?php
                                if (isset($_GET['q']) && !empty($_GET['q'])) {
                                    $value = $_GET['q'];
                                } else {
                                    $value = '';
                                }
                                $value = strip_tags($_GET['q']);
                                $value = htmlentities($value, ENT_QUOTES);
                                ?>
                                <form action="" method="get"><input type="text" name="q" value="<?php echo $value; ?>" size="80" /> Using &#37; as wildcard is allowed - Search as <input type="submit" value="String" name="type" /> <input type="submit" value="PID" name="type" /><br />
                                    <input type="checkbox" name="timeline" value="1" /> Include timeline in search - This can be slow!</form><br />
                                <?php
                                if ($value != '') {
                                    ?>
                                    <strong><a href="search_strings.php?q=<?php echo $_GET['q']; ?>">Search in image strings</a></strong> - This can be slow and/or return incorrect results!
                                    <?php
                                }
                                ?>
                                <div class="sepH_a_line"></div>
                                <?php
                                if (isset($_GET['timeline']) && !empty($_GET['timeline']) && $_GET['timeline'] == '1') {
                                    $timeline = 1;
                                } else {
                                    $timeline = 0;
                                }
                                if ($_GET['type'] == 'PID') {
                                    $res = search_pid($_GET['q']);
                                } else {
                                    $res = search_image($_GET['q'], $timeline);
                                }
                                if (count($res) > 0) {
                                    foreach ($res as $db => $table) {
                                        foreach ($table as $key => $value) {
                                            echo '<h3>Results in ' . $key . '</h3>' . PHP_EOL;
                                            echo '<table id="' . $key . '" class="display" cellpadding="0" cellspacing="0" border="0">' . PHP_EOL;
                                            echo '<thead>' . PHP_EOL;
                                            echo '<tr>' . PHP_EOL;
                                            $cresult = mysql_query("SHOW COLUMNS FROM `" . $key . "`");
                                            $i = 0;
                                            while ($crow = mysql_fetch_assoc($cresult)) {
                                                if ($i > 0) {
                                                    echo '<th class="chb_col"><div class="th_wrapp">' . $crow['Field'] . '</div></th>' . PHP_EOL;
                                                }
                                                $i++;
                                            }
                                            echo '</tr>' . PHP_EOL;
                                            echo '</thead>' . PHP_EOL;
                                            echo '<tbody>' . PHP_EOL;
                                            foreach ($value as $num => $idnum) {
                                                $rquery = "SELECT * FROM `" . $key . "` WHERE id=" . $idnum;
                                                $rresult = mysql_query($rquery);
                                                while ($rrow = mysql_fetch_row($rresult)) {
                                                    if (is_marked($key, $idnum)) {
                                                        echo '<tr id="' . $idnum . '" class="marked">' . PHP_EOL;
                                                    } else {
                                                        echo '<tr id="' . $idnum . '">' . PHP_EOL;
                                                    }
                                                    $i = 0;
                                                    foreach ($rrow as $_column) {
                                                        if ($i > 0) {
                                                            echo '<td><a href="search.php?q=' . $_column . '">' . $_column . '</a></td>' . PHP_EOL;
                                                        }
                                                        $i++;
                                                    }
                                                    echo "</tr>" . PHP_EOL;
                                                }
                                            }
                                            echo '</tbody>' . PHP_EOL;
                                            echo "</table>" . PHP_EOL;
                                        }
                                    }
                                } else {
                                    echo '<h4>No results returned</h4>';
                                }
                                ?>
                            </div>
                        </div>
                    </div>

                    <div id="sidebar">
                        <div class="micro">
                            <h4><span>Current case</span></h4>
                            <ul class="sub_section cf">
                                <li><a href="case.php">Overview</a></li>
                                <li><a href="case_queue.php">Queue</a></li>
                                <li><a href="plugin_status.php">Plugin status</a></li>
                            </ul>
                        </div>
                        <div class="micro">
                            <h4><span>Plugins</span></h4>
                            <ul class="sub_section cf">
                                <?php plugin_submenu($plugin, 1); ?>
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div id="footer">
            <div class="wrapper">
                <div class="cf ftr_content">
                    <p class="fl">Copyright &copy; 2015 Wim Venhuizen en Jeroen Hagebeek</p>
                    <a href="javascript:void(0)" class="toTop">Back to top</a>
                </div>
            </div>
        </div>

        <script type="text/javascript">
            head.js(
                    "js/jquery-1.6.2.min.js",
                    "lib/datatables/jquery.dataTables.min.js",
                    "lib/datatables/dataTables.plugins.js",
                    "js/jquery.stickyPanel.js",
                    "js/xbreadcrumbs.js",
                    "js/lagu.js",
                    function () {
                        $('table tbody tr a').click(function (e) {
                            e.stopPropagation();
                        });
                    }
            );
        </script>
    </body>
</html>