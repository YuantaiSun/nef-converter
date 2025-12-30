import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import rawpy
import imageio

class NEFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("尼康NEF转JPG工具 (无损画质版)")
        self.root.geometry("500x300")
        
        # 布局
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(self.frame, text="请选择包含 .NEF 文件的文件夹", font=("Arial", 12))
        self.label.pack(pady=10)

        self.btn_select = tk.Button(self.frame, text="选择文件夹并开始转换", command=self.start_thread, height=2, bg="#ddd")
        self.btn_select.pack(pady=10, fill=tk.X)

        self.progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(pady=20, fill=tk.X)

        self.status_label = tk.Label(self.frame, text="等待开始...", fg="gray")
        self.status_label.pack()

    def start_thread(self):
        # 使用线程避免界面卡死
        threading.Thread(target=self.convert_process, daemon=True).start()

    def convert_process(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.nef')]
        
        if not files:
            messagebox.showinfo("提示", "该文件夹下没有找到 .nef 文件")
            return

        self.btn_select.config(state=tk.DISABLED)
        self.progress['maximum'] = len(files)
        self.progress['value'] = 0
        
        # 创建输出文件夹
        output_dir = os.path.join(folder_path, "JPG_Output")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        success_count = 0
        
        for idx, file in enumerate(files):
            input_path = os.path.join(folder_path, file)
            output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".jpg")
            
            self.status_label.config(text=f"正在处理: {file} ({idx+1}/{len(files)})")
            
            try:
                with rawpy.imread(input_path) as raw:
                    # postprocess 将 RAW 数据demosaic成 RGB 图像
                    # use_camera_wb=True 使用拍摄时的白平衡
                    # no_auto_bright=False 允许自动调整亮度以匹配相机预览
                    rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=False, bright=1.0)
                    
                    # 保存为 JPG，quality=95 接近无损，subsampling=0 保证色彩采样不压缩
                    imageio.imsave(output_path, rgb, quality=95, subsampling=0)
                    success_count += 1
            except Exception as e:
                print(f"Error converting {file}: {e}")

            self.progress['value'] = idx + 1
            self.root.update_idletasks()

        self.status_label.config(text=f"完成！成功转换 {success_count} 张图片。")
        self.btn_select.config(state=tk.NORMAL)
        messagebox.showinfo("成功", f"处理完成！\n图片已保存在: {output_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NEFConverterApp(root)
    root.mainloop()