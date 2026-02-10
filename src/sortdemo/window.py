"""
SortDemoのメインウィンドウモジュール。

アプリケーションのUI構築、ユーザ操作のハンドリング、
ソートアルゴリズムの実行制御を担当する。
ヘッダーバー（アルゴリズム選択・開始/停止ボタン）、
描画キャンバス、下部コントロール（速度・サイズスライダー）
で構成される。
"""

import gi
from gi.repository import Gtk, Adw, GLib
from .canvas import SortCanvas
from .algorithms import BubbleSort, InsertionSort, QuickSort, MergeSort


class SortDemoWindow(Adw.ApplicationWindow):
    """ソートアルゴリズム可視化のメインウィンドウ。

    UIレイアウトの構築、ソートの開始/一時停止/リセット制御、
    タイマーベースのアニメーション駆動を行う。

    ソートアルゴリズムは Python ジェネレータとして実装されており、
    GLib.timeout_add によるタイマーで1ステップずつ進行させることで
    リアルタイムの可視化を実現している。

    Attributes:
        algo_model (Gtk.StringList): ドロップダウン用のアルゴリズム名リスト
        algorithms (dict): アルゴリズム名からクラスへのマッピング
        algo_dropdown (Gtk.DropDown): アルゴリズム選択ドロップダウン
        canvas (SortCanvas): ソートデータの描画領域
        speed_scale (Gtk.Scale): アニメーション速度調整スライダー
        size_scale (Gtk.Scale): データサイズ変更スライダー
        status_label (Gtk.Label): ステップ数表示ラベル
        generator: 現在実行中のソートジェネレータ（未実行時は None）
        timeout_id: GLib タイマーの ID（未設定時は None）
        is_running (bool): ソートが実行中かどうかのフラグ
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Sort Demo")
        self.set_default_size(800, 600)

        # ── メインレイアウト ──
        # 縦方向の Box にヘッダーバー → キャンバス → コントロールを配置
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        # ── ヘッダーバー ──
        header_bar = Adw.HeaderBar()
        main_box.append(header_bar)

        # ── アルゴリズム選択ドロップダウン ──
        # StringList モデルにアルゴリズム名を登録し、DropDown のデータソースとする
        self.algo_model = Gtk.StringList()
        self.algorithms = {
            "Bubble Sort": BubbleSort,
            "Insertion Sort": InsertionSort,
            "Quick Sort": QuickSort,
            "Merge Sort": MergeSort,
        }
        for name in self.algorithms.keys():
            self.algo_model.append(name)

        self.algo_dropdown = Gtk.DropDown(model=self.algo_model)
        # アルゴリズム変更時にソートをリセットする
        self.algo_dropdown.connect("notify::selected", self.on_algo_changed)
        # ドロップダウンをヘッダーバーのタイトル位置に配置
        header_bar.set_title_widget(self.algo_dropdown)

        # ── 開始/一時停止ボタン ──
        self.start_btn = Gtk.Button(label="Start")
        self.start_btn.connect("clicked", self.on_start_clicked)
        header_bar.pack_start(self.start_btn)

        # ── リセットボタン ──
        reset_btn = Gtk.Button(label="Reset")
        reset_btn.connect("clicked", self.on_reset_clicked)
        header_bar.pack_end(reset_btn)

        # ── 描画キャンバス ──
        # vexpand/hexpand を True にして、利用可能な領域いっぱいに広げる
        self.canvas = SortCanvas()
        self.canvas.set_vexpand(True)
        self.canvas.set_hexpand(True)
        main_box.append(self.canvas)

        # ── 下部コントロールバー ──
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.set_margin_top(10)
        controls_box.set_margin_bottom(10)
        controls_box.set_margin_start(10)
        controls_box.set_margin_end(10)
        main_box.append(controls_box)

        # ── 速度スライダー ──
        # 値 1（遅い）〜 100（速い）。タイマー間隔に変換して使用する
        controls_box.append(Gtk.Label(label="Speed:"))
        self.speed_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 100, 1)
        self.speed_scale.set_value(50)
        self.speed_scale.set_hexpand(True)
        controls_box.append(self.speed_scale)

        # ── サイズスライダー ──
        # 要素数を 10〜1000 の範囲で 10 刻みで変更できる
        controls_box.append(Gtk.Label(label="Size:"))
        self.size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 1000, 10)
        self.size_scale.set_value(50)
        self.size_scale.set_hexpand(True)
        # サイズ変更時にデータを再生成する
        self.size_scale.connect("value-changed", self.on_size_changed)
        controls_box.append(self.size_scale)

        # ── ステップ数表示ラベル ──
        self.status_label = Gtk.Label(label="Steps: 0")
        controls_box.append(self.status_label)

        # ── ソート実行状態の管理変数 ──
        self.generator = None    # 現在のソートジェネレータ
        self.timeout_id = None   # GLib タイマー ID
        self.is_running = False  # 実行中フラグ

        # ウィンドウが画面に表示された（map された）タイミングで
        # 初回描画を確実に実行する
        self.connect("map", self.on_map)

        # 初期データの生成（サイズスライダーの現在値を使用）
        self.on_size_changed(self.size_scale)

    # ── シグナルハンドラ ──

    def on_map(self, widget):
        """ウィンドウが画面にマップされた際に呼ばれる。

        ウィジェットが実際に表示されるタイミングで再描画を要求し、
        初期状態を確実に画面に反映する。
        """
        self.canvas.queue_draw()

    def on_size_changed(self, scale):
        """サイズスライダーの値が変更された際に呼ばれる。

        新しいサイズでランダムデータを再生成し、
        実行中のソートを停止してステップ数をリセットする。

        Args:
            scale (Gtk.Scale): サイズスライダーウィジェット
        """
        size = int(scale.get_value())
        self.canvas.generate_data(size)
        self.stop_sorting()
        self.status_label.set_label("Steps: 0")

    def on_algo_changed(self, dropdown, _param):
        """アルゴリズム選択が変更された際に呼ばれる。

        実行中のソートを停止し、ステップ数とハイライトをリセットする。
        データは保持されるため、新しいアルゴリズムで同じデータを
        ソートし直すことができる。

        Args:
            dropdown (Gtk.DropDown): アルゴリズム選択ドロップダウン
            _param: プロパティ変更通知のパラメータ（未使用）
        """
        self.stop_sorting()
        self.status_label.set_label("Steps: 0")
        self.canvas.update_view([])

    def on_reset_clicked(self, btn):
        """リセットボタンがクリックされた際に呼ばれる。

        データを再生成し、ソートをリセットする。
        on_size_changed を再度呼ぶことで、現在のサイズ設定で
        新しいランダムデータを生成する。

        Args:
            btn (Gtk.Button): リセットボタンウィジェット
        """
        self.on_size_changed(self.size_scale)

    def on_start_clicked(self, btn):
        """開始/一時停止ボタンがクリックされた際に呼ばれる。

        ソートが実行中なら一時停止（タイマー解除）し、
        停止中なら開始または再開する。ボタンのラベルも切り替わる。

        Args:
            btn (Gtk.Button): 開始/一時停止ボタンウィジェット
        """
        if self.is_running:
            # 一時停止: タイマーを解除してソートを中断
            self.is_running = False
            if self.timeout_id:
                GLib.source_remove(self.timeout_id)
                self.timeout_id = None
            btn.set_label("Start")
        else:
            # 開始/再開: ソートを開始してボタンラベルを変更
            self.start_sorting()
            btn.set_label("Pause")

    # ── ソート制御メソッド ──

    def start_sorting(self):
        """ソートを開始または再開する。

        ジェネレータが未作成の場合は、選択中のアルゴリズムから
        新しいジェネレータを作成する。既にジェネレータがある場合は
        一時停止からの再開として扱う。
        """
        if not self.generator:
            # 選択中のアルゴリズム名を取得
            algo_name = self.algo_model.get_string(self.algo_dropdown.get_selected())
            # 対応するソートクラスをインスタンス化し、ジェネレータを取得
            algo_class = self.algorithms[algo_name]
            self.generator = algo_class(self.canvas.data).sort()

        self.is_running = True
        self.schedule_tick()

    def stop_sorting(self):
        """ソートを完全に停止し、状態をリセットする。

        タイマーを解除し、ジェネレータを破棄する。
        一時停止とは異なり、再開はできない。
        """
        self.is_running = False
        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
            self.timeout_id = None

        self.generator = None
        self.start_btn.set_label("Start")

    def schedule_tick(self):
        """次のソートステップを実行するタイマーを設定する。

        速度スライダーの値をタイマー間隔（ミリ秒）に変換する。
        スライダー値 1（遅い）→ 100ms 間隔、
        スライダー値 100（速い）→ 1ms 間隔。
        """
        if not self.is_running:
            return

        # スライダー値を反転させてタイマー間隔に変換
        # （値が大きい = 速い = 間隔が短い）
        interval = max(1, int(101 - self.speed_scale.get_value()))
        self.timeout_id = GLib.timeout_add(interval, self.on_tick)

    def on_tick(self):
        """タイマーコールバック。ソートを1ステップ進める。

        ジェネレータから次のステップを取得し、キャンバスを更新する。
        ソートが完了（StopIteration）した場合はソートを停止する。

        Returns:
            bool: False を返すことで GLib タイマーの自動繰り返しを無効化。
                  次のタイマーは schedule_tick() で明示的に設定する。
        """
        # ワンショットタイマーなので、呼ばれた時点で ID をクリア
        self.timeout_id = None

        if not self.is_running:
            return False

        try:
            # ジェネレータから (アクティブインデックス, ステップ数) を取得
            active_indices, steps = next(self.generator)
            self.canvas.update_view(active_indices)
            self.status_label.set_label(f"Steps: {steps}")

            # 次のステップのタイマーを設定
            self.schedule_tick()
            # False を返して GLib による自動繰り返しを抑止
            # （schedule_tick で明示的にタイマーを設定するため）
            return False

        except StopIteration:
            # ソート完了: ジェネレータが尽きた
            self.stop_sorting()
            self.canvas.update_view([])  # ハイライトをクリア
            return False
