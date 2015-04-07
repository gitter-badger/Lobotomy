<?php session_start(); ?>
<?php
include_once './includes/database.php';
include_once './includes/counters.php';
include_once './includes/case_info.php';
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
    </head>
    <body>


        <div id="main">
            <div class="wrapper">
                <div id="main_section" class="cf brdrrad_a">

                    <div id="content_wrapper">
                        <div id="main_content" class="cf">
                            <div class="cf">
                                <?php
                                    mysql_select_db("1501260808_memfor3novvmem");
                                    $query = "SELECT date, size, type, mode, uid, gid, meta, filename FROM memtimeliner";
                                    $result = mysql_query($query);
                                    ?>
                                    <table cellpadding="0" cellspacing="0" border="0" class="display" id="data_table">
                                        <thead>
                                            <tr>
                                                <th class="chb_col">
                                                    <div class="th_wrapp">Date</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">Size</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">Type</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">Mode</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">UID</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">GID</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">Meta</div>
                                                </th>
                                                <th>
                                                    <div class="th_wrapp">Filename</div>
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <?php
                                            while ($row = mysql_fetch_assoc($result)) {
                                                ?>
                                                <tr>
                                                    <td><?php echo $row['date']; ?></td>
                                                    <td><?php echo $row['size']; ?></td>
                                                    <td><?php echo $row['type']; ?></td>
                                                    <td><?php echo $row['mode']; ?></td>
                                                    <td><?php echo $row['uid']; ?></td>
                                                    <td><?php echo $row['gid']; ?></td>
                                                    <td><?php echo $row['meta']; ?></td>
                                                    <td><?php echo $row['filename']; ?></td>
                                                </tr>
                                                <?php
                                            }
                                            ?>
                                        </tbody>
                                    </table>
                            </div>

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
                    "lib/fusion-charts/FusionCharts.js",
                    "js/jquery.microaccordion.js",
                    "js/jquery.stickyPanel.js",
                    "js/xbreadcrumbs.js",
                    "js/lagu.js",
                    function () {
                        var table = $('#data_table').dataTable({
                            aaSorting: [],
                            "iDisplayLength": 100,
                            "scrollX": "200px"
                        });
                        new $.fn.dataTable.FixedHeader(table);
                    }
            );
        </script>

    </body>
</html>