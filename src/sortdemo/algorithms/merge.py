"""
マージソートアルゴリズムモジュール。

マージソートは分割統治法に基づく安定なソートアルゴリズム。
配列を再帰的に半分に分割し、各部分配列をソートした後、
2つの整列済み配列を統合（マージ）してソート結果を構築する。

計算量:
  - 最悪・平均・最良: O(n log n)
  - 空間: O(n)（マージ時の一時配列）
"""


class MergeSort:
    """マージソートの可視化用実装。

    ジェネレータベースで1ステップずつソートを進め、
    各ステップで操作中のインデックスとステップ数を返す。

    Attributes:
        data (list[int]): ソート対象のデータ配列（インプレースで変更される）
        steps (int): 累計ステップ数
    """

    def __init__(self, data):
        """マージソートインスタンスを初期化する。

        Args:
            data (list[int]): ソート対象のデータ配列
        """
        self.data = data
        self.steps = 0

    def sort(self):
        """マージソートのエントリポイント。

        配列全体を対象に再帰的な分割・統合を開始する。

        Yields:
            tuple[list[int], int]: (アクティブなインデックスのリスト, 累計ステップ数)
        """
        yield from self._merge_sort(0, len(self.data) - 1)

    def _merge_sort(self, l, r):
        """再帰的にマージソートを実行する。

        配列を中央で2つに分割し、それぞれを再帰的にソートした後、
        _merge で統合する。

        Args:
            l (int): ソート対象の左端インデックス
            r (int): ソート対象の右端インデックス
        """
        if l < r:
            # 中央のインデックスを計算（オーバーフロー防止の書き方）
            m = l + (r - l) // 2
            # 左半分を再帰的にソート
            yield from self._merge_sort(l, m)
            # 右半分を再帰的にソート
            yield from self._merge_sort(m + 1, r)
            # ソート済みの左右を統合
            yield from self._merge(l, m, r)

    def _merge(self, l, m, r):
        """2つの整列済み部分配列を統合する。

        data[l..m] と data[m+1..r] をそれぞれ一時配列にコピーし、
        小さい方から順に data[l..r] に書き戻す。

        Args:
            l (int): 左側部分配列の開始インデックス
            m (int): 左側部分配列の終了インデックス（分割点）
            r (int): 右側部分配列の終了インデックス

        Yields:
            tuple[list[int], int]: (アクティブなインデックスのリスト, 累計ステップ数)
                - 書き込み時: [書き込み先インデックス]
        """
        # 左右の部分配列のサイズ
        n1 = m - l + 1  # 左側の要素数
        n2 = r - m      # 右側の要素数

        # 一時配列にコピー（マージ中に元データが上書きされるため）
        L = self.data[l:m+1]      # 左側部分配列のコピー
        R = self.data[m+1:r+1]    # 右側部分配列のコピー

        i = 0  # 左側一時配列のインデックス
        j = 0  # 右側一時配列のインデックス
        k = l  # 書き込み先（元配列）のインデックス

        # 左右の一時配列から小さい方を選んで元配列に書き戻す
        while i < n1 and j < n2:
            self.steps += 1
            # 現在書き込み中の位置をハイライト
            yield [k], self.steps

            if L[i] <= R[j]:
                # 左側の要素が小さいか等しい場合、左側から取得（安定ソート）
                self.data[k] = L[i]
                i += 1
            else:
                # 右側の要素が小さい場合、右側から取得
                self.data[k] = R[j]
                j += 1
            k += 1

        # 左側一時配列の残りをすべて書き戻す
        while i < n1:
            self.steps += 1
            yield [k], self.steps
            self.data[k] = L[i]
            i += 1
            k += 1

        # 右側一時配列の残りをすべて書き戻す
        while j < n2:
            self.steps += 1
            yield [k], self.steps
            self.data[k] = R[j]
            j += 1
            k += 1
