import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import rawpy
import imageio
import traceback

class NEFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("尼康NEF转JPG工具 (终极修复版)")
        self.root.geometry("500x350")
        
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(self.frame, text="请选择包含 .NEF 文件的文件夹", font=("Arial", 12))
        self.label.pack(pady=10)

        self.btn_select = tk.Button(self.frame, text="选择文件夹并开始转换", command=self.start_thread, height=2, bg="#ddd")
        self.btn_select.pack(pady=10, fill=tk.X)

        self.progress = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(pady=20, fill=tk.X)

        self.status_label = tk.Label(self.frame, text="等待开始...", fg="gray", wraplength=400)
        self.status_label.pack()

    def start_thread(self):
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
        
        output_dir = os.path.join(folder_path, "JPG_Output")
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出文件夹: {e}")
                self.btn_select.config(state=tk.NORMAL)
                return

        success_count = 0
        error_shown = False 

        for idx, file in enumerate(files):
            input_path = os.path.join(folder_path, file)
            output_path = os.path.join(output_dir, os.path.splitext(file)[0] + ".jpg")
            
            self.status_label.config(text=f"正在处理: {file}")
            
            try:
                # --- 核心修改开始 ---
                # 不直接传路径，而是先用 Python 打开文件，彻底避开 C++ 路径编码 Bug
                with open(input_path, 'rb') as source_file:
                    with rawpy.imread(source_file) as raw:
                        # use_camera_wb=True: 使用拍摄时的白平衡
                        # bright=1.0: 保持默认亮度
                        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=False, bright=1.0)
                        imageio.imsave(output_path, rgb, quality=95, subsampling=0)
                # --- 核心修改结束 ---
                
                success_count += 1
            except Exception as e:
                print(f"Failed: {file} - {e}")
                if not error_shown:
                    # 获取详细报错并弹窗
                    error_msg = traceback.format_exc()
                    self.root.after(0, lambda m=error_msg, f=file: messagebox.showerror(
                        "转换失败", 
                        f"文件: {f}\n\n这可能是因为文件已损坏或相机型号太新。\n\n详细错误:\n{m}"
                    ))
                    error_shown = True

            self.progress['value'] = idx + 1
            self.root.update_idletasks()

        self.status_label.config(text=f"完成！成功: {success_count}, 失败: {len(files) - success_count}")
        self.btn_select.config(state=tk.NORMAL)
        
        if success_count > 0:
            messagebox.showinfo("完成", f"成功转换 {success_count} 张图片！\n保存在: {output_dir}")
        elif not error_shown:
            messagebox.showwarning("提示", "没有转换任何图片，但也没有检测到严重错误。")

if __name__ == "__main__":
    root = tk.Tk()
    app = NEFConverterApp(root)
    root.mainloop()