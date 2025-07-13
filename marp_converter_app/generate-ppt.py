import sys
import os
import subprocess
import json
from tkinter import Tk, filedialog, messagebox

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def select_file(title, filetypes):
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    root.destroy()
    return file_path

def show_message(title, message):
    root = Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(title, message)
    root.destroy()

def ask_yes_no(title, message):
    root = Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askyesno(title, message)
    root.destroy()
    return response

if __name__ == "__main__":
    config = load_config()
    theme_path = config.get("theme_path")

    # Initial theme selection or re-selection
    if not theme_path or not os.path.exists(theme_path):
        show_message("テーマファイル選択", "初回起動です。使用するテーマCSSファイルを選択してください。")
        theme_path = select_file("テーマCSSファイルを選択してください", [("CSS files", "*.css")])
        if not theme_path:
            show_message("エラー", "テーマファイルが選択されませんでした。終了します。")
            sys.exit(1)
        config["theme_path"] = theme_path
        save_config(config)
        show_message("テーマ設定完了", f"テーマファイルが設定されました:\n{theme_path}")
    else:
        # Ask if user wants to change theme
        if ask_yes_no("テーマの変更", f"現在のテーマファイル:\n{theme_path}\n\n別のテーマファイルに切り替えますか？"):
            theme_path = select_file("新しいテーマCSSファイルを選択してください", [("CSS files", "*.css")])
            if not theme_path:
                show_message("テーマ変更キャンセル", "テーマファイルの変更をキャンセルしました。現在のテーマを使用します。")
                theme_path = config.get("theme_path") # Revert to old theme if cancelled
            else:
                config["theme_path"] = theme_path
                save_config(config)
                show_message("テーマ変更完了", f"新しいテーマファイルが設定されました:\n{theme_path}")

    show_message("Markdownファイル選択", "変換したいMarkdownファイルを選択してください。")
    markdown_file_path = select_file("変換したいMarkdownファイルを選択してください", [("Markdown files", "*.md")])

    if not markdown_file_path:
        show_message("エラー", "Markdownファイルが選択されませんでした。終了します。")
        sys.exit(1)

    # Use 'marp' command directly, assuming it's in the system's PATH
    marp_command = "marp"

    file_name = os.path.basename(markdown_file_path).replace(".md", "")
    output_dir = "output"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    command = [
        marp_command,
        markdown_file_path,
        "--pptx",
        "--output",
        os.path.join(output_dir, f"{file_name}.pptx"),
        "--theme-set",
        theme_path,
        "--allow-local-files"
    ]

    print(f"Generating PPTX for: {markdown_file_path}")
    print(f"Executing command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Marp stdout: {result.stdout}")
        show_message("変換完了", f"PPTXファイルが正常に生成されました:\n{os.path.join(output_dir, f'{file_name}.pptx')}")
    except FileNotFoundError:
        show_message("エラー", "'marp' コマンドが見つかりません。\n\nMarp CLIがグローバルにインストールされていることを確認してください。\n1. Node.jsをインストール: https://nodejs.org/\n2. Marp CLIをグローバルにインストール: npm install -g @marp-team/marp-cli")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        show_message("エラー", f"PPTX生成中にエラーが発生しました:\n{e.stderr}")
        sys.exit(1)