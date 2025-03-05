import nbformat
import glob
from black import format_str, FileMode

def format_notebook(notebook_path):
    print(f"Formatting {notebook_path}...")
    
    # ノートブックを読み込む
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # 各セルのコードをフォーマット
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            try:
                # Blackを使用してコードをフォーマット
                cell.source = format_str(cell.source, mode=FileMode())
            except Exception as e:
                print(f"Warning: Could not format cell in {notebook_path}: {e}")
    
    # フォーマット済みのノートブックを保存
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)

def main():
    # 全てのノートブックファイルを取得
    notebooks = glob.glob('*.ipynb')
    
    for notebook_path in notebooks:
        format_notebook(notebook_path)
        print(f"✓ Formatted {notebook_path}")

if __name__ == '__main__':
    main() 