import os
import time
import cv2
import numpy as np
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from skimage.metrics import structural_similarity as ssim

# --- 設定項目 ---

# 1. 動画のURL
VIDEO_URL = "https://www.google.com" # ここに対象の動画URLを貼り付け

# 2. スクリーンショットの保存先フォルダ
OUTPUT_DIR = "slides_output"

# 3. 類似度のしきい値 (0.0 ~ 1.0)
#    1.0に近いほど「ほぼ同じ画像」と判断される。
#    この値を下げると、わずかな変化でも別スライドと判定されやすくなる。
#    書き込みがある場合は低めに設定 (推奨値 0.75-0.85)
SIMILARITY_THRESHOLD = 0.80

# 4. チェック間隔（秒）
#    この秒数ごとに画面をチェックする。短すぎるとPCに負荷がかかる。
CHECK_INTERVAL_SECONDS = 1.0

# 5. 比較範囲の指定（クロッピング）
#    動画の再生バーや広告などを除外したい場合に設定する (左, 上, 右, 下)
#    設定しない場合は None にする
#    例 CROP_BOX = (0, 0, 1920, 900) # 上部900ピクセルのみを比較対象にする
CROP_BOX = None

# 6. 履歴保持の設定
#    スライド変化を検出した時に、何秒前の画面を保存するか
HISTORY_SECONDS = 1.5  # 1.5秒前の画面を保存
#    履歴を保持する最大フレーム数（メモリ使用量を制限）
MAX_HISTORY_FRAMES = 10

# 7. 変化検出の安定性設定
#    連続して何回類似度が下がったら新しいスライドと判定するか
CHANGE_CONFIRMATION_COUNT = 2  # 2回連続で変化を検出したら確定

# --- 設定項目はここまで ---


def compare_images(img1, img2):
    """2つの画像を比較し、類似度を返す"""
    # グレースケールに変換して比較する
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 比較のためにリサイズ（処理を高速化し、微細なノイズの影響を減らす）
    resized1 = cv2.resize(gray1, (320, 180))
    resized2 = cv2.resize(gray2, (320, 180))

    # 構造的類似度 (SSIM) を計算
    score, _ = ssim(resized1, resized2, full=True)
    return score

def main():
    # 実行時のタイムスタンプでフォルダ名を作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_output_dir = os.path.join(OUTPUT_DIR, f"session_{timestamp}")
    
    # 出力フォルダを作成
    os.makedirs(session_output_dir, exist_ok=True)
    print(f"画像保存先: {session_output_dir}")

    # Selenium WebDriverのセットアップ
    # まず、ローカルのchromedriverを試す
    try:
        # 同じフォルダにchromedriverがある場合
        service = ChromeService(executable_path='./chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        print("ローカルのchromedriverを使用します。")
    except Exception as e:
        print("ローカルのchromedriverが見つかりません。webdriver-managerを使用します。")
        try:
            # webdriver-managerを使うと、自動で適切なChromeDriverをダウンロード・設定してくれる
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
            print("webdriver-managerでchromedriverをダウンロード・設定しました。")
        except Exception as e2:
            print("--- WebDriverの起動に失敗しました ---")
            print("エラー:", e2)
            print("手動でダウンロードしたchromedriverをスクリプトと同じフォルダに置いて再試行してください。")
            return
        
    driver.maximize_window()
    driver.get(VIDEO_URL)

    # ユーザーが動画を再生し、フルスクリーンにするのを待つ
    input("\nブラウザで動画を再生し、フルスクリーンなど最適な表示状態にしてください。\n準備ができたら、このコンソールでEnterキーを押してください...")

    print("\nスライドの監視を開始します。(終了するには Ctrl+C を押してください)")

    previous_image = None
    slide_counter = 0
    change_count = 0  # 連続変化カウンター
    
    # 履歴保持用のリスト（タイムスタンプ付きで画像を保存）
    image_history = []  # [(timestamp, full_image, target_image), ...]

    try:
        while True:
            current_time = time.time()
            
            # スクリーンショットを撮ってOpenCVで扱える形式に変換
            png_data = driver.get_screenshot_as_png()
            nparr = np.frombuffer(png_data, np.uint8)
            current_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 指定されていれば画像をクロップ
            if CROP_BOX:
                x1, y1, x2, y2 = CROP_BOX
                # スライスは [y1:y2, x1:x2] の順なので注意
                target_image = current_image[y1:y2, x1:x2]
            else:
                target_image = current_image

            # 履歴に現在の画像を追加
            image_history.append((current_time, current_image.copy(), target_image.copy()))
            
            # 古い履歴を削除（メモリ使用量を制限）
            if len(image_history) > MAX_HISTORY_FRAMES:
                image_history.pop(0)

            if previous_image is None:
                # 最初のスライドを保存
                slide_counter += 1
                filename = os.path.join(session_output_dir, f"slide_{slide_counter:03d}.png")
                cv2.imwrite(filename, current_image)
                print(f"最初のスライドを保存しました: {filename}")
                previous_image = target_image
            else:
                # 前の画像と比較
                similarity = compare_images(previous_image, target_image)
                print(f"現在の類似度: {similarity:.4f} (変化回数: {change_count})", end="\r")

                if similarity < SIMILARITY_THRESHOLD:
                    change_count += 1
                    if change_count >= CHANGE_CONFIRMATION_COUNT:
                        # 連続して変化が検出されたら、新しいスライドと判断
                        slide_counter += 1
                        
                        # 履歴から指定秒数前の画像を探す
                        target_time = current_time - HISTORY_SECONDS
                        best_image = current_image  # デフォルトは現在の画像
                        
                        for hist_time, hist_full_image, hist_target_image in reversed(image_history):
                            if hist_time <= target_time:
                                best_image = hist_full_image
                                break
                        
                        filename = os.path.join(session_output_dir, f"slide_{slide_counter:03d}.png")
                        cv2.imwrite(filename, best_image)
                        print(f"\n新しいスライドを検出！ {HISTORY_SECONDS}秒前の画像を保存しました: {filename}")
                        
                        previous_image = target_image
                        change_count = 0  # カウンターをリセット
                        # 新しいスライドを保存した直後は少し待つ（アニメーションなどをスキップするため）
                        time.sleep(1.5)
                else:
                    # 類似度が高い場合はカウンターをリセット
                    change_count = 0

            # 指定した間隔で待機
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n\n監視を終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        # ブラウザを閉じる
        driver.quit()
        print(f"合計 {slide_counter} 枚のスライドを {session_output_dir} に保存しました。")


if __name__ == "__main__":
    main()