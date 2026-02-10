"""
ソートの可視化を行う描画キャンバスモジュール。

データ配列を棒グラフとして描画し、ソート中にアクティブな要素を
赤色でハイライト表示する。Gtk.DrawingArea を継承して
Cairo による自前の描画処理を実装している。
"""

import logging
import random
from gi.repository import Gtk


class SortCanvas(Gtk.DrawingArea):
    """ソートデータを棒グラフとして描画するカスタムウィジェット。

    各データ要素を縦棒で表し、値が大きいほど棒が高くなる。
    ソートアルゴリズムの進行中は、現在比較・交換中の要素を
    赤色でハイライトして視覚的にフィードバックする。

    Attributes:
        data (list[int]): ソート対象のデータ配列
        active_indices (list[int]): 現在ハイライト中のインデックスリスト
    """

    def __init__(self):
        super().__init__()
        # 描画関数を登録（GTK が再描画時にこの関数を呼び出す）
        # 第2引数の None は user_data（追加データ不要のため None）
        self.set_draw_func(self.draw_func, None)

        # ウィジェットの最小サイズを設定
        self.set_content_width(600)
        self.set_content_height(400)

        self.data = []               # ソート対象のデータ配列
        self.active_indices = []     # ハイライト対象のインデックス
        self._logger = logging.getLogger(__name__)

    def generate_data(self, size):
        """指定サイズのランダムデータを生成する。

        1〜size の連番を作成してシャッフルすることで、
        重複のないランダムな整数列を生成する。

        Args:
            size (int): データの要素数
        """
        self._logger.debug("Generating data with size: %d", size)
        self.data = list(range(1, size + 1))
        random.shuffle(self.data)
        self.active_indices = []
        self.queue_draw()  # データ変更後に再描画を要求

    def update_view(self, active_indices):
        """ハイライト対象のインデックスを更新し、再描画を要求する。

        ソートアルゴリズムが1ステップ進むたびに呼ばれ、
        現在操作中の要素を画面上でハイライトする。

        Args:
            active_indices (list[int]): ハイライトするインデックスのリスト
        """
        self.active_indices = active_indices
        self.queue_draw()

    def draw_func(self, area, cr, width, height, user_data):
        """GTK の描画コールバック。Cairo コンテキストを使って棒グラフを描画する。

        queue_draw() が呼ばれるたびに GTK がこの関数を呼び出す。
        各データ要素を幅が均等な縦棒として描画し、
        active_indices に含まれるインデックスの棒を赤色で表示する。

        Args:
            area (Gtk.DrawingArea): 描画領域ウィジェット（自身）
            cr (cairo.Context): Cairo 描画コンテキスト
            width (int): 描画領域の幅（ピクセル）
            height (int): 描画領域の高さ（ピクセル）
            user_data: ユーザデータ（未使用、None）
        """
        # 背景を白で塗りつぶす
        cr.set_source_rgb(1, 1, 1)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        if not self.data:
            return

        n = len(self.data)
        if n == 0:
            return

        # 各棒の幅を描画領域幅から均等に算出
        bar_width = width / n
        # 最大値に対する比率で棒の高さを決定
        max_val = max(self.data) if self.data else 1

        # 棒が細すぎる場合（3px以下）は枠線を描画しない
        # （パフォーマンスと視認性のため）
        draw_border = bar_width > 3

        for i, value in enumerate(self.data):
            # 値を最大値で正規化して棒の高さを計算
            bar_height = (value / max_val) * height

            # デフォルト色: 青（通常の要素）
            r, g, b = 0.2, 0.4, 0.8

            # アクティブな要素は赤色でハイライト（比較・交換中）
            if i in self.active_indices:
                r, g, b = 0.9, 0.2, 0.2

            # 棒を塗りつぶして描画（下端揃えのため y 座標を調整）
            cr.set_source_rgb(r, g, b)
            cr.rectangle(i * bar_width, height - bar_height, bar_width, bar_height)
            cr.fill()

            if draw_border:
                # 棒の境界線を黒で描画（要素の区切りを明確にする）
                cr.set_source_rgb(0, 0, 0)
                cr.set_line_width(1)
                cr.rectangle(i * bar_width, height - bar_height, bar_width, bar_height)
                cr.stroke()
