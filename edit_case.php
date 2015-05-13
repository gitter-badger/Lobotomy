<?php
session_start();
ini_set('error_reporting', E_ALL);
error_reporting(-1);
include_once './includes/database.php';
include_once './includes/counters.php';

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    $query = "INSERT INTO cases "
            . "                 (name, description, creator, added)"
            . "                 VALUES"
            . "                     ("
            . "                      '" . mysqli_real_escape_string($_POST['case_name']) . "',"
            . "                      '" . mysqli_real_escape_string($_POST['case_description']) . "',"
            . "                      '" . mysqli_real_escape_string($_POST['case_creator']) . "',"
            . "                      NOW()"
            . "                     )";
    $result = mysqli_query($sqldb, $query);
    $case_id = mysqli_insert_id();

    if (isset($_POST['case_dumps']) && !empty($_POST['case_dumps'])) {
        foreach ($_POST['case_dumps'] as $dbase) {
            mysqli_query($sqldb, "UPDATE dumps SET case_assigned=" . $case_id . " WHERE dbase='" . $dbase . "'");
            mysqli_select_db($sqldb, $dbase);
            mysqli_query($sqldb, "UPDATE settings SET caseid=".$case_id);
            mysqli_select_db($sqldb, "lobotomy");
        }
    }
    header('location: case_list.php');
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

                            <h1 class="sepH_c">Create new case</h1>

                            <form action="" class="js_submit" method="post">
                                <div class="formEl_a">
                                    <fieldset class="sepH_b">
                                        <div class="sepH_b">
                                            <label for="case_name" class="lbl_a">Name</label>
                                            <input type="text" id="case_name" name="case_name" class="inpt_a" />
                                            <span class="f_help">The name or internally used code with which the case can be identified</span>
                                        </div>
                                        <div class="sepH_b">
                                            <label for="case_description" class="lbl_a">Description</label>
                                            <textarea id="case_description" name="case_description" cols="30" rows="10"></textarea>
                                            <span class="f_help">A short description about this case</span>
                                        </div>
                                        <div class="sepH_b">
                                            <label for="case_creator" class="lbl_a">Investigator</label>
                                            <select name="case_creator" id="case_creator">
                                                <option></option>
                                                <option value="wim">Wim Venhuizen</option>
                                                <option value="jeroen">Jeroen Hagebeek</option>
                                                <option value="marco">Marco van Loosen</option>
                                            </select>
                                            <span class="f_help">The case leader</span>
                                        </div>
                                        <?php
                                        if ($counter['unassigned_dumps'] > 0) {
                                            echo '<div class="sepH_c">' . PHP_EOL;
                                            echo '<label for="case_dumps" class="lbl_a">Assign memory dumps (Optional)</label>' . PHP_EOL;
                                            echo '<select name="case_dumps[]" id="case_dumps" multiple="multiple">' . PHP_EOL;
                                            $query = "SELECT dbase FROM dumps WHERE case_assigned=0 ORDER BY dbase DESC";
                                            $result = mysqli_query($sqldb, $query);
                                            while ($row = mysqli_fetch_assoc($result)) {
                                                echo '<option value="' . $row['dbase'] . '">' . $row['dbase'] . '</option>' . PHP_EOL;
                                            }
                                            echo '</select>' . PHP_EOL;
                                            echo '<span class="f_help">Optional: assign existing memory dumps to this case</span>' . PHP_EOL;
                                            echo '</div>' . PHP_EOL;
                                        }
                                        ?>
                                        <button type="submit" class="btn btn_c sepV_a"><span>Create</span></button>
                                    </fieldset>
                                </div>
                            </form>
                        </div>
                    </div>

                    <div id="sidebar">
                        <div class="micro">
                            <h4><span>Lobotomy</span></h4>
                            <ul class="sub_section cf" style="display:none">
                                <li><a href="dashboard.php">Dashboard</a></li>
                                <li class="active"><a href="case_list.php">Cases</a></li>
                                <li><a href="el_buttons.html">Buttons</a></li>
                                <li><a href="calendar.html">Calendar</a></li>
                                <li><a href="charts.html">Charts</a></li>
                                <li><a href="el_slider.html">Content Slider</a></li>
                                <li><a href="el_faq.html">Faq/Help</a></li>
                                <li><a href="file_explorer.html">File explorer</a></li>
                                <li><a href="form.html">Form</a></li>
                                <li><a href="form_elements.html">Form elements</a></li>
                                <li><a href="el_grid.html">Grid</a></li>
                                <li><a href="el_graphics.html">Icons &amp; Ajax loadears</a></li>
                                <li><a href="el_gallery.html">Image Gallery</a></li>
                                <li><a href="el_modals.html">Modals &amp; Overlays</a></li>
                                <li><a href="el_pricing_table.html">Pricing table</a></li>
                                <li><a href="el_tables.html">Tables</a></li>
                                <li><a href="wizard.html">Step By Step Wizard</a></li>
                                <li><a href="el_typography.html">Typography &amp; text styling</a></li>
                                <li><a href="el_widgets.html">Widgets</a></li>
                            </ul>
                        </div>
                        <div class="micro">
                            <h4><span>Error pages</span></h4>
                            <ul class="sub_section cf" style="display:none">
                                <li><a href="error_unexpected.html">Unexpected error</a></li>
                                <li><a href="error_401.html">Error 401</a></li>
                                <li><a href="error_403.html">Error 403</a></li>
                                <li><a href="error_404.html">Error 404</a></li>
                                <li><a href="error_500.html">Error 500</a></li>
                                <li><a href="error_503.html">Error 503</a></li>
                            </ul>
                        </div>
                        <div class="micro">
                            <h4><span>Sub-levels</span></h4>
                            <ul class="sub_section cf" style="display:none">
                                <li class="parent">
                                    <ul>
                                        <li><a href="#">Level 1</a></li>
                                        <li><a href="#">Level 2</a></li>
                                        <li><a href="#">Level 2</a></li>
                                        <li class="parent">
                                            <ul>
                                                <li><a href="#">Level 3</a></li>
                                                <li><a href="#">Level 3</a></li>
                                                <li class="parent">
                                                    <ul>
                                                        <li><a href="#">Level 4 long title test long title test</a></li>
                                                        <li><a href="#">Level 4</a></li>
                                                        <li><a href="#">Level 4</a></li>
                                                        <li><a href="#">Level 4</a></li>
                                                        <li><a href="#">Level 4</a></li>
                                                        <li><a href="#">Level 4</a></li>
                                                    </ul>
                                                </li>
                                                <li><a href="#">Level 3</a></li>
                                            </ul>
                                        </li>
                                    </ul>
                                </li>
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