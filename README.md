# Visual Studio Code Mail

## 概要

VisualCodeCreateMail は、Visual Studio Code からテンプレートや設定ファイルを利用してメール下書きを作成および送信するためのツールです。Python を使用してメールテンプレートと設定を解析し、事前に入力されたメールをデフォルトのメールクライアントで開きます。

## 必要条件

- Python 3.x
- `PyYAML` ライブラリ (`pip install pyyaml`)

### 一部機能

- value_github_issue

  - `requests` ライブラリ (`pip install requests`)
  - `python-dotenv` ライブラリ (`pip install python-dotenv`)

## ファイル構成

```
project-root/
|-- scripts/
|   |-- create_mail.py  # メール作成のメインスクリプト
|   |-- custom_date.py  # 日付スクリプトの例
|-- config.yml          # プレースホルダー値の設定ファイル
|-- env.yml             # メールアドレスを記載した環境ファイル
```

### 設定ファイル

#### `config.yml`

このファイルでは、プレースホルダーのタグと、それに対応する置換値やスクリプト参照を定義します。
例:

```yaml
- TAG: "${NAME}"
  MSG: "John Doe"

- TAG: "${DATE}"
  MSG: "custom_date"
  OPT: "script"
  ARG:
    - "%Y/%m/%d"

- TAG: "${GITHUB_ISSUE}"
  OPT: "script"
  MSG: "value_github_issue"
  ARG:
    - "" # github token
    - "ShotaIuchi/VSCMail"
    - "#{{number}}: {{title}} ({{state}})"

- TAG: "${CUSTOM}"
  MSG: "custom_script"
  OPT: "script"
  ARG:
    - "arg1"
    - "arg2"
```

#### `env.yml`

このファイルでは、ファイルとメールの受信者を対応付けます。また、CC および BCC もオプションで記載できます。
例:

```yaml
- FILE: "email_template.txt"
  TO: "recipient@example.com"
  CC: "cc@example.com"
  BCC: "bcc@example.com"
```

### メールテンプレート

メールテンプレートは以下の構成で記述してください:

1. タイトルを 1 行目に記述。
2. 空行を 1 行挟む。
3. メール本文を記述。

例 (`email_template.txt`):

```
件名例

こちらがメール本文です。${NAME} や ${DATE} を必要に応じて置換してください。
```

1. Visual Studio Code でメールテンプレートファイル (`email_template.txt`) を開いた状態にする。
2. メニュー「ターミナル」から「タスクの実行」を選択。
3. `VSCMail` を選択してタスクを実行。
4. デフォルトのメールクライアントが開き、メールの下書きが入力済みの状態で表示されます。

## ライセンス

このツールは MIT ライセンスの下で配布されています。
