"""
クイックソートアルゴリズムモジュール。

クイックソートは分割統治法に基づく高効率なソートアルゴリズム。
配列からピボット（基準値）を選び、ピボットより小さい要素を左側、
大きい要素を右側に振り分ける「パーティション」操作を再帰的に
繰り返すことでソートを行う。

計算量:
  - 最悪: O(n²)（ピボットが常に最小/最大値の場合）
  - 平均: O(n log n)
  - 空間: O(log n)（再帰スタック）
"""


class QuickSort:
    """クイックソートの可視化用実装。

    ジェネレータベースで1ステップずつソートを進め、
    各ステップで操作中のインデックスとステップ数を返す。
    ピボットには配列の末尾要素を使用する（Lomuto パーティション方式）。

    Attributes:
        data (list[int]): ソート対象のデータ配列（インプレースで変更される）
        steps (int): 累計ステップ数
    """

    def __init__(self, data):
        """クイックソートインスタンスを初期化する。

        Args:
            data (list[int]): ソート対象のデータ配列
        """
        self.data = data
        self.steps = 0

    def sort(self):
        """クイックソートのエントリポイント。

        配列全体を対象に再帰的な分割ソートを開始する。

        Yields:
            tuple[list[int], int]: (アクティブなインデックスのリスト, 累計ステップ数)
        """
        yield from self._quick_sort(0, len(self.data) - 1)

    def _quick_sort(self, low, high):
        """再帰的にクイックソートを実行する。

        パーティション操作でピボットの正しい位置を確定し、
        ピボットの左右の部分配列に対して再帰的にソートを行う。

        Args:
            low (int): ソート対象の開始インデックス
            high (int): ソート対象の終了インデックス
        """
        if low < high:
            # パーティション操作を実行し、ピボットの確定位置を取得
            # _partition はジェネレータなので yield from で委譲し、
            # return 値（ピボットの位置）を pi で受け取る
            pi_gen = self._partition(low, high)
            pi = yield from pi_gen

            # ピボットの左側を再帰ソート
            yield from self._quick_sort(low, pi - 1)
            # ピボットの右側を再帰ソート
            yield from self._quick_sort(pi + 1, high)

    def _partition(self, low, high):
        """Lomuto パーティション方式で配列を分割する。

        末尾要素をピボットとして選択し、ピボット以下の要素を
        左側に、ピボットより大きい要素を右側に振り分ける。

        Args:
            low (int): パーティション対象の開始インデックス
            high (int): パーティション対象の終了インデックス（ピボット位置）

        Returns:
            int: ピボットが配置された最終的なインデックス

        Yields:
            tuple[list[int], int]: (アクティブなインデックスのリスト, 累計ステップ数)
                - 比較時: [現在の要素, ピボット]
                - 交換時: [交換先, 交換元]
                - 最終配置時: [ピボットの確定位置, 元のピボット位置]
        """
        # ピボットとして末尾要素を選択
        pivot = self.data[high]
        # i はピボット以下の要素を配置する位置を追跡するポインタ
        i = low - 1

        for j in range(low, high):
            self.steps += 1
            # 現在の要素 j とピボット high をハイライト
            yield [j, high], self.steps

            if self.data[j] <= pivot:
                # ピボット以下の要素を左側に寄せる
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                # 交換後の状態をハイライト
                yield [i, j], self.steps

        # ピボットを正しい位置（i+1）に配置
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        yield [i + 1, high], self.steps
        # ピボットの確定位置を返す（yield from で呼び出し元が受け取る）
        return i + 1
