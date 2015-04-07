<?php

function startsWith($haystack, $needle) {
    // search backwards starting from haystack length characters from the end
    return $needle === "" || strrpos($haystack, $needle, -strlen($haystack)) !== FALSE;
}

function endsWith($haystack, $needle) {
    // search forward starting from end minus needle length characters
    return $needle === "" || (($temp = strlen($haystack) - strlen($needle)) >= 0 && strpos($haystack, $needle, $temp) !== FALSE);
}

function init_filters($file) {
    $filter = array();
    $handle = @fopen($file, "r");
    $line = 1;
    $in_block = False;
    $block_num = 0;
    if ($handle) {
        while (($buffer = fgets($handle, 4096)) !== false) {
            if (!startsWith($buffer, '#') && $buffer != '') {
                $buffer = trim($buffer);
                $ptn = "/@(.*) {/";
                $str = $buffer;
                preg_match($ptn, $str, $matches);
                if (!empty($matches[1])) {
                    $plugin = trim($matches[1]);
                    $in_block = $plugin;
                    $block_num++;
                } else {
                    if (startsWith($buffer, '}')) {
                        $in_block = False;
                    }
                }
                if ($in_block) {
                    if (!startswith($buffer, '__') && !startswith($buffer, '@') && !startswith($buffer, '}')) {
                        $tmp = explode(':', $buffer, 2);
                        $field = trim($tmp[0]);
                        $value = trim($tmp[1]);
                        $filter[$in_block][$block_num][$field] = $value;
                    }
                    if (strpos($buffer, '__match') !== false) {
                        $tmp = explode(':', $buffer, 2);
                        $field = trim($tmp[0]);
                        $value = trim($tmp[1]);
                        $filter[$in_block][$block_num]['__match'] = $value;
                    }
                    if (strpos($buffer, '__type') !== false) {
                        $tmp = explode(':', $buffer, 2);
                        $field = trim($tmp[0]);
                        $value = trim($tmp[1]);
                        $filter[$in_block][$block_num]['__type'] = $value;
                    }
                }
            }
        }
        if (!feof($handle)) {
            echo "Error: unexpected fgets() fail\n";
        }
        fclose($handle);
    }
    return $filter;
}

function apply_filter($data, $file = '/home/solvent/filter.lob') {
    $filters = init_filters($file);
    $plugin = $_GET['name'];
    
    $return = array();
    
    foreach ($filters[$plugin] as $exp) {
        switch ($exp['__match']) {
            case 'exact':
                $match = True;
                foreach (array_keys($exp) as $field) {
                    if ($field != '__match' && $field != '__type') {
                        if (strtolower($exp[$field]) == strtolower($data[$field])) {
                            //echo 'MATCH! ' . $exp[$field] . '==' . $data[$field];
                        } else {
                            $match = False;
                        }
                    }
                }
                if ($match) {
                    //echo $exp['__type'];
                    //return $exp['__type'];
                    $return[] = $exp['__type'];
                }
                break;
            case 'contains':
                $match = True;
                foreach (array_keys($exp) as $field) {
                    if ($field != '__match' && $field != '__type') {
                        if (intval(substr_count(strtolower($data[$field]), strtolower($exp[$field]))) > 0) {
                            //echo 'MATCH! ' . $data[$field] . '~=' . $exp[$field];
                        } else {
                            $match = False;
                        }
                    }
                }
                if ($match) {
                    //echo $exp['__type'];
                    //return $exp['__type'];
                    $return[] = $exp['__type'];
                }
                break;
            case 'notcontains':
                $match = True;
                foreach (array_keys($exp) as $field) {
                    if ($field != '__match' && $field != '__type') {
                        if (intval(substr_count(strtolower($data[$field]), strtolower($exp[$field]))) > 0) {
                            $match = False;
                        } else {
                            //echo 'MATCH! ' . $data[$field] . '!~' . $exp[$field];
                        }
                    }
                }
                if ($match) {
                    //echo $exp['__type'];
                    //return $exp['__type'];
                    $return[] = $exp['__type'];
                }
                break;
            case 'not':
                $match = False;
                foreach (array_keys($exp) as $field) {
                    if ($field != '__match' && $field != '__type') {
                        if (strtolower($exp[$field]) == strtolower($data[$field])) {
                            $match = True;
                        } else {
                            //echo 'MATCH! ' . $data[$field] . '!=' . $exp[$field];
                        }
                    }
                }
                if ($match) {
                    //echo $exp['__type'];
                    //return $exp['__type'];
                    $return[] = $exp['__type'];
                }
                break;
        }
    }
    return $return;
}

?>