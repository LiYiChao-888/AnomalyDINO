import os
import shutil

def batch_rename_folders(root_path, target_name="GroundTruth", new_name="ground_truth"):
    """
    遍历数据集目录，将所有名为 target_name 的文件夹重命名为 new_name。
    """
    if not os.path.exists(root_path):
        print(f"错误：路径不存在 -> {root_path}")
        return

    print(f"开始扫描目录: {root_path} ...")
    count = 0

    # os.walk 会递归遍历所有子目录
    # topdown=False 确保我们可以先处理子目录（虽然对于重命名文件夹本身不是严格必须，但在修改目录结构时更安全）
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        
        # 检查当前目录下是否有我们要改名的文件夹
        if target_name in dirnames:
            old_dir = os.path.join(dirpath, target_name)
            new_dir = os.path.join(dirpath, new_name)
            
            try:
                # 检查目标文件夹名是否已经存在，避免冲突
                if os.path.exists(new_dir):
                    print(f"[跳过] 目标已存在，未执行重命名: {new_dir}")
                else:
                    os.rename(old_dir, new_dir)
                    print(f"[成功] 重命名: {old_dir} -> {new_dir}")
                    count += 1
            except Exception as e:
                print(f"[错误] 无法重命名 {old_dir}: {e}")

    print(f"\n处理完成!共修改了 {count} 个文件夹。")

if __name__ == "__main__":
    # ================= 配置区域 =================
    # 请在这里填入你的数据集根目录路径
    # 例如: "D:/datasets/ydfid" 或 "/home/user/data/ydfid"
    dataset_root = "/data/Users/liyc/myProject/AnomalyDINO-LYC/data/ydfid" 
    # ===========================================

    # 二次确认，防止误操作
    confirm = input(f"即将把 '{dataset_root}' 下所有的 'defect-free' 重命名为 'good'。\n请确认 (y/n): ")
    if confirm.lower() == 'y':
        batch_rename_folders(dataset_root)
    else:
        print("操作已取消。")