import sys
import subprocess
import pkg_resources

# 定义需要的依赖包
required = {
    'PyQt6',
    'opencc-python-reimplemented', 
    'ebooklib'
}

# 检查并安装依赖
def check_dependencies():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    
    if missing:
        print("正在安装缺失的依赖包...")
        python = sys.executable
        subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
        print("依赖包安装完成")

# 启动主程序
def run_main():
    try:
        from main import MainWindow
        from PyQt6.QtWidgets import QApplication
        import sys
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"程序启动失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    check_dependencies()
    run_main()
