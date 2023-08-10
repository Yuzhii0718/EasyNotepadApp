# coding:utf-8
"""
**************************************************
@File   ：PyQt6_QuickStart -> Notepad
@IDE    ：PyCharm
@Author ：Yuzhii0718
@Date   ：2023/8/10 20:53
**************************************************
"""
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtGui import QFont

from Part_3.notePadDemo import Ui_MainWindow


class NotepadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(NotepadWindow, self).__init__()
        self.setupUi(self)

        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionSave.triggered.connect(self.save_file)
        self.actionExit.triggered.connect(self.exit_file)
        self.actionCopy.triggered.connect(self.copy_file)
        self.actionCut.triggered.connect(self.cut_file)
        self.actionPaste.triggered.connect(self.paste_file)
        self.actionUndo.triggered.connect(self.undo_file)
        self.actionRedo.triggered.connect(self.redo_file)
        self.actionAbout_app.triggered.connect(self.about_app)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_preview.triggered.connect(self.preview_dialog)
        self.actionExport_pdf.triggered.connect(self.export_pdf)
        self.actionBold.triggered.connect(self.set_bold)
        self.actionItalic.triggered.connect(self.set_italic)
        self.actionUnderline.triggered.connect(self.set_underline)
        self.actionLeft.triggered.connect(self.set_left)
        self.actionRight.triggered.connect(self.set_right)
        self.actionCenter.triggered.connect(self.set_center)
        self.actionJustify.triggered.connect(self.set_justify)
        self.actionFont.triggered.connect(self.set_font)
        self.actionColor.triggered.connect(self.set_color)

        self.textEdit.textChanged.connect(self.text_change)

        self.filename = ""

    def new_file(self):
        if self.maybe_save():
            self.textEdit.clear()
            self.filename = ""

    def open_file(self):
        # 将 .py, .c, .cpp, .h, .txt 文件类型添加到文件筛选器中
        # 如果文件不是 txt 格式，则视作 txt 文件打开
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "All Files (*);;Text Files (*.txt)")
        if filename:
            with open(filename, "r") as f:
                self.textEdit.setText(f.read())
                self.filename = filename
                self.setWindowTitle(f"{filename} - Yuzhii 的 Notepad")

    def save_file(self):
        if self.filename == "":
            filename, _ = QFileDialog.getSaveFileName(self, "Save File")
            if filename:
                with open(filename, "w") as f:
                    f.write(self.textEdit.toPlainText())
                    self.filename = filename
                    self.setWindowTitle(f"{filename} - Yuzhii 的 Notepad")
                    QMessageBox.about(self, "Save File", "File saved successfully.")

    def exit_file(self):
        self.close()

    def copy_file(self):
        self.textEdit.copy()

    def cut_file(self):
        self.textEdit.cut()

    def paste_file(self):
        self.textEdit.paste()

    def undo_file(self):
        self.textEdit.undo()

    def redo_file(self):
        self.textEdit.redo()

    def about_app(self):
        QMessageBox.about(self, "About Notepad", "This is a Notepad demo.\n\nAuthor: Yuzhii0718")

    def text_change(self):
        self.actionSave.setEnabled(True)

    def maybe_save(self):
        if not self.textEdit.document().isModified():
            return True

        ret = QMessageBox.warning(self, "Notepad", "The document has been modified.\nDo you want to save "
                                                   "your changes?",
                                  QMessageBox.StandardButton.Save |
                                  QMessageBox.StandardButton.Discard |
                                  QMessageBox.StandardButton.Cancel)
        if ret == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def unsave(self):
        # 检测文档是否被修改过，修改过则在窗口标题后加上 * 号
        if self.textEdit.document().isModified():
            self.setWindowTitle(f"{self.filename} - Yuzhii 的 Notepad *")

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.accepted:
            self.textEdit.print(printer)

    def preview_dialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_preview)
        preview_dialog.exec()

    def print_preview(self, printer):
        self.textEdit.print(printer)

    def export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export PDF", ".", "PDF files (*.pdf);;All Files (*)")
        if filename != "":
            if QFileInfo(filename).suffix() == "": filename += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            self.textEdit.document().print(printer)

    def set_bold(self):
        self.textEdit.setFontWeight(QFont.Weight.Bold if self.textEdit.fontWeight() < QFont.Weight.Bold
                                    else QFont.Weight.Normal)

    def set_italic(self):
        self.textEdit.setFontItalic(not self.textEdit.fontItalic())

    def set_underline(self):
        self.textEdit.setFontUnderline(not self.textEdit.fontUnderline())

    def set_left(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def set_right(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def set_center(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_justify(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def set_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setCurrentFont(font)

    def set_color(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotepadWindow()
    window.show()
    sys.exit(app.exec())
