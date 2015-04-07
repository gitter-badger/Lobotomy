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
                    <li class="nav_item"><a href="tasks.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/create_write.png)" alt="" src="images/blank.gif"/><span>Tasks</span></a></li>
                    <li class="nav_item"><a href="charts.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/chart8.png)" alt="" src="images/blank.gif"/><span>Reports</span></a></li>
                    <li class="nav_item"><a href="../documentation/index.html" class="main_link"><img class="img_holder" style="background-image: url(images/icons/help.png)" alt="" src="images/blank.gif"/><span>Documentation</span></a></li>
                </ul>
            </div>
        </div>

        <div id="main">
            <div class="wrapper">
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

                            <div class="sepH_c">

                                <h1 class="sepH_c">Data Table</h1>

                                <div class="sepH_a">
                                    <a href="javascript:void(0)" class="delete_all_dt">Delete selected</a>
                                </div>

                                <table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
                                    <thead>
                                        <tr>
                                            <th><div class="th_wrapp">Timestamp</div></th>
                                            <th><div class="th_wrapp">Source</div></th>
                                            <th><div class="th_wrapp">Message</div></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php
                                        $f = fopen("/home/solvent/lobotomy.log", "r");
                                        while (($line = fgetcsv($f)) !== false) {
                                            echo "<tr>";
                                            foreach ($line as $cell) {
                                                echo "<td>" . htmlspecialchars($cell) . "</td>";
                                            }
                                            echo "</tr>\n";
                                        }
                                        ?>
                                    </tbody>
                                </table>
                            </div>

                            <h1 class="sepH_c">Simple Table</h1>

                            <div class="sepH_a">
                                <a href="javascript:void(0)" class="delete_all_simple">Delete selected</a>
                            </div>

                            <table cellpadding="0" cellspacing="0" border="0" class="table_a smpl_tbl">
                                <thead>
                                    <tr>
                                        <th class="chb_col"><div class="th_wrapp"><input type="checkbox" class="chSel_all inpt_c1" /></div></th>
                                        <th><div class="th_wrapp">Name</div></th>
                                        <th><div class="th_wrapp">Capital</div></th>
                                        <th><div class="th_wrapp">Population</div></th>
                                        <th><div class="th_wrapp">Area (km<sup>2</sup>)</div></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Albania</td>
                                        <td>Tirana</td>
                                        <td>2,986,952</td>
                                        <td>28,748</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Andora</td>
                                        <td>Andorra la Vella</td>
                                        <td>84,525</td>
                                        <td>468</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Armenia</td>
                                        <td>Yerevan</td>
                                        <td>2,966,802</td>
                                        <td>29,743</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Austria</td>
                                        <td>Vienna</td>
                                        <td>8,214,160</td>
                                        <td>83,871</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Azerbaijan</td>
                                        <td>Baku</td>
                                        <td>8,303,512</td>
                                        <td>86,600</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Belarus</td>
                                        <td>Minsk</td>
                                        <td>9,612,632</td>
                                        <td>207,600</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Belgium</td>
                                        <td>Brussels</td>
                                        <td>10,423,493</td>
                                        <td>30,528</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Bosnia and Herzegovina</td>
                                        <td>Sarajewo</td>
                                        <td>4,612,598</td>
                                        <td>51,197</td>
                                    </tr>
                                    <tr>
                                        <td class="chb_col"><input type="checkbox" name="row_sel" class="inpt_c1" /></td>
                                        <td>Bulgaria</td>
                                        <td>Sofia</td>
                                        <td>7,148,785</td>
                                        <td>110,879</td>
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
                                <li class="active"><a href="el_tables.html">Tables</a></li>
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
                        $('.chSel_all').click(function () {
                            $(this).closest('table').find('input[name=row_sel]').attr('checked', this.checked);
                        });
                        $(".delete_all_simple").click(function () {
                            $('input[name=row_sel]:checked', '.smpl_tbl').closest('tr').fadeTo(600, 0, function () {
                                $(this).remove();
                                $('.chSel_all', '.smpl_tbl').attr('checked', false);
                            });
                            return false;
                        });
                        $('.delete_all_dt').click(function () {
                            oTable = $('#data_table').dataTable();
                            $('input[@name=row_sel]:checked', oTable.fnGetNodes()).closest('tr').fadeTo(600, 0, function () {
                                oTable.fnDeleteRow(this);
                                $('.chSel_all', '#data_table').attr('checked', false);
                                return false;
                            });
                        });
                        $('#data_table').dataTable({
                            "aaSorting": [[1, "asc"]],
                            "aoColumns": [
                                {"bSortable": false},
                                null,
                                null,
                                {"sType": "formatted-num"},
                                {"sType": "formatted-num"}
                            ]
                        });
                    }
            )
        </script>
    </body>
</html>
