**Windows Only!**  

性質上、設定によってはOSの破壊を招く恐れがあります。  
一応、**管理者権限での実行を不可**にして安全性を考慮していますが、このライブラリを使用して生じた損害に対して一切の責任を負いかねます。  

以上同意いただける方のみご利用ください。  


<div id="目次"></div>

- <a href="#概要">概要</a>
  - <a href="#インストール">インストール</a>
  - <a href="#使い方">使い方</a>


<h1 id="概要">概要</h1>  

<a href="#目次">目次に戻る</a>

- フォルダ内のパスの追加・削除・変更[^1]を監視する`monitoring`
- フォルダ内のパスを特定フォーマットに従い連番リネームする`serial_renamer`

以上２種類のライブラリが入ったライブラリです。  

[^1]: 以下、まとめて`変更`とします。


<h2 id="インストール">インストール</h2>

<a href="#目次">目次に戻る</a>

インストール  
`pip install git+https://github.com/Otsuhachi/OtsuFolderSerialRenamer.git#egg=otsufolserren`  

アップデート  
`pip install -U otsufolserren`

アンインストール  
`pip uninstall otsufolserren`  

<h2 id="使い方">使い方</h2>

<a href="#目次">目次に戻る</a>

1. <a href="#get_fm">get_fmを利用してTypeFMなインスタンスを生成する</a>
1. <a href="#fsr">FolderSerialRenamerインスタンスを生成する</a>
1. <a href="#fsr_func">メソッドとプロパティ</a>を参考に自由に利用する

<h3 id="get_fm">get_fmを利用してTypeFMなインスタンスを生成する</h3>

- <a href="#目次">目次に戻る</a>
- <a href="#使い方">使い方に戻る</a>

`serial_renamer`を利用するためには`TypeFM`という形式に対応しているクラスのインスタンスを生成する必要があります。  
`TypeFM`はフォルダ内のパスの`変更`を監視する3種類のクラスのいずれかです。  
`otsufolserren`の`get_fm`関数から生成する方法を推奨しています。  

`get_fm`は位置引数`path`と`mode`と、キーワード引数`cache_dir`を持ちます。  

引数|型|値
:--:|:--:|:--:
path|str, pathlib.Path|監視するフォルダのパス
mode|`MODE`|監視するパスの種類。すべて、フォルダのみ、ファイルのみの３種類
cache_dir|str, pathlib.Path|キャッシュファイルの生成先フォルダのパス。生成できれば存在しなくてもOK

`MODE`とは監視するパスの種類を指定するための特定の文字列です。  
大文字、小文字は等価として扱われます。  

MODE|監視するパスの種類
:--:|:--:
`'d'`|フォルダのみ
`'f'`|ファイルのみ
`'df'`, `'fd'`|すべて

<h4 id="typemf_func">TypeMFのメソッドとプロパティ</h4>

- <a href="#使い方">使い方に戻る</a>

メソッド|引数|戻り型|概要
:--:|:--:|:--:|:--:
check||bool|フォルダ内のパスの`変更`を確認し、その有無を返す<br>`__bool__`が呼び出される場面ではこのメソッドの結果を返す
get_difference||tuple[int, list[str]]|(変更件数, [変更内容1, ..., 変更内容n])
iterdir|Optional[PATH_FILTER]|Generator[pathlib.Path, None, None]|フォルダ内の条件に一致するパスを返す<br>条件は`pathlib.Path`を引数として受け、`bool`を返す関数[^2]
update|||`update_cache`と`update_cache_file`を呼び出す<br>コンテキストマネージャとして使用する際、最後に呼び出される
update_cache|||フォルダ内の監視するパス一覧を最新の状態に更新する
update_cache_file|||キャッシュファイルを**現在のキャッシュ**で更新する<br>更新の有無はキャッシュとキャッシュファイルの差分で検出される

プロパティ|型|概要
:--:|:--:|:--:
cache|dict[pathlib.Path, tuple[int, int]]|`{<パス>: (<更新日時>, <生成日時>), ...}`
cache_file|pathlib.Path|キャッシュファイルのパス
path|pathlib.Path|監視するフォルダのパス
paths|set[pathlib.Path]|監視しているパスの一覧

[^2]: `pathlib.Path.is_dir`など

<h3 id="fsr">FolderSerialRenamerインスタンスを生成する</h3>

- <a href="#目次">目次に戻る</a>
- <a href="#使い方">使い方に戻る</a>

フォルダの`変更`の監視に加え、連番リネームを行いたい場合、`FolderSerialRenamer`インスタンスを生成する必要があります。  
正式には`otsufolserren.serial_renamer.classes.FolderSerialRenamer`ですが、`otsufolserren`からインポートできます。  

`FolderSerialRenamer`を生成する際、位置引数`fm`, `name_template`, `order`を与えることができます。  

引数|型|値
:--:|:--:|:--:
fm|TypeFM|監視するフォルダのFolderMonitoringインスタンス
name_template|Optional[str]|連番リネームの際に使用する名前のテンプレート<br>`{i:03d}`など、整数`i`に対するフォーマットを含めることができる。[^3]<br>フォーマットを含まない場合はテンプレートの末尾に`{i:0<監視するパス数の桁数>d}`が追加される[^4]
order|Optional[PATH_ORDER]|並び順を決める関数。<br>`pathlib.Path`を引数として受け、比較メソッド`__lt__(self, __other)->bool`を持つオブジェクトを返す関数が使用可能。<br>指定しなければ`TypeFM.iterdir`と同様の並び順になる

[^3]: ただし、位置指定の文字は`=`のみ対応です。
[^4]: `None`の場合は空文字列として扱うので挿入されるフォーマット部分のみの名前となる。

引数`order`に使用できる関数については`otsufolserren.orders`内で４種類が定義されています。  
これらも`otsufolserren`からインポートできます。  

order用関数|並び
:--:|:--:
ORDER_ATIME|最終アクセス日時
ORDER_CTIME|作成日時
ORDER_MTIME|内容更新日時
ORDER_NAME|名前

<h4 id="fsr_func">FolderSerialRenamerのメソッドとプロパティ</h4>

- <a href="#使い方">使い方に戻る</a>

`TypeMF`の<a href="#typemf_func">メソッドとプロパティ</a>をそのまま使用することができます。  
また、以下の追加メソッドが存在しています。  

メソッド|引数|戻り型|概要
:--:|:--:|:--:|:--:
get_preview||RENAME_PREVIEW|リネームのプレビューを取得する
rename|only_when_change:bool, *, preview:Optional[RENAME_PREVIEW]||リネームを実行する。<br>`only_when_change`は`変更`が発見されている時のみ実行するかどうか。<br>`preview`は事前に`get_preview`している場合、その戻り値を渡す

`RENAME_PREVIEW`は`{<元のパス>: <リネーム後のパス>, ...}`形式の辞書を表します。  

`fm(TypeFM)`の`update`はコンテキストマネージャとして使用している際、最後に呼び出される他、`rename`終了時にも呼び出されます。  
