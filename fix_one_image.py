import argparse
import os
from PIL import Image, ImageOps, ImageFile

# 【关键设置】允许加载截断/损坏的图片，解决 "Corrupt JPEG" 报错
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process_single_image(input_path, output_path=None, target_size=(512, 512), crop_pixels=8):
    """
    处理单张图片：
    1. 修复损坏的文件结构。
    2. 统一尺寸到 target_size。
    3. 切除边缘 crop_pixels 个像素。
    """
    
    if not os.path.exists(input_path):
        print(f"❌ 错误：找不到文件 {input_path}")
        return

    # 如果没有指定输出路径，默认在原文件名后加 "_fixed"
    if output_path is None:
        name, ext = os.path.splitext(input_path)
        output_path = f"{name}_fixed{ext}"

    # 计算中间放大过程的尺寸 (例如 512+4 = 516)
    temp_size = (target_size[0] + 2 * crop_pixels, target_size[1] + 2 * crop_pixels)

    print(f"正在处理: {input_path}")
    print(f"目标尺寸: {target_size} (边缘切除: {crop_pixels}px)")

    try:
        with Image.open(input_path) as img:
            # 转换颜色模式
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # 1. 先放大到稍大尺寸 (例如 516x516)
            # ImageOps.fit 会自动处理非正方形图片，保持比例填满
            img_zoomed = ImageOps.fit(
                img, 
                temp_size, 
                method=Image.Resampling.LANCZOS, 
                centering=(0.5, 0.5)
            )

            # 2. 从中心裁剪回目标尺寸 (512x512)
            # 这样上下左右边缘的 2 像素就被切掉了，顺便去除了损坏的边缘
            left = crop_pixels
            top = crop_pixels
            right = left + target_size[0]
            bottom = top + target_size[1]
            
            final_img = img_zoomed.crop((left, top, right, bottom))

            # 3. 保存 (重新编码会修复文件结构)
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            final_img.save(output_path, quality=95)
            
            print(f"✅ 成功！已保存至: {output_path}")

    except Exception as e:
        print(f"❌ 处理失败: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="修复并裁剪单张图片")
    parser.add_argument("--input", type=str, required=True, help="输入图片路径")
    parser.add_argument("--output", type=str, default=None, help="输出图片路径 (可选，默认另存为 *_fixed.png)")
    
    args = parser.parse_args()

    process_single_image(args.input, args.output)