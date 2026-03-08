from PIL import Image, ImageFilter, ImageDraw

def remove_background_only(input_path, output_path, tolerance=50):
    """
    画像を読み込み、四隅からつながる背景色のみを透過させる関数
    :param tolerance: 色の許容誤差 (0-255)。JPEGノイズがある場合は30-60推奨。
    """
    # 1. 画像を読み込み、アルファチャンネル付き(RGBA)に変換
    img = Image.open(input_path).convert("RGBA")
    
    # 2. 作業用のコピーを作成（ここで塗りつぶし判定を行う）
    # 元の画像データは色を保持したいので、コピーに対して操作します
    work_img = img.copy()
    
    # 3. 背景の抽出 (Flood Fill)
    # 画像の(0,0)の色を基準に、つながっている似た色を「完全透明(0,0,0,0)」に塗りつぶす
    # thresh=tolerance で、微妙に色が違う白（JPEGノイズなど）もまとめて透過扱いにします
    ImageDraw.floodfill(work_img, (0, 0), (0, 0, 0, 0), thresh=tolerance)
    
    # 4. マスクの作成と平滑化（ジャギー対策）
    # 塗りつぶした結果から「アルファチャンネル（透明度情報）」だけを取り出す
    mask = work_img.getchannel('A')
    
    # 境界線を滑らかにするために、アルファチャンネルをわずかにぼかす
    # これにより、パキッとした切り抜きではなく、フチが少し馴染むようになります
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1))
    
    # 5. 元の画像に、滑らかにしたアルファチャンネルを適用
    img.putalpha(mask)
    
    # 6. 保存
    img.save(output_path, "PNG")
    print(f"保存しました: {output_path}")

# --- 実行 ---
remove_background_only(
    'cleaned_output_3colors.png', 
    'final_transparent.png',
    tolerance=40  # 白背景が少し汚れている場合はこの数値を上げてください(最大255)
)