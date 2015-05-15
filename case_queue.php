<?php session_start(); ?>
<?php
if (!$_SESSION['case']['selected']) {
    header('location: case_list.php');
}
include_once './includes/database.php';
include_once './includes/counters.php';
include_once './includes/case_info.php';
include_once './includes/dump_info.php';
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
                    </div>
                </div>
            </div>
        </div>

        <div id="top_bar">
            <div class="wrapper cf">
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

                            <h1 class="sepH_c">Tasks</h1>

                            <table class="display" id="content_table">
                                <thead>
                                    <tr>
                                        <th><div class="th_wrapp">ID</div></th>
                                        <th><div class="th_wrapp">Command</div></th>
                                        <th><div class="th_wrapp">Priority</div></th>
                                        <th><div class="th_wrapp">Added</div></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php
                                    $query = "SELECT id, command, priority, added FROM queue WHERE ";
                                    foreach ($_SESSION['case']['dumps'] as $database) {
                                        $query .= "command LIKE '%" . $database . "%' OR ";
                                    }
                                    $query = trim($query);
                                    $query .= "DER BY priority, added";
                                    $result = mysqli_query($sqldb, $query);
                                    while ($row = mysqli_fetch_assoc($result)) {
                                        ?>
                                        <tr>
                                            <td><?php echo $row['id']; ?></td>
                                            <td><?php echo $row['command']; ?></td>
                                            <td><?php echo $row['priority']; ?></td>
                                            <td><?php echo $row['added']; ?></td>
                                        </tr>
                                        <?php
                                    }
                                    ?>
                                </tbody>
                            </table>

                        </div>
                    </div>

                    <div id="sidebar">
                        <div class="micro">
                            <h4><span>Current case</span></h4>
                            <ul class="sub_section cf">
                                <li><a href="case.php">Overview</a></li>
                                <li class="active"><a href="case_queue.php">Queue</a></li>
                                <li><a href="plugin_status.php">Plugin status</a></li>
                            </ul>
                        </div>
                        <div class="micro">
                            <h4><span>Plugins</span></h4>
                            <ul class="sub_section cf">
                                <?php plugin_submenu($plugin); ?>
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
                        $('#content_table').dataTable({
                            "aaSorting": [[2, "asc"]]
                        });
                    }
            )
        </script>
    </body>
</html>