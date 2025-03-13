<!DOCTYPE html>
<html>
<head>
    <title>Remove Duplicates from Sorted List</title>
</head>
<body>
    <h2>Enter sorted list of numbers separated by space</h2>
    <form method="post">
        <input type="text" name="numbers" placeholder="Enter numbers">
        <input type="submit" name="submit" value="Remove Duplicates">
    </form>
    <?php
    function removeDuplicate($arr) {
        $n = count($arr);
        if ($n == 0 || $n == 1) {
            return $arr;
        }
        $unique = [];
        $unique[] = $arr[0];
        for ($i = 1; $i < $n; $i++) {
            if ($arr[$i] != $arr[$i - 1]) {
                $unique[] = $arr[$i];
            }
        }
        return $unique;
    }

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $input = $_POST["numbers"];
        $inputArray = explode(" ", $input);
        $sortedArray = array_map('intval', $inputArray);
        sort($sortedArray);
        echo "<h2>Entered List</h2>";
        echo "<pre>" . print_r($sortedArray, true) . "</pre>";
        $result = removeDuplicate($sortedArray);
        echo "<h2>List After Removing Duplicates</h2>";
        echo "<pre>" . print_r($result, true) . "</pre>";
    }
    ?>
</body>
</html>
