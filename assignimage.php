<?php
session_start();
include_once './includes/database.php';
include_once './includes/counters.php';
include_once './includes/case_info.php';

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (isset($_POST['case_dumps']) && !empty($_POST['case_dumps'])) {
        foreach ($_POST['case_dumps'] as $dbase) {
            mysqli_query($sqldb, "UPDATE dumps SET case_assigned=" . $_SESSION['case']['id'] . " WHERE dbase='" . $dbase . "'");
            mysqli_select_db($sqldb, $dbase);
            mysqli_query($sqldb, "UPDATE settings SET caseid=".$_SESSION['case']['id']);
            mysqli_select_db($sqldb, "lobotomy");
        }
    }
    header('location: case.php');
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns = "http://www.w3.org/1999/xhtml" xml:lang = "en">
    <head>
        <meta http-equiv = "Content-Type" content = "text/html;charset=UTF-8" />
        <title>Lobotomy</title>
        <link rel = "shortcut icon" href = "favicon.ico" />

        <link rel = "stylesheet" href = "css/style.css" media = "all" type = "text/css" />
        <link rel = "stylesheet" href = "http://fonts.googleapis.com/css?family=Open+Sans" type = "text/css" />

        <script type = "text/javascript" src = "js/head.load.min.js"></script>
        <script type="text/javascript" src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    </head>
    <body class="bg_c sidebar">

        <div id="slide_wrapper">
            <div id="slide_panel" class="wrapper">
                <div id="slide_content">
                    <span id="slide_close"><img src="images/blank.gif" alt="" class="round_x16_b" /></span>

                    <div class="cf">
                        <div class="dp100 sortable"><p class="s_color tac sepH_a">You can drag widgets from dashboard and drop it here.</p></div>
                    </div>

                    <div class="row cf">
                        <div class="dp75 taj">
                            <h4 class="sepH_b">Lorem ipsum dolor sit amet...</h4>
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam enim diam, vulputate vitae pharetra vel, pretium dictum ligula. In mauris eros, aliquam sit amet ullamcorper id, dictum eget ipsum. Nulla non porta arcu. Pellentesque faucibus, erat id interdum accumsan, neque magna ultrices ante, at laoreet lorem sem sit amet risus. Proin quis turpis ac nulla faucibus luctus at ac nisl. Suspendisse adipiscing turpis non risus tempus sit amet rhoncus est luctus. Cras in accumsan nulla. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam enim diam, vulputate vitae pharetra vel, pretium dictum ligula. In mauris eros, aliquam sit amet ullamcorper id, dictum eget ipsum. Nulla non porta arcu. Pellentesque faucibus, erat id interdum accumsan, neque magna ultrices ante, at laoreet lorem sem sit amet risus. Proin quis turpis ac nulla faucibus luctus at ac nisl. Suspendisse adipiscing turpis non risus tempus sit amet rhoncus est luctus. Cras in accumsan nulla.
                        </div>
                        <div class="dp25">
                            <div id="chart_k"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

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
                    <li class="nav_item active" title="Return to the main overview"><a href="dashboard.php" class="main_link"><img class="img_holder" style="background-image: url(images/icons/computer_imac.png)" alt="" src="images/blank.gif"/><span>Dashboard</span></a><img class="tick tick_a" alt="" src="images/blank.gif" /></li>
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
                            <ul class="first">
                                <li><a href="dashboard.php">Dashboard</a></li>
                            </ul>
                        </li>
                        <li class="parent">
                            <a href="case_list.php">Cases</a>
                            <ul>
                                <li><a href="case_list.php">Overview</a></li>
                                <li><a href="new_case.php">Create new case</a></li>
                            </ul>
                        </li>
                        <li class="current"><a href="new_case.php">Create new case</a></li>
                    </ul>

                    <div id="content_wrapper">
                        <div id="main_content" class="cf">

                            <h1 class="sepH_c">Assign image to <?php echo $_SESSION['case']['name']; ?></h1>

                            <form action="" class="js_submit" method="post">
                                <div class="formEl_a">
                                    <fieldset class="sepH_b">
                                        <?php
                                        if ($counter['unassigned_dumps'] > 0) {
                                            echo '<div class="sepH_c">' . PHP_EOL;
                                            echo '<label for="case_dumps" class="lbl_a">Assign memory image(s)</label>' . PHP_EOL;
                                            echo '<select name="case_dumps[]" id="case_dumps" multiple="multiple">' . PHP_EOL;
                                            $query = "SELECT dbase FROM dumps WHERE case_assigned=0 ORDER BY dbase DESC";
                                            $result = mysqli_query($sqldb, $query);
                                            while ($row = mysqli_fetch_assoc($result)) {
                                                echo '<option value="' . $row['dbase'] . '">' . $row['dbase'] . '</option>' . PHP_EOL;
                                            }
                                            echo '</select>' . PHP_EOL;
                                            echo '<span class="f_help">Select the images to assign to this case. Multiple selections allowed.</span>' . PHP_EOL;
                                            echo '</div>' . PHP_EOL;
                                            echo '<button type="submit" class="btn btn_c sepV_a"><span>Assign</span></button>'.PHP_EOL;
                                        }
                                        else {
                                            echo '<h4>There are no unassigned images available.</h4>';
                                        }
                                        ?>
                                    </fieldset>
                                </div>
                            </form>
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
                    "lib/fusion-charts/FusionCharts.js",
                    "js/jquery.microaccordion.js",
                    "js/jquery.stickyPanel.js",
                    "js/jquery.tools.min.js",
                    "js/xbreadcrumbs.js",
                    "js/lagu.js",
                    function () {
                        lga_fusionCharts.chart_k();
                    }
            )
        </script>

    </body>
</html>