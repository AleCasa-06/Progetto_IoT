<?php
$conn = new mysqli("localhost", "root", "", "parcheggio"); 

// Mostra auto parcheggiate e elimina le uscite, max=100
$stmt = $conn->query("SELECT * FROM automobili WHERE Data_uscita IS NULL"); 
$st = $conn->query("SELECT * FROM automobili WHERE Data_uscita IS NOT NULL"); 

$uscite = $st->fetch_all(MYSQLI_ASSOC); // Prendi tutte le uscite

// Elimina auto uscite
if (!empty($uscite)) {
    foreach ($uscite as $uscita) {
        $targa = $uscita['targa']; 
        $conn->query("DELETE FROM automobili WHERE targa = '$targa'"); 
    }
}

// Salva auto parcheggiate
$auto_parcheggiate = [];
$postiOccupati = 0;

while ($auto = $stmt->fetch_assoc()) {
    if (!empty($auto['targa'])) {
        $postiOccupati++;
    }
    // Usa chiave composta se vuoi, o array semplice:
    $auto_parcheggiate[] = $auto;
}



foreach ($auto_parcheggiate as $auto) {
    echo "Targa: " . $auto['targa'] . "<br>"; 
    echo "Ingresso: " . $auto['Data_ingresso'] . "<br><br>"; 
}

echo "Posti liberi: " . (100 - $postiOccupati) . "<br>";
echo "Posti occupati: $postiOccupati";
?>
