<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport">
  <title>Scontrino Parcheggio</title>
  <link rel="stylesheet" href="style/style.css">
</head>
    <body>
        <div class="parking-ticket">
            <h1>Parcheggio Casarotto-Venzo</h1>
            
            
        </div>
    </body>
</html>


<?php
$conn = new mysqli("localhost", "root", "", "parcheggio"); 

//mostra auto parcheggiate e elimina le uscite, max=100
$stmt = $conn->query("SELECT * FROM auto WHERE Data_uscita = NULL "); 
$st = $conn->query("SELECT * FROM auto WHERE NOT Data_uscita = NULL"); 

$uscite = $st->fetch_all(MYSQL_ASSOC); 

for($i = 0; $i < count($uscite) ; $i++ ){
    $targa = $uscite['targa']; 
    $sl = $conn->query("DELETE FROM auto WHERE targa = '$targa'"); 
}



$auto_parcheggiate = $stmt->fetch_all(MYSQL_ASSOC); 


$postiOccupati = count($auto_parcheggiate); 

for($i = 0; $i < $postiOccupati ; $i++ ){
    echo "Targa: " . $auto_parcheggiate['targa']; 
    echo "Ingresso: " . $auto_parcheggiate['Data_ingresso']; 
    
    echo "Posti liberi: " . (100 - $postiOccupati); 
}







?>