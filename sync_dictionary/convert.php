<?php
// convert.phpとか適当に名前つけて保存してくだしあ


// ファイル名を引数から読込んで定義
$option = getopt('i:o:');
$filename_in  = empty( $option['i'] ) ? "./名称未設定.txt" : $option['i'] ;
$filename_out = empty( $option['o'] ) ? "./IME辞書01.plist" : $option['o'] ;

// 存在確認して入力ファイルを開く
if( !file_exists($filename_in) ){
    echo("WARN - 指定された入力ファイルは存在しません。 file=$filename_in");
  exit();
} else {
    $fp_in = fopen( $filename_in, "r" );
}

// 存在確認して出力ファイルを作成・開く
if( file_exists($filename_out) ){
    echo("WARN - 既に出力先ファイルが存在しています。 file=$filename_out");
    exit();
} else {
    touch( $filename_out );
    $fp_out = fopen( $filename_out, "w" );
}

//出力ファイルにヘッダ行を投入
fwrite($fp_out,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
fwrite($fp_out,"<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n");
fwrite($fp_out,"<plist version=\"1.0\">\n");
fwrite($fp_out,"<array>\n");


//一行読み込み、以下の処理を繰り返す
while (($data = fgets($fp_in)) !== FALSE)
{
  // HTでバラして配列に変換
  $data_array = explode("\t", $data);

  // 使うのは0個目と1個目だけなので、ここが空だったらスルーする
  if( $data_array[0]!=="" && $data_array[1]!=="" )
  {
    //HTMLエスケープしないとimportした時落ちる(白目)
    $shortcut = htmlspecialchars($data_array[0]);
    $phrase   = htmlspecialchars($data_array[1]);

    // 出力
    fwrite($fp_out,"    <dict>\n");
    fwrite($fp_out,"        <key>phrase</key>\n");
    fwrite($fp_out,"        <string>$phrase</string>\n");
    fwrite($fp_out,"        <key>shortcut</key>\n");
    fwrite($fp_out,"        <string>$shortcut</string>\n");
    fwrite($fp_out,"    </dict>\n");
  }
}

//出力ファイルにフッタ行を投入
fwrite($fp_out,"</array>\n");
fwrite($fp_out,"</plist>\n");

//ファイルを閉じる
fclose($fp_in);
fclose($fp_out);
