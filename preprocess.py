import os
from PIL import Image, ImageOps
from tqdm import tqdm
import argparse
import shutil

def process_dataset(source_root, target_root, target_size=(512, 512)):
    """
    遍历数据集，将所有图片调整为 target_size。
    策略 Resize + Center Crop (利用 ImageOps.fit)，最大程度保留画面内容。
    """
    # 支持的图片扩展名
    valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff'}
    
    # 获取所有文件列表
    files_to_process = []
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if os.path.splitext(file)[1].lower() in valid_extensions:
                files_to_process.append(os.path.join(root, file))

    print(f"找到 {len(files_to_process)} 张图片，准备处理...")
    print(f"源路径: {source_root}")
    print(f"目标路径: {target_root}")
    print(f"目标尺寸: {target_size}")

    for src_path in tqdm(files_to_process, desc="Processing"):
        # 计算目标文件路径
        rel_path = os.path.relpath(src_path, source_root)
        dst_path = os.path.join(target_root, rel_path)
        
        # 创建目标文件夹
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        try:
            with Image.open(src_path) as img:
                # 转换颜色模式，防止 RGBA 导致的问题
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 使用 ImageOps.fit 实现 "Scale and Crop"
                # centering=(0.5, 0.5) 表示从中心向四周裁剪
                # method=Image.Resampling.LANCZOS 保证缩放质量
                processed_img = ImageOps.fit(
                    img, 
                    target_size, 
                    method=Image.Resampling.LANCZOS, 
                    centering=(0.5, 0.5)
                )

                # 保存图片
                processed_img.save(dst_path, quality=95)
                
        except Exception as e:
            print(f"处理图片 {src_path} 时出错: {e}")

    # 复制非图片文件 (如 json, txt 等，如果有的话)
    print("正在复制非图片文件...")
    for root, dirs, files in os.walk(source_root):
        for file in files:
            if os.path.splitext(file)[1].lower() not in valid_extensions:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, source_root)
                dst_file = os.path.join(target_root, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)

    print("处理完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将数据集图片统一处理为指定尺寸 (512x512)")
    parser.add_argument("--data_root", type=str, required=True, help="原始数据集的根目录路径")
    parser.add_argument("--output_root", type=str, default=None, help="处理后数据集的保存路径 (默认在原名后加_512)")
    
    args = parser.parse_args()

    source_dir = args.data_root
    if args.output_root is None:
        # 如果路径以 / 结尾，先去掉
        if source_dir.endswith(('/', '\\')):
            source_dir = source_dir[:-1]
        target_dir = source_dir + "_512"
    else:
        target_dir = args.output_root

    process_dataset(source_dir, target_dir, target_size=(512, 512))