# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QProgressBar
from PyQt6.QtCore import Qt
import sys
import os
import shutil
import zipfile
import tempfile
from opencc import OpenCC
from ebooklib import epub

# 定义文档类型常量
EPUB_DOCUMENT = 9  # 根据ebooklib源代码，EPUB_DOCUMENT的值为9

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('EPUB繁简转换器')
        self.setGeometry(100, 100, 400, 300)
        
        # 创建主控件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 添加UI元素
        self.hint_label = QLabel('拖拽EPUB文件到此处或点击下方按钮选择')
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.hint_label.font()
        font.setBold(True)
        font.setPointSize(12)
        self.hint_label.setFont(font)
        layout.addWidget(self.hint_label)
        
        self.label = QLabel('选择EPUB文件进行繁简转换')
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        
        # 添加开始转换按钮
        self.start_button = QPushButton('开始转换')
        self.start_button.clicked.connect(self.start_conversion)
        self.start_button.setEnabled(False)  # 初始禁用
        layout.addWidget(self.start_button)
        
        # 添加选择文件按钮
        self.select_button = QPushButton('选择文件')
        self.select_button.clicked.connect(self.select_file)
        layout.addWidget(self.select_button)
        
        # 添加批量转换按钮
        self.batch_button = QPushButton('批量转换')
        self.batch_button.clicked.connect(self.select_folder)
        layout.addWidget(self.batch_button)
        
        # 启用拖拽功能
        self.setAcceptDrops(True)
        
        # 初始化转换器
        self.cc = OpenCC('t2s')  # 繁体转简体
        self.selected_file = None  # 存储选择的文件路径
        
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择EPUB文件', '', 'EPUB文件 (*.epub)'
        )
        if file_path:
            self.selected_file = file_path
            self.label.setText(f'已选择: {os.path.basename(file_path)}')
            self.start_button.setEnabled(True)  # 启用开始转换按钮
    
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            self.selected_folder = folder_path
            self.label.setText(f'已选择文件夹: {os.path.basename(folder_path)}')
            self.start_button.setEnabled(True)  # 启用开始转换按钮
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().lower().endswith('.epub') for url in urls):
                event.acceptProposedAction()
    
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        epub_files = [url.toLocalFile() for url in urls 
                     if url.toLocalFile().lower().endswith('.epub')]
        if epub_files:
            if len(epub_files) == 1:
                self.selected_file = epub_files[0]
                self.label.setText(f'已选择: {os.path.basename(epub_files[0])}')
            else:
                self.selected_folder = os.path.dirname(epub_files[0])
                self.label.setText(f'已选择多个文件: {len(epub_files)}个EPUB文件')
            self.start_button.setEnabled(True)
    
    def start_conversion(self):
        if hasattr(self, 'selected_file') and self.selected_file:
            self.convert_epub([self.selected_file])
        elif hasattr(self, 'selected_folder') and self.selected_folder:
            epub_files = [os.path.join(self.selected_folder, f) 
                         for f in os.listdir(self.selected_folder) 
                         if f.lower().endswith('.epub')]
            if epub_files:
                self.convert_epub(epub_files)
            else:
                self.label.setText('文件夹中没有找到EPUB文件')
    
    def convert_epub(self, file_paths):
        try:
            self.progress.setValue(0)
            self.start_button.setEnabled(False)  # 转换期间禁用按钮
            
            total_files = len(file_paths)
            for file_idx, file_path in enumerate(file_paths):
                self.label.setText(f'正在处理 {file_idx+1}/{total_files}: {os.path.basename(file_path)}')
                
                # 准备输出文件路径
                dir_name = os.path.dirname(file_path)
                base_name = os.path.basename(file_path)
                name, ext = os.path.splitext(base_name)
                output_path = os.path.join(dir_name, f'简体化_{name}{ext}')
                
                # 读取EPUB文件
                book = epub.read_epub(file_path)
                
                # 处理每个HTML文件
                items = [item for item in book.get_items() if item.get_type() == EPUB_DOCUMENT]
                for i, item in enumerate(items):
                    content = item.get_content().decode('utf-8')
                    converted = self.cc.convert(content)
                    item.set_content(converted.encode('utf-8'))
                    # 更新文件内进度 (0-90%) 和整体进度 (0-100%)
                    file_progress = int((i + 1) / len(items) * 90)
                    total_progress = int((file_idx + (i + 1)/len(items)) / total_files * 100)
                    self.progress.setValue(total_progress)
                    
                # 保存转换后的EPUB文件
                epub.write_epub(output_path, book)
                self.progress.setValue(int((file_idx + 1) / total_files * 100))
            
            self.label.setText(f'批量转换完成: {total_files}个文件')
            self.start_button.setEnabled(True)  # 转换完成重新启用按钮
            
        except Exception as e:
            self.label.setText(f'错误: {str(e)}')
            self.progress.setValue(0)
            self.start_button.setEnabled(True)  # 出错时重新启用按钮

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
