<?php
session_start();
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
                    <li class="sep"><a href="login.html">Logout</a></li>
                    <li><a href="#">Front End Preview</a></li>
                </ul>
                <ul class="new_items fr">
                    <li class="sep"><span class="count_el">2</span> <a href="#">new messages</a></li>
                    <li class="sep"><span class="count_el">10</span> <a href="#">new comments</a></li>
                    <li class="sep"><span class="count_el">4</span> <a href="#">tasks</a></li>
                    <li id="slide_open">sliding panel<img src="images/blank.gif" alt="" class="arrow_down_a" /></li>
                </ul>
            </div>
        </div>

        <div id="header">
            <div class="wrapper cf">
                <div class="logo fl">
                    <a href="#"><img src="images/logo.png" alt="" /></a>
                </div>
                <ul class="fr cf" id="main_nav">
                    <li class="nav_item"><a href="dashboard.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/computer_imac.png)" alt="" src="images/blank.gif"/><span>Dashboard</span></a></li>
                    <li class="nav_item"><a href="content.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/file_cabinet.png)" alt="" src="images/blank.gif"/><span>Content</span></a></li>
                    <li class="nav_item"><a href="file_explorer.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/image2_2.png)" alt="" src="images/blank.gif"/><span>Media library</span></a></li>
                    <li class="nav_item"><a href="users.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/users2.png)" alt="" src="images/blank.gif"/><span>Users</span></a></li>
                    <li class="nav_item active"><a href="tasks.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/create_write.png)" alt="" src="images/blank.gif"/><span>Tasks</span></a><img class="tick tick_a" alt="" src="images/blank.gif" /></li>
                    <li class="nav_item"><a href="charts.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/chart8.png)" alt="" src="images/blank.gif"/><span>Reports</span></a></li>
                    <li class="nav_item"><a href="../documentation/index.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/help.png)" alt="" src="images/blank.gif"/><span>Documentation</span></a></li>
                </ul>
            </div>
        </div>

        <div id="main">
            <div class="wrapper cf">
                <div id="main_section" class="cf brdrrad_a">

                    <ul id="breadcrumbs" class="xbreadcrumbs cf">
                        <li class="parent">
                            <img src="images/blank.gif" alt="" class="sepV_a vam home_ico" />
                            <a href="dashboard.html" class="vam">Lobotomy</a>
                            <ul class="first">
                                <li><a href="#">Content</a></li>
                                <li><a href="#">Media library</a></li>
                                <li><a href="#">Users</a></li>
                                <li><a href="#">Tasks</a></li>
                                <li><a href="#">Reports</a></li>
                                <li><a href="#">Settings</a></li>
                            </ul>
                        </li>
                        <li class="parent">
                            <a href="#">Content</a>
                            <ul>
                                <li><a href="#">Articles</a></li>
                                <li><a href="#">Pages</a></li>
                                <li><a href="#">Custom content</a></li>
                            </ul>
                        </li>
                        <li class="parent">
                            <a href="#">Articles</a>
                            <ul>
                                <li><a href="#">Show All</a></li>
                                <li><a href="#">Create new</a></li>
                            </ul>
                        </li>
                        <li class="current"><a href="#">Contact page</a></li>
                    </ul>

                    <div id="content_wrapper">
                        <div id="main_content" class="cf">

                            <h1 class="sepH_c">Tasks</h1>

                            <table class="display" id="content_table">
                                <thead>
                                    <tr>
                                        <th><div class="th_wrapp">Title</div></th>
                                        <th><div class="th_wrapp">id</div></th>
                                        <th><div class="th_wrapp">Assigned to</div></th>
                                        <th><div class="th_wrapp">Priority</div></th>
                                        <th><div class="th_wrapp">Deadline</div></th>
                                        <th><div class="th_wrapp">Info</div></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td><a href="#"><del>First task longer title...</del></a></td>
                                        <td><a href="#" class="small"><del>lagu-123</del></a></td>
                                        <td>Lisa A. Robinson</td>
                                        <td class="small">Low</td>
                                        <td>21/10/2011</td>
                                        <td><span class="notification ok_bg">Closed</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Second task</a></td>
                                        <td><a href="#" class="small">lagu-223</a></td>
                                        <td>Francis H. Lamons</td>
                                        <td class="small bld">High</td>
                                        <td>25/09/2011</td>
                                        <td><span class="notification info_bg">New task</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Third task</a></td>
                                        <td><a href="#" class="small">sam-12</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small bld">High</td>
                                        <td>23/09/2011</td>
                                        <td><span class="notification error_bg">Blocker</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#"><del>Fourth task longer title than third task...</del></a></td>
                                        <td><a href="#" class="small"><del>lg-3</del></a></td>
                                        <td>Donna C. Lindsay</td>
                                        <td class="small">Medium</td>
                                        <td>18/09/2011</td>
                                        <td><span class="notification ok_bg">Closed</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Fifth task</a></td>
                                        <td><a href="#" class="small">proj-23</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification alert_bg">Reopened</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#"><del>Another task</del></a></td>
                                        <td><a href="#" class="small"><del>another-123</del></a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification ok_bg">Closed</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Another task</a></td>
                                        <td><a href="#" class="small">another-123</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Medium</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification info_bg">In progress</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Another task</a></td>
                                        <td><a href="#" class="small">another-123</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification alert_bg">Reopened</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Another task</a></td>
                                        <td><a href="#" class="small">another-123</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Medium</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification info_bg">In progress</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#">Another task</a></td>
                                        <td><a href="#" class="small">another-123</a></td>
                                        <td>Dierdre F. Prisco</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification info_bg">New comment</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#"><del>Another task</del></a></td>
                                        <td><a href="#" class="small"><del>another-123</del></a></td>
                                        <td>Lisa A. Robinson</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification ok_bg">Closed</span></td>
                                    </tr>
                                    <tr>
                                        <td><a href="#"><del>Another task</del></a></td>
                                        <td><a href="#" class="small"><del>another-123</del></a></td>
                                        <td>Lisa A. Robinson</td>
                                        <td class="small">Low</td>
                                        <td>16/09/2011</td>
                                        <td><span class="notification ok_bg">Closed</span></td>
                                    </tr>
                                </tbody>
                            </table>

                        </div>
                    </div>

                    <div id="sidebar">
                        <div class="micro">
                            <h4><span>Elements</span></h4>
                            <ul class="sub_section cf" style="display:none">
                                <li><a href="el_accordion.html">Accordion</a></li>
                                <li><a href="el_alerts.html">Alert boxes</a></li>
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
                    <p class="fl">Copyright &copy; 2012 tzd-themes.com</p>
                    <a href="javascript:void(0)" class="toTop">Back to top</a>
                </div>
            </div>
        </div>

        <script type="text/javascript">
            head.js(
                    "js/jquery-1.6.2.min.js",
                    "lib/datatables/jquery.dataTables.min.js",
                    "lib/datatables/dataTables.plugins.js",
                    "lib/fusion-charts/FusionCharts.js",
                    "js/jquery.microaccordion.js",
                    "js/jquery.stickyPanel.js",
                    "js/xbreadcrumbs.js",
                    "js/lagu.js",
                    function () {
                        lga_fusionCharts.chart_k();
                        $('#content_table').dataTable({
                            "aaSorting": [[3, "asc"]],
                            "aoColumns": [
                                {"sType": "string"},
                                {"sType": "html"},
                                {"sType": "string"},
                                {"sType": "priority"},
                                {"sType": "eu_date"},
                                {"sType": "html"}
                            ]
                        });
                    }
            )
        </script>
    </body>
</html>
