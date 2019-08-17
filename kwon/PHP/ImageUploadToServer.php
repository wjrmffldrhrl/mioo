<?

$con = mysqli_connect("localhost", "kyu9341", "asas120700", "kyu9341");

header("Content-Type:text/html;charset=utf-8");

$data = $_POST["data1"];


$file_path = $data."/";



echo $file_path;
  if(is_dir($data)){
    echo "폴더 존재 o";
  }else{
    echo "폴더 존재 x";
    @mkdir($data, 0777);
    @chmod($data, 0777);
  }

  $file_path = $file_path . basename($_FILES['uploaded_file']['name']);

  if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], $file_path)){
    echo "file upload success";
  }else{
    echo "file upload fail";
  }

?>
