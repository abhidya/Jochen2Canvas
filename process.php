<?php
header("Content-Type: text/plain");


$binStart = $_GET['binsStart'];
$numbins = count($binStart);


$args = "";

for($i = 0; $i < $numbins; $i++){
	$args .= $binStart[$i] . " ";
}


$handle = popen("/usr/bin/python3 hello.py 2>&1 '" .$args."'" , 'r');
$output = fread($handle, 1024);
var_dump($output);
pclose($handle);
echo($handle)


?>



