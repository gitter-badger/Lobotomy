<?php
session_start();
include_once './includes/database.php';
include_once './includes/counters.php';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
        <title>Lobotomy</title>
        <link rel="shortcut icon" href="favicon.ico" />

        <link rel="stylesheet" href="css/style.css" media="all" type="text/css" />
        <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Open+Sans" type="text/css" />

        <script type="text/javascript" src="js/head.load.min.js"></script>
        <script type="text/javascript" src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
        <script>
            $(document).ready(
                    function () {
                        setInterval(function () {
                            var randomnumber = Math.floor(Math.random() * 100);
                            $('#tasks').load("tasks.php");
                        }, 1000);
                    });
            $(document).ready(
                    function () {
                        setInterval(function () {
                            var randomnumber = Math.floor(Math.random() * 100);
                            $('#summary').load("summary.php");
                        }, 1000);
                    }
            );

            var random_images_array = ["ajax_red.gif", "ajax_blue.gif", "ajax_green.gif", "ajax_yellow.gif", "ajax_gray.gif", "ajax_black.gif"];
            function getRandomImage(imgAr, path) {
                path = path || 'images/';
                var num = Math.floor(Math.random() * imgAr.length);
                var img = imgAr[ num ];
                var imgStr = '<img src="' + path + img + '" alt = "Loading..">';
                document.write(imgStr);
                document.close();
            }
        </script>
    </head>
    <body class="bg_c sidebar">
        <div id="top_bar">
            <div class="wrapper cf">
                <ul class="new_items fr">
                    <li class="sep"><span class="count_el"><?php echo $counter['unassigned_dumps']; ?></span> unassigned memory dumps</li>
                    <li class="sep"><span class="count_el"><?php echo $counter['tasks_pending']; ?></span> tasks in queue</li>
                </ul>
            </div>
        </div>

        <div id="header">
            <div class="wrapper cf">
                <div class="logo fl">
                    <a href="#"><img src="images/logo.png" alt="" /></a>
                </div>
                <ul class="fr cf" id="main_nav">
                    <li class="nav_item" title="Return to the dashboard"><a href="dashboard.php" class="main_link"><img class="img_holder" style="background-image: url(images/icons/computer_imac.png)" alt="" src="images/blank.gif"/><span>Dashboard</span></a><img class="tick tick_a" alt="" src="images/blank.gif" /></li>
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
                    </ul>

                    <div id="content_wrapper">
                        <div id="main_content">
                            <div class="cf">
                                <div class="dp50 sortable">
                                    <div class="box_c">
                                        <h3 class="box_c_heading cf">
                                            <span class="fl">Summary</span>
                                            <img src="images/blank.gif" alt="" class="fr square_x_11 wRemove" />
                                            <img src="images/blank.gif" alt="" class="fr switch_arrows_a wToogle" />
                                        </h3>
                                        <div class="box_c_content cf" id="summary">
                                            <script type="text/javascript">getRandomImage(random_images_array);</script>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <h1 class="sepH_c">Tasks</h1>
                            <div id="tasks">
                                <script type="text/javascript">getRandomImage(random_images_array);</script>
                            </div>

                            <div class="cf">
                                <div class="sortable dp100"></div>
                            </div>

                        </div>
                    </div>

                </div>
            </div>
        </div>

        <div id="footer">
            <div class="wrapper">
                <div class="cf ftr_content">
                    <p class="fl">Copyright &copy; 2015 Wim Venhuizen en Jeroen Hagebeek.</p>
                    <a href="javascript:void(0)" class="toTop">Back to top</a>
                </div>
            </div>
        </div>

        <script type="text/javascript">
            head.js(
                    "js/jquery-1.6.2.min.js",
                    "lib/jquery-ui/jquery-ui-1.8.15.custom.min.js",
                    "js/jquery.tools.min.js",
                    "js/jquery.stickyPanel.js",
                    "js/jquery.text-overflow.min.js",
                    "js/xbreadcrumbs.js",
                    "js/lagu.js",
            )
        </script>

    </body>
</html>
