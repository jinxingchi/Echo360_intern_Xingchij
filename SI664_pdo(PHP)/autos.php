<?php

// Demand a GET parameter
if ( ! isset($_GET['who']) || strlen($_GET['who']) < 1  ) {
    die('Name parameter missing');
}

// If the user requested logout go back to index.php
if ( isset($_POST['logout']) ) {
    header('Location: index.php');
    exit();
}

$pdo = new PDO('mysql:host=localhost; port=8889;dbname=misc', 'xingchij', 'jinxingchi');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$make = '';
$year = '';
$mileage = '';
$warning = FALSE;

if ( isset($_POST['make']) && isset($_POST['year'])
     && isset($_POST['mileage'])) {
	if ( !is_numeric($_POST['year']) || !is_numeric($_POST['mileage'])) {
		$warning = "Mileage and year must be numeric";
	} else if ( strlen($_POST['make'])<1 ) {
			$warning = "Make is required";
		} else {
			$sql = "INSERT INTO autos (make, year, mileage)
             	  VALUES (:make, :year, :mil)";
        	$stmt = $pdo->prepare($sql);
    		$stmt->execute(array(
        		':make' => $_POST['make'],
        		':year' => $_POST['year'],
        		':mil' => $_POST['mileage']));
    		$warning = "added";
			}
}


?>
<!DOCTYPE html>
<html>
<head>
<title>Xingchi Jin's Autos Database</title>
<?php require_once "bootstrap.php"; ?>
</head>
<body>
<div class="container">

<?php
// Note triple not equals and think how badly double
// not equals would work here...
if ( $warning !== FALSE ) {
    // Look closely at the use of single and double quotes
    if ( $warning == "added") {
    	echo('<p style="color: green;">'."Record inserted"."</p>\n");
    	} else {
    		echo('<p style="color: red;">'.htmlentities($warning)."</p>\n");
    		}
}

echo "<h1>Tracking Autos for ".$_GET['who']. "</h1>";
?>

<form method="post">
<label for="make">Make:</label>
<input type="text" name="make" size="60" <?php echo 'value="'. htmlentities($make). '"'; ?> id="make"><br/>
<label for="year">Year:</label>
<input type="text" name="year" <?php echo 'value="'. htmlentities($year). '"'; ?> id="year"><br/>
<label for="mil">Mileage:</label>
<input type="text" name="mileage" <?php echo 'value="'. htmlentities($mileage). '"'; ?> id='mileage'><br/>
<input type="submit" name="Add" value="Add">
<input type="submit" name="logout" value="Logout">
</form>

<h2>Automobiles</h2>
<?php

$stmt = $pdo->query("SELECT make, year, mileage FROM autos");
echo ("<ul>");
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
	echo ("<li>");
	echo (htmlentities($row['year'])." ".htmlentities($row['make'])." / ".htmlentities($row['mileage']));
	echo ("</li>");
}
echo "</ul>";

?>
</div>
</body>
</html>