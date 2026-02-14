# Repository Structure

SortDemo - GTK 4 (Libadwaita) を使用したソートアルゴリズム可視化アプリケーション

## Directory Tree

```
sortdemo/
├── src/
│   ├── sortdemo/
│   │   ├── __init__.py
│   │   ├── main.py              # アプリケーションエントリーポイント
│   │   ├── window.py            # メインウィンドウ（UI実装）
│   │   ├── canvas.py            # 描画キャンバス（可視化）
│   │   └── algorithms/          # ソートアルゴリズム実装
│   │       ├── __init__.py
│   │       ├── bubble.py        # バブルソート
│   │       ├── insertion.py     # 挿入ソート
│   │       ├── quick.py         # クイックソート
│   │       └── merge.py         # マージソート
│   ├── sortdemo.egg-info/       # パッケージ情報
│   └── __init__.py
├── tests/
│   └── test_bubble.py           # バブルソートのテスト
├── .venv/                       # Python仮想環境
├── .idea/                       # IDE設定
├── AGENTS.md                    # 開発指示書
├── README.md                    # プロジェクト説明
├── pyproject.toml               # プロジェクト設定
├── uv.lock                      # UVパッケージマネージャ用ロックファイル
├── .gitignore                   # Git除外設定
└── .python-version              # Pythonバージョン指定
```

## Key Files

| File | Purpose |
|------|---------|
| `src/sortdemo/main.py` | アプリケーション起動とセットアップ |
| `src/sortdemo/window.py` | メインウィンドウUI、ヘッダーバー、コントロールパネル |
| `src/sortdemo/canvas.py` | 配列要素を棒グラフで描画、色分け表示 |
| `src/sortdemo/algorithms/*.py` | 各ソートアルゴリズムのジェネレータ実装 |
| `pyproject.toml` | 依存関係、エントリーポイント、プロジェクトメタデータ |

## Dependencies

- Python 3.13+
- GTK 4
- Libadwaita (PyGObject)

## Entry Point

```
sortdemo = "sortdemo.main:main"
```
