# Image Cleaner

画像のクリーニング（色の簡素化）と背景透過処理を行う Python ツールです。

ロゴやイラストなどの画像を、指定した色のみに変換し、さらに背景を透過させることで、Web 向けに最適化されたクリーンな PNG 画像を生成します。

## 機能概要

### 1. 色の簡素化 (`image_cleaner.py`)

入力画像の各ピクセルを、指定したターゲット色の中から最も近い色に置き換えます。

- **複数色対応**: 3色以上のターゲット色を自由に指定可能
- **アンチエイリアス処理**: ガウシアンブラーと LANCZOS リサイズにより、色の境界のジャギー（ギザギザ）を抑制
- **軽量出力**: PNG の最適化オプションによりファイルサイズを軽減

### 2. 背景透過 (`bg_remover.py`)

色の簡素化後の画像から、背景色を透過させます。

- **Flood Fill 方式**: 画像の四隅（左上）からつながる背景色のみを透過
- **許容誤差（tolerance）対応**: JPEG ノイズなどによる微妙な色のばらつきにも対応
- **滑らかな切り抜き**: アルファチャンネルにガウシアンブラーを適用し、フチを自然に馴染ませる

## 処理フロー

```
target.png (入力画像)
    │
    ▼  image_cleaner.py (色の簡素化)
    │
cleaned_output_3colors.png (中間ファイル)
    │
    ▼  bg_remover.py (背景透過)
    │
final_transparent.png (最終出力)
```

## 動作環境

- Python 3.x
- Windows / macOS / Linux

## セットアップ

### 1. リポジトリのクローン

```bash
git clone <リポジトリURL>
cd image_cleaner
```

### 2. 仮想環境の作成と有効化

```bash
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS / Linux
```

### 3. 依存パッケージのインストール

```bash
uv pip install -r requirements.txt
```

## 使い方

### ステップ 1: 色の簡素化

`image_cleaner.py` の実行設定を編集し、入力ファイル名とターゲット色を指定します。

```python
# ターゲット色の指定 (RGB形式)
colors = [
    [0, 0, 0],       # 黒
    [255, 255, 255],  # 白
    [40, 120, 220],   # 青
    [50, 198, 129],   # 緑
    [100, 80, 180],   # 紫
    [136, 136, 136]   # グレー
]

binarize_to_specific_colors_web(
    'target.png',                  # 入力ファイル
    'cleaned_output_3colors.png',  # 出力ファイル
    colors
)
```

実行:

```bash
py image_cleaner.py
```

### ステップ 2: 背景透過

`bg_remover.py` を実行して背景を透過させます。

```python
remove_background_only(
    'cleaned_output_3colors.png',  # 入力ファイル (ステップ1の出力)
    'final_transparent.png',       # 出力ファイル
    tolerance=40  # 背景色の許容誤差 (0-255)
)
```

実行:

```bash
py bg_remover.py
```

### パラメータの調整

| パラメータ | ファイル | 説明 | 推奨値 |
|---|---|---|---|
| `target_colors` | `image_cleaner.py` | 画像に使用する色の一覧 (RGB) | 用途に応じて指定 |
| `tolerance` | `bg_remover.py` | 背景色の許容誤差 | 30〜60 (JPEG ノイズがある場合) |

## 依存パッケージ

| パッケージ | バージョン | 用途 |
|---|---|---|
| NumPy | 2.4.2 | ピクセルデータの高速な距離計算 |
| Pillow | 12.1.1 | 画像の読み込み、フィルタ処理、保存 |

