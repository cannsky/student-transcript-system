<?php

/*
Author: Can Gök
Description: PHP bot to get data from cirriculum and convert it to json file format
*/

function GetData(){
    $websiteUrl = "http://cse.eng.marmara.edu.tr/lisans-programi/bolum-mufredati";
    return file_get_contents($websiteUrl);
}

function ParseData($data){
    preg_match_all(
        '@<table class="fullTable" style="width:700px;" border="1">(.*?)</table>@si',
        $data,
        $outputData);
    return $outputData;
}

function ParseData2($data){
    preg_match_all(
        '@<table class="fullTable" style="width:700px;font-family:tahoma, arial, helvetica, sans-serif;font-size:small;" border="1">(.*?)</table>@si',
        $data,
        $outputData);
    return $outputData;
}

function ParseLectureDetails($data){
    $i = 0;
    foreach($data as &$datum){
        preg_match_all(
            '@<td(.*?)</td>@si',
            $datum,
            $outputData);
        $j = 0;
        foreach($outputData[0] as &$outputDatum){
            $outputData[0][$j++] = strip_tags($outputDatum);
        }
        $data[$i++] = $outputData[0];
    }
    return $data;
}

function UpdateSemesterIndex($data, $semesterIndex){
    $i = 0;
    foreach($data as &$array){
        $array[0] = $semesterIndex;
        $data[$i++] = $array;
    }
    unset($data[$i]);
    return $data;
}

function TranslateTurkishToEnglish($data){
    $i = 0;
    foreach($data as &$array){
        if(strcmp($array[3], "Zorunlu") == 0) $array[3] = "Mandatory";
        else if(strcmp($array[3], "Seçmeli") == 0) $array[3] = "Elective";
        $data[$i++] = $array;
    }
    return $data;
}

function ConvertData($data, $semesterIndex){
    $data = UpdateSemesterIndex($data, $semesterIndex);
    $data = TranslateTurkishToEnglish($data);
    return $data;
}

function CreateLectureArray($newData, $details){
    foreach($details as &$detail){
        if(strcmp($detail[1], "Toplam") == 0) continue;
        $newArray = array(
            "Semester" => $detail[0],
            "Lecture Code" => $detail[1],
            "Lecture Name" => $detail[2],
            "Lecture Type" => $detail[3],
            "Theoretical Lecture Hours" => $detail[4],
            "Practical-Lab Lecture Hours" => $detail[5],
            "Credit" => $detail[6],
            "European Credit Transfer System" => $detail[7]
        );
        array_push($newData, $newArray);
    }
    return $newData;
}

$newData = [];

function ParseLectureData($data, $newData){
    $semesterIndex = 0;
    foreach($data[0] as &$datum){
        $semesterIndex++;
        preg_match_all(
            '@<tbody>(.*?)</tbody>@si',
            $datum,
            $semester);
        preg_match_all(
            '@<tr>(.*?)</tr>@si',
            $semester[0][0],
            $lectures);
        $details = ParseLectureDetails($lectures[0]);
        $details = ConvertData($details, $semesterIndex);
        $newData = CreateLectureArray($newData, $details);
    }
    return $newData;
}

$rawData = GetData();
$parsedSemesterData = ParseData($rawData);
$parsedExtraData = ParseData2($rawData);
$newData = ParseLectureData($parsedSemesterData, $newData);
$newData = ParseLectureData($parsedExtraData, $newData);
file_put_contents("inputs.json", json_encode($newData, JSON_UNESCAPED_UNICODE));

?>