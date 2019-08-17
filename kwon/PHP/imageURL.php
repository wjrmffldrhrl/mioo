<?php
$my_img[]='http://modernsweet.co.kr/web/upload/NNEditor/20190715/%EC%9D%B4%EB%8F%99%ED%9C%98%20%EC%95%88%EA%B2%BD%20%ED%95%98%ED%94%84%20%EC%BB%AC%EB%9F%AC%20%EC%95%88%EA%B2%BD%20%2819%29_shop1_202439.jpg';

$my_img[]='http://modernsweet.co.kr/web/upload/NNEditor/20190715/%EC%9D%B4%EB%8F%99%ED%9C%98%20%EC%95%88%EA%B2%BD%20%ED%95%98%ED%94%84%20%EC%BB%AC%EB%9F%AC%20%EC%95%88%EA%B2%BD%20%2822%29_shop1_202440.jpg';

 $fullpath = "images_saved";

foreach($my_img as $i){
    image_save_from_url($i,$fullpath);

    if(getimagesize($fullpath."/".basename($i))){
        echo '<h3 style="color: green;">Image ' . basename($i) . ' Downloaded Successfully</h3>';
    }else{
        echo '<h3 style="color: red;">Image ' . basename($i) . ' Download Failed</h3>';
    }
}

function image_save_from_url($my_img,$fullpath){
    if($fullpath!="" && $fullpath){
        $fullpath = $fullpath."/".basename($my_img);
    }
    $ch = curl_init ($my_img);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER,1);
    curl_setopt ($ch, CURLOPT_FOLLOWLOCATION, 1);
    $rawdata=curl_exec($ch);
    curl_close ($ch);
    if(file_exists($fullpath)){
        unlink($fullpath);
    }
    $fp = fopen($fullpath,'x');
    fwrite($fp, $rawdata);
    fclose($fp);
}
?>
