# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:19:33 2023
@author: zhao
"""

import sys
from PyQt5 import QtWidgets, QtCore
import os
import fitz  # PyMuPDF

'''
PyQt5:
    QtWidgets:
        QApplication
        QWidget
        QDialog
        QMainWindow
        QLabel
        QFileDialog
    QtCore:
        pyqtSignal
        pyqtSlot
        Qt
        QObject
    QtGui
'''

import MarkPDF_ui  # 导入ui.py创建的类

class QMarkPDF(QtWidgets.QMainWindow):
    '''
    LocalBlastGUI逻辑部分
    '''
    def __init__(self, parent=None):
        
        super().__init__(parent) # 继承QtWidgets.QMainWindow
        self.ui = MarkPDF_ui.Ui_MarkPDF()
        self.ui.setupUi(self)

##  ===============================有connectSlotsByName()自动关联的槽函数===============================
    def highlight_multiple_keywords(self, pdf_path, search_keywords, output_path):
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            # 获取页面
            page = pdf_document[page_num]
            # 在页面中搜索每个关键词并进行高亮标记
            for keyword in search_keywords:
                text_instances = page.search_for(keyword)
                # 高亮每个匹配的文本
                for inst in text_instances:
                    rect = inst.irect  # 获取文本边界框
                    highlight = page.add_highlight_annot(rect)  # 在文本周围添加高亮标注
                    highlight.set_colors()  # 设置高亮颜色为黄色
        # 保存带有高亮标记的PDF
        pdf_document.save(output_path)
        # 关闭PDF文件
        pdf_document.close()

    def walk(self, input_dir, query_list, output_dir):
        for path, dir_list, file_list in os.walk(input_dir):
            for dir_rec in file_list:
                print(dir_rec)
                self.highlight_multiple_keywords(os.path.join(input_dir,dir_rec), query_list, os.path.join(output_dir, dir_rec))

    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        # self.mark_in_pdf()
        # print(self.inputDir)
        # print(self.outputDir)
        # print(self.ui.textEdit.toPlainText())
        query_line = self.ui.textEdit.toPlainText()
        query_list = query_line.split(";")
        print('='*100)
        print("标记关键词为：", query_list)
        print('+'*100)
        try:
            self.walk(input_dir=self.ui.lineEdit_2.text(), query_list=query_list, output_dir=self.ui.lineEdit_3.text())
        except:
            if self.ui.lineEdit_2.text() == self.ui.lineEdit_3.text():
                QtWidgets.QMessageBox.warning(self,"错误","输入和输出文件夹不能相同！")
            else:
                QtWidgets.QMessageBox.warning(self,"错误", "标记失败！")
        print('='*100)
        print('标记文件保存至MatchPDF文件夹中')

    @QtCore.pyqtSlot()
    def on_pushButton_2_clicked(self):
        try:
            self.inputDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输入路径")
            print(f"输入文件位置{self.inputDir}")
            self.ui.lineEdit_2.setText(self.inputDir)
        except:
            QtWidgets.QMessageBox.warning(self, "错误", "输入路径出错！")

    @QtCore.pyqtSlot()
    def on_pushButton_3_clicked(self):
        try:
            self.outputDir = QtWidgets.QFileDialog.getExistingDirectory(self, "选择输出路径")
            print(f"输出文件位置{self.outputDir}")
            self.ui.lineEdit_3.setText(self.outputDir)
        except:
            QtWidgets.QMessageBox.warning(self, "错误", "输出路径出错！")

    @QtCore.pyqtSlot()
    def on_pushButton_4_clicked(self):
        try:
            cmd = "Bins\SciHub.exe"
            os.popen(cmd)
        except:
            QtWidgets.QMessageBox.warning(self, "错误", "无法打开SciHub")

if __name__ == "__main__":
    '''
    appMain创建应用程序和窗体，然后显示窗体，并开始运行应用程序；
    将ui.py文件的测试运行部分单独拿出来作为一个文件。
    当一个应用程序有多个窗体，并且窗体之间有数据传输时，
    appMain.py负责创建应用程序的主窗体并运行起来，
    这样整个应用程序的结构就更加清晰了。
    '''
    app = QtWidgets.QApplication(sys.argv)  # 第一步创建GUI应用程序，固定步骤

    window = QMarkPDF()  # 第二步在应用上创建主窗口
    window.show()  # 显示主窗口所有内容

    sys.exit(app.exec_())  # 执行应用循环，固定步骤

# import fitz  # PyMuPDF
# import os

# def highlight_multiple_keywords(pdf_path, search_keywords, output_path):
#     # 打开PDF文件
#     pdf_document = fitz.open(pdf_path)

#     for page_num in range(pdf_document.page_count):
#         # 获取页面
#         page = pdf_document[page_num]

#         # 在页面中搜索每个关键词并进行高亮标记
#         for keyword in search_keywords:
#             text_instances = page.search_for(keyword)

#             # 高亮每个匹配的文本
#             for inst in text_instances:
#                 rect = inst.irect  # 获取文本边界框
#                 highlight = page.add_highlight_annot(rect)  # 在文本周围添加高亮标注
#                 highlight.set_colors()  # 设置高亮颜色为黄色

#     # 保存带有高亮标记的PDF
#     pdf_document.save(output_path)

#     # 关闭PDF文件
#     pdf_document.close()

# def walk(input_dir, query, output_dir):
#     print(input_dir)
#     if not os.path.exists('MatchPDF'):
#         os.mkdir('MatchPDF')
#     for path, dir_list, file_list in os.walk(input_dir):
#         for dir_rec in file_list:
#             print(dir_rec)
#             highlight_multiple_keywords(os.path.join(input_dir,dir_rec), query_list, os.path.join(output_dir, dir_rec))

# if __name__ == "__main__":
#     with open('query.txt', 'r') as f:
#         for query_line in f.readlines():
#             # print(query_line)
#             query_list = query_line.split(";")
#             print('='*100)
#             print("标记关键词为：", query_list)
#             print('+'*100)
#             walk(input_dir='RawPDF/', query="metagenome;FWD", output_dir='MatchPDf')
#     print('='*100)
#     print('标记文件保存至MatchPDF文件夹中')
#     input("按回车键结束...")

# D:\ProgramFiles\miniconda3\envs\pdf\Scripts\pyinstaller.exe -F MarkPDF_logic.py

# import fitz  # PyMuPDF

# def highlight_multiple_keywords_colors(pdf_path, keyword_colors, output_path):
#     # 打开PDF文件
#     pdf_document = fitz.open(pdf_path)

#     for page_num in range(pdf_document.page_count):
#         # 获取页面
#         page = pdf_document[page_num]

#         # 遍历关键词和颜色
#         for keyword, color in keyword_colors.items():
#             text_instances = page.search_for(keyword)

#             # 高亮每个匹配的文本
#             for inst in text_instances:
#                 rect = inst.irect  # 获取文本边界框
#                 highlight = page.add_highlight_annot(rect)  # 在文本周围添加高亮标注
#                 highlight.set_colors(color)  # 设置高亮颜色

#     # 保存带有高亮标记的PDF
#     pdf_document.save(output_path)

#     # 关闭PDF文件
#     pdf_document.close()

# # 示例：在example.pdf中搜索"Python"和"PDF"并用不同颜色进行高亮标记，保存为output_highlighted.pdf
# # keywords_and_colors = {"microbiome": (1, 1, 1), "FWD": (0, 0, 0)}
# keywords_and_colors = {"microbiome": (0.9411764705882353, 0.9725490196078431, 1.0), "FWD": (0, 0, 0)}
# highlight_multiple_keywords_colors("006 生物信息学\pubmed_pdf\RawPDF\Gao-2021-Disease-induced changes in plant micr.pdf", \
#                             keywords_and_colors, \
#                                 "006 生物信息学\pubmed_pdf\MatchPDF\match.pdf")