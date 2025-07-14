import sys
import os
import subprocess
import json
import platform
import shutil
import re
from pathlib import Path
from tkinter import Tk, filedialog, messagebox, Toplevel, Label, Button, Text, Scrollbar, Frame
from tkinter import ttk

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

def select_directory(title, initial_dir=None):
    """ディレクトリ選択ダイアログ"""
    root = Tk()
    root.withdraw()  # Hide the main window
    if initial_dir and os.path.exists(initial_dir):
        dir_path = filedialog.askdirectory(title=title, initialdir=initial_dir)
    else:
        dir_path = filedialog.askdirectory(title=title)
    root.destroy()
    return dir_path

def extract_theme_name(css_file_path):
    """CSSファイルから@theme名を抽出する"""
    try:
        with open(css_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # /* @theme theme-name */ パターンを検索
        pattern = r'/\*\s*@theme\s+([^\s*]+)\s*\*/'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            theme_name = match.group(1)
            print(f"CSSファイルからテーマ名を取得: {theme_name}")
            return theme_name
        else:
            print("CSSファイルに@theme定義が見つかりませんでした")
            return None
            
    except Exception as e:
        print(f"CSSファイルの読み込みエラー: {e}")
        return None

def show_message(title, message):
    """スクロール可能なメッセージダイアログを表示"""
    try:
        # メッセージが短い場合は通常のメッセージボックスを使用
        if len(message) < 300 and message.count('\n') < 10:
            root = Tk()
            root.withdraw()
            messagebox.showinfo(title, message)
            root.destroy()
            return
        
        # 長いメッセージの場合はカスタムダイアログを使用
        root = Tk()
        root.withdraw()
        
        dialog = Toplevel(root)
        dialog.title(title)
        dialog.geometry("600x400")
        dialog.resizable(True, True)
        
        # メインフレーム
        main_frame = Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # テキストエリアとスクロールバー
        text_frame = Frame(main_frame)
        text_frame.pack(fill="both", expand=True)
        
        text_widget = Text(text_frame, wrap="word", font=("", 10))
        scrollbar = Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # メッセージを挿入
        text_widget.insert("1.0", message)
        text_widget.configure(state="disabled")  # 読み取り専用
        
        # OKボタン
        button_frame = Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ok_button = Button(button_frame, text="OK", command=dialog.destroy, font=("", 10))
        ok_button.pack()
        
        # ダイアログを中央に配置
        dialog.transient(root)
        dialog.grab_set()
        
        # 画面中央に配置
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # ダイアログが閉じるまで待機
        dialog.wait_window()
        root.destroy()
        
    except Exception as e:
        # カスタムダイアログでエラーが発生した場合は標準のメッセージボックスにフォールバック
        print(f"カスタムダイアログエラー: {e}")
        try:
            root = Tk()
            root.withdraw()
            # 長いメッセージは切り詰める
            if len(message) > 1000:
                truncated_message = message[:1000] + "\n\n...(メッセージが長すぎるため切り詰められました)"
                messagebox.showinfo(title, truncated_message)
            else:
                messagebox.showinfo(title, message)
            root.destroy()
        except Exception as fallback_error:
            # 最後の手段：コンソールに出力
            print(f"メッセージボックス表示エラー: {fallback_error}")
            print(f"タイトル: {title}")
            print(f"メッセージ: {message}")
            print("上記メッセージを確認してください。")

def ask_yes_no(title, message):
    root = Tk()
    root.withdraw()  # Hide the main window
    response = messagebox.askyesno(title, message)
    root.destroy()
    return response

def check_node_npm():
    """Node.jsとnpmがインストールされているかチェック"""
    try:
        # Windows環境でのコマンド拡張子対応
        if platform.system() == "Windows":
            node_cmd = "node.exe"
            npm_cmd = "npm.cmd"
        else:
            node_cmd = "node"
            npm_cmd = "npm"
        
        # Node.jsのチェック
        print("Node.jsの確認中...")
        node_result = subprocess.run([node_cmd, "--version"], capture_output=True, text=True, check=False)
        if node_result.returncode != 0:
            print(f"Node.js check failed: {node_result.stderr}")
            return False
        print(f"✓ Node.js version: {node_result.stdout.strip()}")
        
        # npmのチェック
        print("npmの確認中...")
        npm_result = subprocess.run([npm_cmd, "--version"], capture_output=True, text=True, check=False)
        if npm_result.returncode != 0:
            print(f"npm check failed: {npm_result.stderr}")
            return False
        print(f"✓ npm version: {npm_result.stdout.strip()}")
        
        return True
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in check_node_npm: {e}")
        return False

def install_marp_cli():
    """Marp CLIを自動インストール"""
    try:
        show_message("依存関係のインストール", "Marp CLIが見つかりません。\n自動インストールを開始します。\n\n少し時間がかかる場合があります...")
        
        # Marp CLIをグローバルインストール
        if platform.system() == "Windows":
            result = subprocess.run(["npm.cmd", "install", "-g", "@marp-team/marp-cli"], 
                                  capture_output=True, text=True, check=True, shell=True)
        else:
            result = subprocess.run(["npm", "install", "-g", "@marp-team/marp-cli"], 
                                  capture_output=True, text=True, check=True)
        
        print(f"npm install output: {result.stdout}")
        show_message("インストール完了", "Marp CLIのインストールが完了しました。")
        return True
        
    except subprocess.CalledProcessError as e:
        if platform.system() == "Windows":
            error_msg = f"Marp CLIのインストールに失敗しました:\n\n{e.stderr}\n\n手動でインストールしてください:\n1. コマンドプロンプトを管理者権限で開く\n2. npm.cmd install -g @marp-team/marp-cli を実行"
        else:
            error_msg = f"Marp CLIのインストールに失敗しました:\n\n{e.stderr}\n\n手動でインストールしてください:\nnpm install -g @marp-team/marp-cli"
        show_message("インストールエラー", error_msg)
        return False
    except Exception as e:
        show_message("エラー", f"予期しないエラーが発生しました:\n{str(e)}")
        return False

def find_marp_command():
    """Marpコマンドを検出する（Windows/Mac/Linux対応）"""
    print("Marpコマンドを検索中...")
    print(f"現在のPATH環境変数: {os.environ.get('PATH', 'なし')}")
    
    possible_commands = ["marp", "marp.cmd", "marp.exe"]
    
    for cmd in possible_commands:
        found_path = shutil.which(cmd)
        if found_path:
            print(f"✓ Marpコマンドが見つかりました: {found_path}")
            # Windows環境ではフルパスを返す
            if platform.system() == "Windows":
                return found_path
            else:
                return cmd
        else:
            print(f"✗ {cmd} が見つかりません (shutil.which)")
    
    # Windows環境での追加検索
    if platform.system() == "Windows":
        print("Windowsの標準インストールパスを確認中...")
        
        # npm root -g でグローバルパスを取得
        try:
            npm_cmd = "npm.cmd" if shutil.which("npm.cmd") else "npm"
            result = subprocess.run([npm_cmd, "root", "-g"], capture_output=True, text=True, check=True)
            npm_global_root = result.stdout.strip()
            npm_bin_path = os.path.join(npm_global_root, ".bin")
            print(f"npm global root: {npm_global_root}")
            print(f"npm bin path: {npm_bin_path}")
            
            # npm binディレクトリ内のMarpを確認
            for ext in [".cmd", ".exe", ""]:
                marp_path = os.path.join(npm_bin_path, f"marp{ext}")
                print(f"確認中: {marp_path}")
                if os.path.exists(marp_path):
                    print(f"✓ Marpコマンドが見つかりました: {marp_path}")
                    return marp_path
        except Exception as e:
            print(f"npm rootコマンドエラー: {e}")
        
        # 従来の固定パス検索
        npm_global_paths = [
            os.path.expanduser("~\\AppData\\Roaming\\npm\\marp.cmd"),
            os.path.expanduser("~\\AppData\\Roaming\\npm\\marp.exe"),
            "C:\\Program Files\\nodejs\\marp.cmd",
            "C:\\Program Files\\nodejs\\marp.exe"
        ]
        for path in npm_global_paths:
            print(f"確認中: {path}")
            if os.path.exists(path):
                print(f"✓ Marpコマンドが見つかりました: {path}")
                return path
    
    # 最後の手段：直接テスト実行
    print("直接実行テストを試行中...")
    for cmd in possible_commands:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True, check=False, timeout=5)
            if result.returncode == 0:
                print(f"✓ 直接実行でMarpコマンドが動作しました: {cmd}")
                # Windows環境ではwhichでフルパスを取得して返す
                if platform.system() == "Windows":
                    full_path = shutil.which(cmd)
                    return full_path if full_path else cmd
                else:
                    return cmd
            else:
                print(f"✗ {cmd} 実行エラー: {result.stderr}")
        except FileNotFoundError:
            print(f"✗ {cmd} ファイルが見つかりません")
        except Exception as e:
            print(f"✗ {cmd} 実行時エラー: {e}")
    
    print("Marpコマンドが見つかりませんでした")
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
    output_dir_path = config.get("output_dir")

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

    # 出力ディレクトリの設定
    if not output_dir_path or not os.path.exists(output_dir_path):
        # 初回設定時はデフォルト提案
        project_root = Path(__file__).parent.parent
        default_output = project_root / "output"
        
        if ask_yes_no("出力ディレクトリ設定", f"PPTXファイルの出力先を設定してください。\n\nデフォルトの出力先を使用しますか？\n{default_output}\n\n「いいえ」を選ぶと別のフォルダを選択できます。"):
            output_dir_path = str(default_output)
        else:
            output_dir_path = select_directory("PPTXファイルの出力先フォルダを選択してください")
            if not output_dir_path:
                show_message("エラー", "出力ディレクトリが選択されませんでした。デフォルトを使用します。")
                output_dir_path = str(default_output)
        
        config["output_dir"] = output_dir_path
        save_config(config)
        show_message("出力先設定完了", f"出力先が設定されました:\n{output_dir_path}")
    else:
        # 出力ディレクトリの変更確認
        if ask_yes_no("出力先の変更", f"現在の出力先:\n{output_dir_path}\n\n別の出力先に変更しますか？"):
            new_output_dir = select_directory("新しい出力先フォルダを選択してください", output_dir_path)
            if not new_output_dir:
                show_message("出力先変更キャンセル", "出力先の変更をキャンセルしました。現在の設定を使用します。")
            else:
                output_dir_path = new_output_dir
                config["output_dir"] = output_dir_path
                save_config(config)
                show_message("出力先変更完了", f"新しい出力先が設定されました:\n{output_dir_path}")

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
            if platform.system() == "Windows":
                show_message("エラー", "Marp CLIが必要です。\n\n手動でインストールしてください:\n1. コマンドプロンプトを管理者権限で開く\n2. npm.cmd install -g @marp-team/marp-cli を実行\n3. コマンドプロンプトを再起動\n4. このツールを再実行")
            else:
                show_message("エラー", "Marp CLIが必要です。\n\n手動でインストールしてください:\n1. ターミナルを開く\n2. npm install -g @marp-team/marp-cli を実行\n3. このツールを再実行")
            sys.exit(1)

    # ファイル名とパスの処理（日本語対応）
    markdown_path = Path(markdown_file_path)
    file_name = markdown_path.stem
    
    # 設定された出力ディレクトリを使用
    output_dir = Path(output_dir_path)

    # 出力ディレクトリを作成
    output_dir.mkdir(parents=True, exist_ok=True)

    # 出力ファイルパス
    output_file = output_dir / f"{file_name}.pptx"
    
    # テーマファイルの存在確認
    if not os.path.exists(theme_path):
        show_message("エラー", f"テーマファイルが見つかりません:\n{theme_path}\n\n新しいテーマファイルを選択してください。")
        # テーマファイルを再選択
        new_theme_path = select_file("テーマCSSファイルを選択してください", [("CSS files", "*.css")])
        if not new_theme_path:
            show_message("エラー", "テーマファイルが必要です。終了します。")
            sys.exit(1)
        theme_path = new_theme_path
        config["theme_path"] = theme_path
        save_config(config)
    
    # CSSファイルからテーマ名を抽出
    theme_name = extract_theme_name(theme_path)
    
    if theme_name:
        # テーマ名が取得できた場合
        command = [
            marp_command,
            str(markdown_path),
            "--pptx",
            "--output",
            str(output_file),
            "--theme-set",
            str(Path(theme_path).absolute()),
            "--theme",
            theme_name,  # CSSから抽出したテーマ名を使用
            "--allow-local-files",
            "--no-config-file"  # package.jsonの設定を無視
        ]
    else:
        # テーマ名が取得できない場合はファイルパスを直接指定
        print("テーマ名が取得できないため、CSSファイルパスを直接指定します")
        command = [
            marp_command,
            str(markdown_path),
            "--pptx",
            "--output",
            str(output_file),
            "--theme-set",
            str(Path(theme_path).absolute()),
            "--theme",
            str(Path(theme_path).absolute()),
            "--allow-local-files",
            "--no-config-file"  # package.jsonの設定を無視
        ]

    print(f"Generating PPTX for: {markdown_file_path}")
    print(f"Using Marp command: {marp_command}")
    print(f"Executing command: {' '.join(command)}")
    
    # Windows環境での追加デバッグ情報
    if platform.system() == "Windows":
        print(f"実行前のコマンド存在確認:")
        print(f"  shutil.which('{marp_command}'): {shutil.which(marp_command)}")
        print(f"  os.path.exists('{marp_command}'): {os.path.exists(marp_command)}")
        print(f"  現在の作業ディレクトリ: {os.getcwd()}")

    try:
        print("Marpコマンドを実行中...")
        # タイムアウトを30秒に設定してハングアップを防ぐ
        if platform.system() == "Windows":
            # Windows環境ではshell=Trueを試してみる
            print("Windows環境: shell=True で実行します")
            result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8', timeout=30, shell=True)
        else:
            result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=30)
        
        print("Marpコマンドが完了しました")
        print(f"終了コード: {result.returncode}")
        print(f"Marp stdout: {result.stdout}")
        if result.stderr:
            print(f"Marp stderr: {result.stderr}")
        
        # エラーチェック
        if result.returncode != 0:
            error_message = f"Marpコマンドがエラーで終了しました (終了コード: {result.returncode})\n\n"
            if result.stdout:
                error_message += f"標準出力:\n{result.stdout}\n\n"
            if result.stderr:
                error_message += f"エラー出力:\n{result.stderr}\n\n"
            error_message += f"実行コマンド:\n{' '.join(command)}"
            print(f"ERROR: {error_message}")
            sys.exit(1)
        
        print("出力ファイルの確認中...")
        # 出力ファイルが実際に作成されたか確認
        if output_file.exists():
            print("出力ファイルが見つかりました")
            print(f"SUCCESS: PPTXファイルが生成されました: {output_file.absolute()}")
            # 一時的にコンソール出力のみ
            #show_message("変換完了", f"PPTXファイルが正常に生成されました:\n{output_file.absolute()}")
        else:
            print("出力ファイルが見つかりません")
            print(f"WARNING: 出力ファイルが見つかりません: {output_file.absolute()}")
            #show_message("警告", f"コマンドは成功しましたが、出力ファイルが見つかりません:\n{output_file.absolute()}")
    
    except subprocess.TimeoutExpired:
        print("ERROR: Marpコマンドがタイムアウトしました (30秒)")
        print("ERROR: コマンドの実行に時間がかかりすぎています")
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR: '{marp_command}' コマンドが見つかりません")
        if platform.system() == "Windows":
            print("ERROR: Windows環境でMarp CLIが正しくインストールされていない可能性があります")
            print("解決方法:")
            print("1. コマンドプロンプトを管理者権限で開く")
            print("2. npm.cmd install -g @marp-team/marp-cli を実行")
            print("3. コマンドプロンプトを再起動")
            print("4. npm.cmd list -g @marp-team/marp-cli で確認")
        else:
            print("ERROR: Marp CLIがインストールされていない可能性があります")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: 予期しないエラーが発生しました: {str(e)}")
        print(f"ERROR: エラーの種類: {type(e).__name__}")
        sys.exit(1)
    
    print("処理が完了しました")