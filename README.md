# EPUB繁简转换器

一个简单的GUI工具，用于将EPUB格式的电子书从繁体中文转换为简体中文。

## 功能

- 选择EPUB文件进行转换
- 自动识别EPUB文件中的HTML内容
- 使用OpenCC进行繁体到简体的转换
- 保留原EPUB文件的所有结构和元数据
- 显示转换进度

## 安装

1. 确保已安装Python 3.x
2. 安装所需依赖：
   ```bash
   pip install PyQt6 opencc-python-reimplemented ebooklib
   ```

## 使用方法

1. 运行程序：
   ```bash
   python main.py
   ```
2. 选择转换模式：
   - 单个文件转换：拖拽EPUB文件到窗口或点击"选择文件"按钮
   - 批量转换：拖拽多个EPUB文件或点击"批量转换"按钮选择文件夹
3. 点击"开始转换"按钮开始转换过程
4. 转换完成后，会在原文件所在目录生成新文件，文件名格式为`简体化_原文件名.epub`
5. 批量转换时会显示整体进度和当前正在处理的文件

## 依赖项

- PyQt6 (用于GUI界面)
- opencc-python-reimplemented (繁简转换)
- ebooklib (EPUB文件处理)

## 注意事项

- 请确保输入的EPUB文件是有效的
- 转换过程可能需要一些时间，取决于文件大小
- 转换后的文件会保留原文件的所有格式和样式
