import os
import time
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from skimage.metrics import structural_similarity as ssim

# --- 設定項目 ---

# 1. 動画のURL
VIDEO_URL = "chrome.com" # ここに対象の動画URLを貼り付け

# 2. スクリーンショットの保存先フォルダ
OUTPUT_DIR = "slides_output"

# 3. 類似度のしきい値 (0.0 ~ 1.0)
#    1.0に近いほど「ほぼ同じ画像」と判断される。
#    この値を下げると、わずかな変化でも別スライドと判定されやすくなる。
#    推奨値 0.90 (90%の類似度)
SIMILARITY_THRESHOLD = 0.90

# 4. チェック間隔（秒）
#    この秒数ごとに画面をチェックする。短すぎるとPCに負荷がかかる。
CHECK_INTERVAL_SECONDS = 1.0

# 5. 比較範囲の指定（クロッピング）
#    動画の再生バーや広告などを除外したい場合に設定する (左, 上, 右, 下)
#    設定しない場合は None にする
#    例 CROP_BOX = (0, 0, 1920, 900) # 上部900ピクセルのみを比較対象にする
CROP_BOX = None

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
    # 出力フォルダを作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Selenium WebDriverのセットアップ
    # webdriver-managerを使うと、自動で適切なChromeDriverをダウンロード・設定してくれる
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    except Exception as e:
        print("--- WebDriverの起動に失敗しました ---")
        print("エラー:", e)
        print("手動でダウンロードしたchromedriverをスクリプトと同じフォルダに置いて再試行してください。")
        # 同じフォルダにchromedriverがある場合
        service = ChromeService(executable_path='./chromedriver')
        driver = webdriver.Chrome(service=service)
        
    driver.maximize_window()
    driver.get(VIDEO_URL)

    # ユーザーが動画を再生し、フルスクリーンにするのを待つ
    input("\nブラウザで動画を再生し、フルスクリーンなど最適な表示状態にしてください。\n準備ができたら、このコンソールでEnterキーを押してください...")

    print("\nスライドの監視を開始します。(終了するには Ctrl+C を押してください)")

    previous_image = None
    slide_counter = 0

    try:
        while True:
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

            if previous_image is None:
                # 最初のスライドを保存
                slide_counter += 1
                filename = os.path.join(OUTPUT_DIR, f"slide_{slide_counter:03d}.png")
                cv2.imwrite(filename, current_image)
                print(f"最初のスライドを保存しました: {filename}")
                previous_image = target_image
            else:
                # 前の画像と比較
                similarity = compare_images(previous_image, target_image)
                print(f"現在の類似度: {similarity:.4f}", end="\r")

                if similarity < SIMILARITY_THRESHOLD:
                    # 類似度がしきい値を下回ったら、新しいスライドと判断
                    slide_counter += 1
                    filename = os.path.join(OUTPUT_DIR, f"slide_{slide_counter:03d}.png")
                    cv2.imwrite(filename, current_image)
                    print(f"\n新しいスライドを検出！ 保存しました: {filename}")
                    
                    previous_image = target_image
                    # 新しいスライドを保存した直後は少し待つ（アニメーションなどをスキップするため）
                    time.sleep(1.5)

            # 指定した間隔で待機
            time.sleep(CHECK_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n\n監視を終了します。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        # ブラウザを閉じる
        driver.quit()
        print(f"合計 {slide_counter} 枚のスライドを {OUTPUT_DIR} に保存しました。")


if __name__ == "__main__":
    main()