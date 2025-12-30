# Nikon NEF to JPG Converter

A simple, standalone tool for batch converting Nikon RAW (.nef) files to high-quality JPGs. Designed for simplicity and ease of use.

一个极简的尼康 RAW (.nef) 批量转 JPG 工具。主打无损画质与操作便捷，无需安装，开箱即用。

---

## 🇬🇧 English

### Features

* **One-Click Operation:** Simple GUI, no command line needed.
* **Batch Processing:** Converts all `.nef` files in a selected folder automatically.
* **High Quality:** Uses `LibRaw` (via `rawpy`) for high-fidelity conversion.
* **Portable:** Single `.exe` file, no installation or Python environment required.

### How to Use

1.  **[📥 Download Latest Version (converter.exe)](releases/latest)** from the Releases page.
2.  Double-click to run (ignore Windows Defender warnings if they appear).
3.  Click the button and select the folder containing your `.nef` photos.
4.  The program will create a `JPG_Output` folder inside and save the converted images there.

### ⚠️ Important Compatibility Note

* **Supported:** Uncompressed RAW, Lossless Compressed RAW.
* **Not Supported:** **High Efficiency (HE / HE*)** compression (found in Z9, Z8, Z6 III, Zf).
  * *Solution:* Please set your camera to **"Lossless Compression"** for future compatibility.

---

## 🇨🇳 中文说明

### 主要功能

* **极简操作**：带图形界面，无需任何编程基础，点一下就能用。
* **批量转换**：自动扫描选中文件夹下的所有 `.nef` 文件并转换。
* **高画质**：基于 `LibRaw` 工业级解码，保留最佳图片细节。
* **便携免安**：单文件 `.exe`，无需安装 Python 环境。

### 使用方法
1.  **[📥 点击这里下载最新版工具 (converter.exe)](releases/latest)**
    * *点击后，在 Assets 区域找到 converter.exe 下载即可。*
2.  双击运行（如果是自制软件，杀毒软件可能会提示，允许运行即可）。
3.  点击按钮，选择存放 `.nef` 照片的文件夹。
4.  程序会自动在该文件夹下新建 `JPG_Output` 目录，转换好的图片都在里面。

### ⚠️ 重要兼容性提示

* **支持**：无损压缩 (Lossless Compression)、未压缩 RAW。
* **不支持**：尼康较新机型（如 Z6 III, Z8, Z9）的 **“高效率 (HE / HE*)”** 格式。
  * *解决方法*：请在相机菜单中，将 RAW 记录格式设置为 **“无损压缩”** 即可完美支持。
