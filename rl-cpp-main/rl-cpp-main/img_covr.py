from PIL import Image
import os

# 定义原始地图和调整大小后地图的路径
original_map_path = r"C:\Users\86139\Desktop\Ypr_project\rl_cpp\maps\eval_exploration_5.png"
resized_map_path = r"C:\Users\86139\Desktop\Ypr_project\rl_cpp\maps\eval_exploration_5_32.png"

# 检查原始地图文件是否存在
if not os.path.exists(original_map_path):
    print(f"错误: 文件 {original_map_path} 不存在。")
    exit(1)

try:
    # 打开原始地图图像
    with Image.open(original_map_path) as img:
        # 如果图像不是RGB模式，则转换为RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 调整图像大小为32x32，使用抗锯齿滤镜以获得更好的质量
        img_resized = img.resize((32, 32), Image.ANTIALIAS)
        
        # 保存调整大小后的图像
        img_resized.save(resized_map_path)
        print(f"成功: 调整大小后的地图已保存到 {resized_map_path}")
        
except Exception as e:
    print(f"错误: 处理图像时发生异常 -> {e}")
    exit(1)


