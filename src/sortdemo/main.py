"""
SortDemoアプリケーションのエントリポイント。

GTK 4 と Libadwaita を使用したソートアルゴリズム可視化ツールの
メインアプリケーションクラスと起動処理を定義する。
"""

import sys
import gi

# GTK 4 と Adwaita 1 のバージョンを明示的に指定
# （他のバージョンが読み込まれるのを防止する）
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw
from .window import SortDemoWindow


class SortDemoApp(Adw.Application):
    """SortDemoのメインアプリケーションクラス。

    Adw.Application を継承し、アプリケーションのライフサイクル
    （起動・アクティブ化・終了）を管理する。
    application_id により、システム上で一意に識別される。
    """

    def __init__(self, **kwargs):
        super().__init__(application_id='com.example.SortDemo',
                         flags=0,
                         **kwargs)

    def do_activate(self):
        """アプリケーションがアクティブ化された際に呼ばれるコールバック。

        既存のウィンドウがあればそれを表示し、なければ新規に
        SortDemoWindow を作成して表示する。
        """
        win = self.props.active_window
        if not win:
            win = SortDemoWindow(application=self)
        win.present()


def main():
    """アプリケーションを生成して実行する。

    Returns:
        int: アプリケーションの終了コード
    """
    app = SortDemoApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
