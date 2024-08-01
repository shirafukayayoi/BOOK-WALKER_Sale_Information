# BOOK-WALKER_Sale_Information

## 概要

BOOK☆WALKERのセール情報を取得するためのスクリプトです。  
Googleスプレットシートにセール情報を記録することができます。  
`GoogleSheetPush.py`を実行することで、セール情報を取得し、スプレットシートに記録します。

## 使い方

1. `main.py`の実行
1. セール情報のURLを入力(2ページ、3ページ、となるとき変わるのが&page=2、&page=3のURKです)  
    例: https://bookwalker.jp/category/2/?order=rank&detail=1&qpri=2&qspp=1&qcsb=1&np=1
1. csvファイルに出力したい場合は、これだけ終了です。

Googleスプレットシートに出力したい場合は、以下の手順を追加してください。

1. GoogleスプレットシートAPI、GoogleDriveAPIの取得、`credentials.json`のダウンロード
1. ダウンロードしたファイルを、`GoogleSheetPush.py`と同じディレクトリに配置
1. Googleスプレットシートのcredentials.jsonのファイル名を`sheet_credentials.json`に変更
1. Googleドライブのcredentials.jsonのファイル名を`drive_credentials.json`に変更
1. GoogleドライブのフォルダIDをMain関数の`folder_id`に設定
1. 実行。セール情報がスプレットシートに記録されます。
