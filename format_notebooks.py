import glob
import nbformat

from black import format_str, FileMode
from isort import code, Config


def format_notebook(notebook_path: str) -> None:
    """指定されたノートブックファイルの各コードセルのインポート文やコードを整形する。"""
    print(f"Formatting {notebook_path}...")
    
    # ノートブックを読み込む
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # isortの設定
    isort_config = Config(
        profile="black",
        multi_line_output=3,
        include_trailing_comma=True,
        force_grid_wrap=0,
        use_parentheses=True,
        ensure_newline_before_comments=True,
        line_length=88,
        order_by_type=False,  # タイプによる順序付けを無効化
        case_sensitive=True,  # 大文字小文字を区別
        force_sort_within_sections=True,  # セクション内で強制的にソート
        lexicographical=True,  # 完全な辞書順でソート
        sections=["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"],
        default_section="THIRDPARTY"
    )
    
    # 各コードセルのコードをフォーマット
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            try:
                # isortを使ってインポート文を整理
                cell.source = code(cell.source, config=isort_config)
                # Blackを使ってコード全体をフォーマット
                cell.source = format_str(cell.source, mode=FileMode())
            except Exception as e:
                print(f"Warning: Could not format a cell in {notebook_path}: {e}")
    
    # フォーマット済みのノートブックを保存する
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)


def main() -> None:
    """カレントディレクトリ内の全ての.ipynbファイルを整形する。"""
    notebooks = glob.glob('*.ipynb')
    
    for notebook_path in notebooks:
        format_notebook(notebook_path)
        print(f"✓ Formatted {notebook_path}")


if __name__ == '__main__':
    main()
