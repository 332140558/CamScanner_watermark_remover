import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

class WatermarkRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 工具箱 (全能扫描王去水印 & 拆分)")
        self.root.geometry("600x350")

        # 创建 Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- Tab 1: 去水印 ---
        self.tab_watermark = tk.Frame(self.notebook)
        self.notebook.add(self.tab_watermark, text="去水印")
        
        # 去水印变量
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.setup_watermark_tab()

        # --- Tab 2: 拆分 ---
        self.tab_split = tk.Frame(self.notebook)
        self.notebook.add(self.tab_split, text="PDF拆分")
        
        # 拆分变量
        self.split_input_path = tk.StringVar()
        
        self.setup_split_tab()

        # 公共状态标签 (放在底部，不在 Tab 里)
        self.status_label = tk.Label(self.root, text="准备就绪", fg="gray")
        self.status_label.pack(side="bottom", pady=10)

    def setup_watermark_tab(self):
        # 输入文件选择
        tk.Label(self.tab_watermark, text="选择PDF原文件:").pack(pady=5, anchor="w", padx=20)
        input_frame = tk.Frame(self.tab_watermark)
        input_frame.pack(fill="x", padx=20)
        tk.Entry(input_frame, textvariable=self.input_path, width=50).pack(side="left", fill="x", expand=True)
        tk.Button(input_frame, text="浏览", command=self.select_input_file).pack(side="right", padx=5)

        # 输出路径选择
        tk.Label(self.tab_watermark, text="保存路径 (文件名):").pack(pady=5, anchor="w", padx=20)
        output_frame = tk.Frame(self.tab_watermark)
        output_frame.pack(fill="x", padx=20)
        tk.Entry(output_frame, textvariable=self.output_path, width=50).pack(side="left", fill="x", expand=True)
        tk.Button(output_frame, text="浏览", command=self.select_output_file).pack(side="right", padx=5)

        # 开始按钮
        tk.Button(self.tab_watermark, text="开始去水印", command=self.process_pdf, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

    def setup_split_tab(self):
        # 输入文件选择
        tk.Label(self.tab_split, text="选择PDF原文件:").pack(pady=5, anchor="w", padx=20)
        input_frame = tk.Frame(self.tab_split)
        input_frame.pack(fill="x", padx=20)
        tk.Entry(input_frame, textvariable=self.split_input_path, width=50).pack(side="left", fill="x", expand=True)
        tk.Button(input_frame, text="浏览", command=self.select_split_input_file).pack(side="right", padx=5)

        # 说明
        tk.Label(self.tab_split, text="说明: 拆分后的文件将保存在原文件目录下的 '_split' 文件夹中。", fg="gray").pack(pady=10, padx=20, anchor="w")

        # 开始按钮
        tk.Button(self.tab_split, text="开始拆分", command=self.process_split, bg="#2196F3", fg="white", font=("Arial", 12)).pack(pady=20)

    def select_split_input_file(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filename:
            self.split_input_path.set(filename)

    def process_split(self):
        input_file = self.split_input_path.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("错误", "请选择有效的输入文件")
            return

        try:
            self.status_label.config(text="正在拆分...", fg="blue")
            self.root.update()

            # 创建输出目录
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_dir = os.path.join(os.path.dirname(input_file), f"{base_name}_split")
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            doc = fitz.open(input_file)
            total_pages = len(doc)
            
            for i in range(total_pages):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=i, to_page=i)
                output_path = os.path.join(output_dir, f"{i+1}.pdf")
                new_doc.save(output_path)
                new_doc.close()
                
                if i % 5 == 0:
                    self.status_label.config(text=f"正在拆分: {i+1}/{total_pages}", fg="blue")
                    self.root.update()

            doc.close()
            
            self.status_label.config(text="拆分完成!", fg="green")
            messagebox.showinfo("成功", f"拆分完成!\n文件已保存至:\n{output_dir}")

        except Exception as e:
            self.status_label.config(text="拆分失败", fg="red")
            messagebox.showerror("错误", f"拆分过程中发生错误:\n{str(e)}")

    def select_input_file(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filename:
            self.input_path.set(filename)
            # 自动设置默认输出路径
            base, ext = os.path.splitext(filename)
            self.output_path.set(f"{base}_no_watermark{ext}")

    def select_output_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if filename:
            self.output_path.set(filename)

    def process_pdf(self):
        input_file = self.input_path.get()
        output_file = self.output_path.get()

        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("错误", "请选择有效的输入文件")
            return
        
        if not output_file:
            messagebox.showerror("错误", "请选择保存路径")
            return

        try:
            self.status_label.config(text="正在处理...", fg="blue")
            self.root.update()
            
            self.remove_watermark(input_file, output_file)
            
            self.status_label.config(text="处理完成!", fg="green")
            messagebox.showinfo("成功", f"文件已保存至:\n{output_file}")
            
        except Exception as e:
            self.status_label.config(text="处理失败", fg="red")
            messagebox.showerror("错误", f"处理过程中发生错误:\n{str(e)}")

    def remove_watermark(self, input_path, output_path):
        """
        去除水印的核心逻辑。
        针对全能扫描王，通常是在右下角。
        这里采用绘制白色矩形覆盖的方式。
        """
        doc = fitz.open(input_path)
        
        for page in doc:
            # 获取页面尺寸
            rect = page.rect
            width = rect.width
            height = rect.height
            
            # 定义覆盖区域 (右下角)
            # 全能扫描王的水印通常在右下角，大约占据宽度的 1/3 到 1/4，高度的底部一小部分
            # 这里需要根据实际情况微调。
            # 假设水印在右下角，高度约为 30-50 像素，宽度约为 150-200 像素
            # 坐标系原点在左上角
            
            # 策略：覆盖右下角的一个矩形区域
            # x0, y0, x1, y1
            # 覆盖区域：右边距 0，底边距 0，宽 180，高 40 (根据经验值估算)
            
            watermark_width = 200
            watermark_height = 50
            
            # 构造遮盖矩形
            # 右下角坐标是 (width, height)
            # 左上角坐标是 (width - watermark_width, height - watermark_height)
            
            clip_rect = fitz.Rect(width - watermark_width, height - watermark_height, width, height)
            
            # 绘制白色矩形覆盖
            # fill color (1, 1, 1) is white
            page.draw_rect(clip_rect, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

        doc.save(output_path)
        doc.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkRemoverApp(root)
    root.mainloop()
