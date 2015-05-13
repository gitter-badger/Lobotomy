<?php session_start(); ?>
<?php
include './includes/filters.php';
if (isset($_GET['case']) && isset($_GET['image'])) {
    if (ctype_digit($_GET['case']) && ctype_digit($_GET['image'])) {
        $_SESSION['case']['id'] = $_GET['case'];
        $_SESSION['dump']['id'] = $_GET['image'];
        $_SESSION['case']['selected'] = True;
        $_SESSION['dump']['selected'] = True;
        header('location: plugin.php?name=' . $_GET['name']);
    }
}
if (!$_SESSION['dump']['selected']) {
    header('location: case.php');
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
                            <ul>
                                <li><a href="#">Articles</a></li>
                                <li><a href="#">Pages</a></li>
                                <li><a href="#">Custom content</a></li>
                            </ul>
                        </li>
                    </ul>

                    <div id="content_wrapper">
                        <div id="main_content" class="cf">
                            <a href="javascript:copyToClipboard('<?php echo $_SERVER['SERVER_ADDR'] . $_SERVER['REQUEST_URI']; ?>&case=<?php echo $_SESSION['case']['id']; ?>&image=<?php echo $_SESSION['dump']['id']; ?>')" class="btn btn_a fl sepV_a"><span class="btnImg" style="background-image: url('images/icons/link.png');">Permalink</span></a>
                            <div class="cf">
                                <h4 class="sepH_a"><?php echo $plugin; ?> - <?php echo $case['name']; ?> - 
                                    <select id="dump_select">
                                        <?php
                                        foreach ($_SESSION['case']['dumps'] as $database) {
                                            $select_query = "SELECT id, dbase FROM dumps WHERE dbase='" . mysqli_real_escape_string($database) . "'";
                                            $select_result = mysqli_query($sqldb, $select_query);
                                            $select_row = mysqli_fetch_assoc($select_result);
                                            if ($_SESSION['dump']['dbase'] == $select_row['dbase']) {
                                                echo '<option id="' . $select_row['id'] . '" selected="selected" />' . $select_row['dbase'] . '</option>';
                                            } else {
                                                echo '<option value="' . $select_row['id'] . '" />' . $select_row['dbase'] . '</option>';
                                            }
                                        }
                                        ?>
                                    </select>
                                </h4>
                                <div class="sepH_a_line"></div>
                                <?php plugin_include($plugin); ?>
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
                        $('#data_table').dataTable({
                            aaSorting: [],
                            "autoWidth": true,
                            "iDisplayLength": 50,
                            "scrollX": "200px"
                        });
                        $('#dump_select').bind('change', function () {
                            var url = 'plugin.php?name=<?php echo $_GET['name']; ?>&case=<?php echo $_SESSION['case']['id']; ?>&image=' + $('select[id=dump_select]').val(); // get selected value
                            if (url) { // require a URL
                                window.location = url; // redirect
                            }
                            return false;
                        });
                        $('#dropdown').bind('change', function () {
                            var url = 'plugin.php?name=xxd&ID=' + $('select[id=dropdown]').val() + '&plugin=dlldump'; // get selected value
                            if (url) { // require a URL
                                window.location = url; // redirect
                            }
                            return false;
                        });
                        $('#data_table tbody tr td a').click(function (e) {
                            e.stopPropagation();
                        });
                        $('#data_table tbody').on('click', 'tr', function () {
                            if ($(this).hasClass("marked")) {
                                $(this).removeClass('marked');
                                $.ajax({
                                    url: "./includes/mark.php",
                                    type: "get", //send it through get method
                                    data: {mode: 0,
                                        id: $(this).attr('id'),
                                        plugin: '<?php echo $plugin; ?>',
                                        db: '<?php echo $_SESSION['dump']['dbase']; ?>'
                                    }
                                });
                            }
                            else {
                                $(this).removeClass();
                                $(this).addClass('marked');
                                $.ajax({
                                    url: "./includes/mark.php",
                                    type: "get", //send it through get method
                                    data: {mode: 1,
                                        id: $(this).attr('id'),
                                        plugin: '<?php echo $plugin; ?>',
                                        db: '<?php echo $_SESSION['dump']['dbase']; ?>'
                                    }
                                });
                            }
                        });
                        $("#hivedump").click(function () {
                            $("tr.marked").each(function (i) {
                                if (!$(this).hasClass("done")) {
                                    $.ajax({
                                        url: "./includes/mark.php",
                                        type: "get", //send it through get method
                                        data: {mode: 2,
                                            id: $(this).attr('id'),
                                            plugin: '<?php echo $plugin; ?>',
                                            db: '<?php echo $_SESSION['dump']['dbase']; ?>'
                                        }
                                    });
                                    $.ajax({
                                        url: "./includes/add_queue.php",
                                        type: "get", //send it through get method
                                        data: {
                                            offset: $(this).data("offset"),
                                            db: '<?php echo $_SESSION['dump']['dbase']; ?>',
                                            mode: 0
                                        }
                                    });
                                    $(this).removeClass('marked');
                                    $(this).addClass('done');
                                }
                            });
                        });
                        $("#printkey").click(function () {
                            $("tr.marked").each(function (i) {
                                if (!$(this).hasClass("done")) {
                                    $.ajax({
                                        url: "./includes/mark.php",
                                        type: "get", //send it through get method
                                        data: {mode: 2,
                                            id: $(this).attr('id'),
                                            plugin: '<?php echo $plugin; ?>',
                                            db: '<?php echo $_SESSION['dump']['dbase']; ?>'
                                        }
                                    });
                                    $.ajax({
                                        url: "./includes/add_queue.php",
                                        type: "get", //send it through get method
                                        data: {
                                            id: $(this).attr('id'),
                                            db: '<?php echo $_SESSION['dump']['dbase']; ?>',
                                            mode: 1
                                        }
                                    });
                                    $(this).removeClass('marked');
                                    $(this).addClass('done');
                                }
                            });
                        });
                    }
            );

        </script>

    </body>
</html>