from PIL import Image, ImageFilter
import numpy as np

def binarize_to_specific_colors_web(input_path, output_path, target_colors):
    """
    3色以上のターゲット色に対応し、Web向けにジャギーを抑えて出力する
    """
    # 1. 画像読み込み
    img = Image.open(input_path).convert("RGB")
    orig_size = img.size
    
    # 2. 作業用に4倍に拡大（アンチエイリアスの精度を上げるため）
    # 1920x1080の半分なら、内部的にかなり高解像度でエッジを計算します
    working_img = img.resize((orig_size[0] * 4, orig_size[1] * 4), Image.LANCZOS)
    data = np.array(img).astype(float)
    
    # 3. ターゲット色をNumPy配列に変換
    targets = np.array(target_colors).astype(float)
    
    # 4. 全ピクセルを (全ピクセル数, 3) に変形して距離計算
    pixels = data.reshape(-1, 3)
    # 各ピクセルと「すべてのターゲット色」との距離を計算
    dists = np.sum((pixels[:, np.newaxis, :] - targets[np.newaxis, :, :])**2, axis=2)
    
    # 最も近い色のインデックスを取得（ここで3色以上の振り分けが行われる）
    best_target_idx = np.argmin(dists, axis=1)
    
    # 5. 色の置き換えと復元
    new_pixels = targets[best_target_idx].astype(np.uint8)
    new_data = new_pixels.reshape(data.shape)
    result_img = Image.fromarray(new_data)
    
    # 6. 【重要】境界線を滑らかにする処理
    # 拡大した状態で少しだけぼかし、元のサイズに高品質リサイズ（LANCZOS）で戻す
    # これにより、色の境目に「中間色」がわずかに生成され、ギザギザが消えます
    result_img = result_img.filter(ImageFilter.GaussianBlur(radius=1.5))
    final_img = result_img.resize(orig_size, Image.LANCZOS)
    
    # 7. PNGとして保存（optimize=Trueでファイルサイズを軽量化）
    final_img.save(output_path, "PNG", optimize=True)

# --- 実行設定 ---
# 3色指定：[ロゴ色1, ロゴ色2, 背景色] など
colors = [
    [0, 0, 0], # 黒
    [255, 255, 255], # 白
    [40, 120, 220],
    [50, 198, 129],
    [100, 80, 180],
    [136, 136, 136]
]

binarize_to_specific_colors_web(
    'target.png', 
    'cleaned_output_3colors.png', 
    colors
)