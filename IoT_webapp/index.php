<html>
    <head>
        <title>Parcheggio Casarotto-Venzo</title>
        <link rel="stylesheet" href="style/style.css">
    </head>
        <body>
            
        </body>
</html>

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
        $dataIngresso = new DateTime($uscita['Data_ingresso']); 
        $dataUscita = new DateTime($uscita['Data_uscita']); 

        $intervallo = $dataIngresso->diff($dataUscita);
        // Ottieni la durata totale in ore decimali
        $ore = $intervallo->h + ($intervallo->i / 60) + ($intervallo->s / 3600);
        $giorniExtra = $intervallo->days - ($intervallo->h || $intervallo->i || $intervallo->s ? 0 : 1); // gestisce giorni interi
        $ore += $giorniExtra * 24;

        $costo = $ore * 1.5; 
 
    }
}

$out = $conn->query("SELECT * FROM auto_uscite"); 
$auto_uscite = []; 
while ($res = $out->fetch_assoc()) {
    $auto_uscite[] = $res; 
}

// Auto uscite
echo "<div class='auto-section'><h2>Auto Uscite</h2>"; 
foreach($auto_uscite as $car) {
    echo "<div class='auto-box uscita'>";
    echo "<p><strong>Targa:</strong> " . $car['targa'] . "</p>"; 
    echo "<p><strong>Ingresso:</strong> " . $car['Data_ingresso'] . "</p>"; 
    echo "<p><strong>Uscita:</strong> " . $car['Data_uscita'] . "</p>"; 
    echo "<p><strong>Costo:</strong> €" . $car['Costo'] . "</p>";
    echo "</div>";
}
echo "</div>"; // Fine sezione Auto Uscite

// Salva auto parcheggiate
$auto_parcheggiate = [];
$postiOccupati = 0;

while ($auto = $stmt->fetch_assoc()) {
    if (!empty($auto['targa'])) {
        $postiOccupati++;
    }
    $auto_parcheggiate[] = $auto;
}

echo "<div class='auto-section'><h2>Auto Parcheggiate</h2>";
foreach ($auto_parcheggiate as $auto) {
    echo "<div class='auto-box parcheggiata'>";
    echo "<p><strong>Targa:</strong> " . $auto['targa'] . "</p>"; 
    echo "<p><strong>Ingresso:</strong> " . $auto['Data_ingresso'] . "</p>"; 
    echo "</div>";
}

echo "</div>"; // Fine sezione Auto Parcheggiate

// Posti
echo "<div class='posti-section'>";
echo "<p><strong><id='lib'>Posti liberi:</strong> " . (100 - $postiOccupati) . "</p>";
echo "<p><strong><id='occ'>Posti occupati:</strong> $postiOccupati</p>";
echo "</div>";
?>
