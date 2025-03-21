# Python-mlb-at-bat
[In English](#in-english)

## 概要
次の打席お知らせアプリ

MLB の選手の打席が近づくと知らせます

## 特徴

- MLB の指定した選手が次打者か次の回の先頭打者になるとダイアログで知らせます  
- 日本語表示、英語表示に対応  
- ブラウザとして Chrome か Firefox がインストールされていると動作します  

### 制限事項

- １回表の第１打席は知らせません  
- 次の打席まで 60分以上かかるとタイムアウトとなりアプリは終了します  
	継続したい場合はアプリを再起動してください  
- お知らせする選手は選手名だけで判断しています  
	相手のチームに同じ名前の選手がいるとその選手の打席も知らせます  
- 本アプリは www.mlb.com にアクセスします  
	その際にクッキーの使用を許可するように応答しています  
	*クッキーの使用を許可したくない場合、本アプリを使用しないでください。*  

## 依存関係（実行時）

- Windows 64ビット OS

## 依存関係（開発時）

- Python 3.12.8
- selenium 4.27.1
- i18nice 0.15.5

## 使い方
### 起動
`mlb-at-bat.exe` を起動します。

コマンド画面を開き動作状況を表示します。

※PC 起動直後は実行開始までに 10秒以上かかります。ご了承ください。  

### 操作方法

- 次の打席を待つかどうかを指示  
	ダイアログボックスで、「はい」または「いいえ」ボタンを押して、次の打席まで待つかどうかを選択します  
	「はい」を押す場合、お知らせした打席が終わってから押してください  
	「いいえ」を押すとアプリを終了します
- 途中でやめたい時  
	コマンド画面で `Ctrl + C` を押します  
	※試合終了や選手交代で次の打席が来ない場合、60分以上経てばタイムアウトとなりアプリは終了します

### 設定

- MLB設定ファイル：settings_mlb.py
	- 変数名　　：項目　　　　：説明　　　　　　：初期値
	- team_url　：チームURL　：チームのURLを指定："https://www.mlb.com/dodgers"
	- player　　：選手名　　　：選手名を指定　　："Ohtani"
	- locate　　：言語　　　　：言語を指定　　　："" (自動で判断)
	- is_firefox：ブラウザ　　：ブラウザを指定　：False(Chrome)、True(Firefox)
	- display_on：ブラウザ表示：ブラウザ操作を見せる：False
- CSS設定ファイル：settings_css.py：編集しないこと
	- 変数名　　：内容
	- on_deck：on_dech を見つけるCSSセレクタ
	- due_up ：due_up を見つけるCSSセレクタ

## プログラムの説明サイト Program description site

- 使い方：[大谷選手の打席を見逃さない！打席お知らせアプリ【フリー】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/scraping/mlb-at-bat-exe)  
- *準備中*作り方：[MLB Gamedayのスクレイピング【Python】 - プログラムでおかえしできるかな](https://juu7g.hatenablog.com/entry/Python/scraping/mlb-at-bat)

## 作者
juu7g

## ライセンス
このソフトウェアは、MITライセンスのもとで公開されています。LICENSEファイルを確認してください。  

## In English

## Description
Next at bat notification app

Notify when MLB players are at bat

## Features

- A dialog will inform you when a designated MLB player will be the next batter or leadoff hitter in the next inning.
- Supports Japanese and English display
- It works if you have Chrome or Firefox installed as your browser.

### Limitations

- The first at bat in the top of the first inning will not be announced.
- If it takes more than 60 minutes for your next turn to bat, the app will time out and close.  
	If you want to continue, please restart the app.
- The players to be announced will be determined by name alone.
	If there is a player with the same name on the opposing team, it will also notify you when that player will be at bat.
- This app accesses www.mlb.com at that time  
	It responds by allowing the use of cookies.  
	If you do not want to allow the use of cookies, please do not use this app.

## Requirement(Runtime)

- Windows 64bit OS

## Requirement(Development)

- Python 3.12.8
- selenium 4.25.0
- i18nice 0.15.5
## Usage
### Starting
Launch `mlb-at-bat.exe`

A command window will open and display the operation status.

* Please note that it may take more than 10 seconds to start execution immediately after starting the PC.  

### How to use

- Choose whether to wait for next at bat
	In the dialogue box, press the "Yes" or "No" button to choose whether to wait until next at bat.
	If you press "Yes", please do so after the notified at-bat is over.  
	Clicking "No" will close the app
- When you want to quit midway  
	Press `Ctrl + C` in the command window  
	* If the game ends or a player is substituted and there is no next at bat, the app will time out and close after 60 minutes.

### Settings

- MLB configuration file : settings_mlb.py
	- Variable Name : Item        : Explanation             : Initial Value
	- team_url      : Team URL    : Specify the team URL    : "https://www.mlb.com/dodgers"
	- player        : Player Name : Specify the player name : "Ohtani"
	- locate        : Language    : Specify language        : "" (Automatic decision)
	- is_firefox    : Browser     : Specify the browser     : False(Chrome)、True(Firefox)
	- display_on    : Browser display : Show browser operation : False
- CSS configuration file : settings_css.py : Do not edit
	- Variable Name : Contents
	- on_deck : CSS selector to find on_dech
	- due_up  : CSS selector to find due_up

## Authors
juu7g

## License
This software is released under the MIT License, see LICENSE file.

