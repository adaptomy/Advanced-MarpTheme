import sys
import os
import subprocess
import json
import platform
import shutil
from pathlib import Path
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

def check_node_npm():
    """Node.jsとnpmがインストールされているかチェック"""
    try:
        # Node.jsのチェック
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True, check=True)
        print(f"Node.js version: {node_result.stdout.strip()}")
        
        # npmのチェック
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True, check=True)
        print(f"npm version: {npm_result.stdout.strip()}")
        
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_marp_cli():
    """Marp CLIを自動インストール"""
    try:
        show_message("依存関係のインストール", "Marp CLIが見つかりません。\n自動インストールを開始します。\n\n少し時間がかかる場合があります...")
        
        # Marp CLIをグローバルインストール
        if platform.system() == "Windows":
            result = subprocess.run(["npm", "install", "-g", "@marp-team/marp-cli"], 
                                  capture_output=True, text=True, check=True, shell=True)
        else:
            result = subprocess.run(["npm", "install", "-g", "@marp-team/marp-cli"], 
                                  capture_output=True, text=True, check=True)
        
        print(f"npm install output: {result.stdout}")
        show_message("インストール完了", "Marp CLIのインストールが完了しました。")
        return True
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Marp CLIのインストールに失敗しました:\n\n{e.stderr}\n\n手動でインストールしてください:\nnpm install -g @marp-team/marp-cli"
        show_message("インストールエラー", error_msg)
        return False
    except Exception as e:
        show_message("エラー", f"予期しないエラーが発生しました:\n{str(e)}")
        return False

def find_marp_command():
    """Marpコマンドを検出する（Windows/Mac/Linux対応）"""
    possible_commands = ["marp", "marp.cmd", "marp.exe"]
    
    for cmd in possible_commands:
        if shutil.which(cmd):
            return cmd
    
    # グローバルインストールパスも確認
    if platform.system() == "Windows":
        npm_global_paths = [
            os.path.expanduser("~\\AppData\\Roaming\\npm\\marp.cmd"),
            os.path.expanduser("~\\AppData\\Roaming\\npm\\marp.exe"),
            "C:\\Program Files\\nodejs\\marp.cmd",
            "C:\\Program Files\\nodejs\\marp.exe"
        ]
        for path in npm_global_paths:
            if os.path.exists(path):
                return path
    
    return None

if __name__ == "__main__":
    print("Marp プレゼンテーション変換ツールを開始します...")
    
    # Node.js/npmの確認
    if not check_node_npm():
        show_message("必要な環境が見つかりません", 
                    "Node.jsとnpmがインストールされていません。\n\n以下をインストールしてから再実行してください:\n1. Node.js: https://nodejs.org/\n2. 再起動後、このツールを再実行してください")
        sys.exit(1)
    
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

    # Marpコマンドを自動検出
    marp_command = find_marp_command()
    if not marp_command:
        # Marp CLIの自動インストールを試行
        if ask_yes_no("Marp CLIが見つかりません", "Marp CLIが見つかりません。\n自動でインストールしますか？\n\n「はい」を選ぶと、npm install -g @marp-team/marp-cli を実行します。"):
            if install_marp_cli():
                # インストール後に再検出
                marp_command = find_marp_command()
                if not marp_command:
                    show_message("エラー", "インストールは完了しましたが、Marpコマンドが見つかりません。\nコマンドプロンプトを再起動してから再実行してください。")
                    sys.exit(1)
            else:
                sys.exit(1)
        else:
            show_message("エラー", "Marp CLIが必要です。\n\n手動でインストールしてください:\n1. コマンドプロンプトを開く\n2. npm install -g @marp-team/marp-cli を実行\n3. このツールを再実行")
            sys.exit(1)

    # ファイル名とパスの処理（日本語対応）
    markdown_path = Path(markdown_file_path)
    file_name = markdown_path.stem
    output_dir = Path("output")

    # 出力ディレクトリを作成
    output_dir.mkdir(exist_ok=True)

    # 出力ファイルパス
    output_file = output_dir / f"{file_name}.pptx"
    
    command = [
        marp_command,
        str(markdown_path),
        "--pptx",
        "--output",
        str(output_file),
        "--theme-set",
        theme_path,
        "--allow-local-files"
    ]

    print(f"Generating PPTX for: {markdown_file_path}")
    print(f"Using Marp command: {marp_command}")
    print(f"Executing command: {' '.join(command)}")

    try:
        # Windows環境での日本語文字化け対策
        if platform.system() == "Windows":
            result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
        else:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        print(f"Marp stdout: {result.stdout}")
        if result.stderr:
            print(f"Marp stderr: {result.stderr}")
        
        # 出力ファイルが実際に作成されたか確認
        if output_file.exists():
            show_message("変換完了", f"PPTXファイルが正常に生成されました:\n{output_file.absolute()}")
        else:
            show_message("警告", f"コマンドは成功しましたが、出力ファイルが見つかりません:\n{output_file.absolute()}")
    
    except FileNotFoundError:
        show_message("エラー", f"'{marp_command}' コマンドが実行できませんでした。\n\nMarp CLIが正しくインストールされていることを確認してください。\n1. Node.jsをインストール: https://nodejs.org/\n2. Marp CLIをグローバルにインストール: npm install -g @marp-team/marp-cli\n3. コマンドプロンプトを再起動")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        error_message = f"PPTX生成中にエラーが発生しました:\n\n"
        error_message += f"終了コード: {e.returncode}\n"
        if e.stdout:
            error_message += f"出力: {e.stdout}\n"
        if e.stderr:
            error_message += f"エラー: {e.stderr}\n"
        error_message += f"\n実行コマンド: {' '.join(command)}"
        show_message("エラー", error_message)
        sys.exit(1)
    except Exception as e:
        show_message("エラー", f"予期しないエラーが発生しました:\n{str(e)}")
        sys.exit(1)