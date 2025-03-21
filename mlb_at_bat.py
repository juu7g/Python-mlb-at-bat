"""
MLB Gameday scraping
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webdriver as rweb
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import TimeoutException
import tkinter as tk
from tkinter import messagebox
import sys, os, locale
import i18n
sys.path.append(os.path.dirname(sys.executable))    # pyinstallerで設定ファイルを参照のため
try:
    import settings_mlb as settings     # 設定ファイルをインポート
    import settings_css as css_sel      # 設定ファイルをインポート
except ModuleNotFoundError as e:
    print(f"Error: {e}")
    input("Press any key to exit.")
    sys.exit()

is_firefox = settings.is_firefox    # 使用ドライバー
# Seleniumのインポート。対象ブラウザ用のモジュールをインポート
if is_firefox:
    from selenium.webdriver.firefox.options import Options
else:
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

def get_meipass() -> str:
    """
    実行時のカレントフォルダ
    pyinstallerで作成したexeを実行した場合とそうでない場合に異なるため

    Return:
        str:    実行時のカレントフォルダ
    """
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS   # 実行ファイルで起動した場合
    else:
        return "."         # pythonコマンドで起動した場合

def init():
    """
    初期設定(多言語対応、開始メッセージ)
    """
    # 多言語対応
    loc = settings.locale       # 設定ファイルの値を取得
    if not loc:                 # 設定ファイルが未設定ならデフォルトロケールから抽出
        loc = locale.getdefaultlocale()[0][:2]  # ('ja_JP', 'cp932')からjaを抽出
    i18n.load_path.append(f"{get_meipass()}\i18n")  # 多言語対応のメッセージ取得先
    i18n.set('locale', loc)                         # 言語を指定
    i18n.set('fallback', 'en')  # 定義されていない言語が指定された時に適用するロケール

    # スクリプト開始情報出力
    print("\nStart Script")
    print(f'  URL:   {settings.team_url}')
    print(f'  Player:{settings.player}')
    print(f"\n{i18n.t('msg.cancel')}\n")

    # トップページを出さないでダイアログだけ出るようにする
    root = tk.Tk()
    root.withdraw()     # トップページを隠す
    # スクリプト開始をダイアログ表示。3秒で自動的に閉じる
    root.after(3000, root.destroy)
    messagebox.showinfo("MLB at Bat", message=f"{i18n.t('msg.startup')}")

    # トップページを出さないでダイアログだけ出るようにする
    root = tk.Tk()
    root.attributes('-topmost', True)   # 最前面に出す
    root.withdraw()     # トップページを隠す

def wait_on_deck_or_due_up() -> bool:
    """
    on_deck か due_up に対象選手名が出るのを待つ
    名前が出たらダイアログで知らせる
    あわせて次の打席を待つか問い合わせる

    Return:
        bool:   True:次の打席を待つ、False:終了する
    """
    # CSSセレクタ
    css_sel_on_deck = css_sel.on_deck
    css_sel_due_up  = css_sel.due_up

    result = False
    wait = WebDriverWait(driver, 60*60)  # Timeout 60分（最大待ち時間）

    # on_deckかdue_upに対象選手名が出るのを待つ
    wait.until(
		Ec.any_of(
            Ec.text_to_be_present_in_element(
                (By.CSS_SELECTOR, css_sel_on_deck), f"On deck: {settings.player}"),
            Ec.text_to_be_present_in_element(
                (By.CSS_SELECTOR, css_sel_due_up), settings.player)
        ), i18n.t("msg.over60"))    # タイムアウト例外へのメッセージ

    # どちらの条件が成立したか分からないので両方のテキストを取得する
    next_player = ""
    # due upのテキスト取得
    try:    # 検索結果が見つからない場合、例外が出る
        next_player = driver.find_element(By.CSS_SELECTOR, css_sel_due_up).text.replace("\n", "")
    except (NoSuchElementException, InvalidSelectorException):
        pass
    else:   # due_upが見つかった場合、先頭ならメッセージを出す。それ以外ならon_deckを待つ
        if not next_player.startswith(settings.player):
            wait.until(Ec.text_to_be_present_in_element(
                (By.CSS_SELECTOR, css_sel_on_deck), f"On deck: {settings.player}")
                )

    # on_deckのテキスト取得
    try:    # 検索結果が見つからない場合、例外が出る
        next_player = driver.find_element(By.CSS_SELECTOR, css_sel_on_deck).text.replace("\n", "")
    except (NoSuchElementException, InvalidSelectorException):
        pass

    # 現在どの回の攻撃なのかテキスト取得
    css_kai = ".TeamSummaryMatchupstyle__GameStateWrapper-sc-1twp77n-4" # CSSセレクタ
    kai = driver.find_element(By.CSS_SELECTOR, css_kai).text

    # ダイアログ表示
    if not next_player.startswith("On deck"):
        next_player = "Due up : " + next_player
    print(f"{i18n.t('msg.title')} {kai} {next_player}")
    result = messagebox.askyesno(f"{i18n.t('msg.title')}", f"{kai}\n{next_player}\n{i18n.t('msg.ask')}")

    return result

def start_browser() -> rweb.WebDriver:
    """
    指定されたブラウザ用のドライバインスタンスの作成
    webdriver_managerで最新ドライバを自動取得

    Return:
        WebDriver:  ドライバーインスタンス
    """
    # ブラウザーを起動
    options = Options()             # オプションインスタンス作成
    if not settings.display_on:
        headless = ("--headless", "-headless")      # (Chrome, Firefox) でのオプション
        options.add_argument(headless[is_firefox])  # ヘッドレスモード(ブラウザを見せない)
    # Webドライバーに依り対象ブラウザを変える。ドライバー更新付
    if is_firefox:
        driver = webdriver.Firefox(options=options)  # ブラウザインスタンス作成
    else:   # Chrome
        # DevToolsエラー等のログを出さない
        service = Service()
        service.creation_flags = 0x08000000 # ヘッドレスモードで DevTools listening on ws:~~ を表示させない
        driver = webdriver.Chrome(service=service, options=options)  # ブラウザインスタンス作成
    return driver

def start_gameday():
    """
    スクレイピングを開始
    球団のURLにアクセス⇒クッキーを許可⇒Gamedayへ移動
    """
    # 待機時間設定
    wait = WebDriverWait(driver, 60)  # Timeout 60秒（最大待ち時間）

    # 球団URLにアクセス
    print("Start browsing")
    driver.get(settings.team_url)    # 指定したURLを表示

    # クッキー画面に応答
    cookie_id = "onetrust-accept-btn-handler"
    element = wait.until(Ec.element_to_be_clickable((By.ID, cookie_id)))
    # element = driver.find_element(By.ID, cookie_id)   # untilの戻り値と同じなので省略
    element.click()
    print("Clicked to accept cookies")

    # メイン画面が表示されるまで待機
    wait.until(Ec.title_contains("Official"))
    print("Start looking for Gameday link")

    # Gameday アイコンが出るまで待ち、出たらアイコン(ボタン)をクリック
    wait.until(Ec.element_to_be_clickable((By.CLASS_NAME, "trk-gameday")), i18n.t("msg.gameday"))
    element = driver.find_element(By.CSS_SELECTOR, ".trk-gameday button")
    element.click()
    print("goto Gameday")

    # Gamedayメイン画面が表示されるまで待機
    wait.until(Ec.title_contains("Gameday"))
    print(f"start waiting for {settings.player}")

# ここからメイン処理
init()

try:
    # ブラウザーを起動
    driver = start_browser()

    # Gamedayにアクセス
    start_gameday()

    # プレイヤーの打席を待つ
    while wait_on_deck_or_due_up(): pass

except TimeoutException as e:
    print(f"{i18n.t('msg.timeout')}：{e.msg}")
    messagebox.showinfo(title=f"{i18n.t('msg.timeout')}", message=f"{e.msg}")
except KeyboardInterrupt:
    print(f"{i18n.t('msg.ctrl-c')}")    # 中断メッセージ
except Exception as identifier:
    print(f"{i18n.t('msg.exception')}", identifier)
finally:
    # ブラウザーを終了
    try:
        driver.quit()
    except (NameError, AttributeError):
        pass

print("Finished")
