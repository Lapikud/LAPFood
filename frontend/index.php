<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="main.css">
        <script src="scripts/script_v1.js" ></script>
        <title>LAPFood</title>
    </head>
    <body onload="populate()" onclick="morningMenu()">
        <header>
            <div id='header'>Time goes here</div>        
        </header>
        <!--<section id="main"></section> -->

        <?php
        //$response = http_get("https://food.lapikud.ee/bitstop", array("timeout"=>1), $info);
        //print_r($info);
        //echo $info;
        //echo http_get ( "https://food.lapikud.ee/bitstop", array("timeout"=>1),$info );

        //teha XOR?
        $response = file_get_contents('https://food.lapikud.ee/bitstop');
        $response = json_decode($response);

        foreach($response->bitstop as $menuItem)
        {
            echo $menuItem . "<br />";
        }
        ?>


    </body>
</html> 