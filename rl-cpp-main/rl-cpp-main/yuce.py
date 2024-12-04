import json
import gym
import numpy as np
from stable_baselines3 import SAC
from rlm.mower_env import MowerEnv
import os
from datetime import datetime
from PIL import Image
import imageio
# 使用 os.path.join 确保路径正确性
base_path = r"C:\Users\86139\Desktop\Ypr_project\rl_cpp_sdf"
# params_path = os.path.join(base_path, "experiments", "test", "env_parameters.json")
# model_path = os.path.join(base_path, "experiments", "test", "agent.zip")
params_path = os.path.join(base_path, "experiments","szp_v2_0d","env_parameters.json")
model_path = os.path.join(base_path, "experiments","szp_v2_0d", "agent.zip")
test_map_path = os.path.join(base_path, "rl-cpp-main", "rl-cpp-main", "maps", "eval_mowing_5.png")

# 创建保存结果的目录，带有时间戳以避免覆盖
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_dir = os.path.join(base_path, 'results', f'run_{timestamp}')
os.makedirs(results_dir, exist_ok=True)
# Step 1: 加载参数
with open(params_path, 'r') as f:
    env_params = json.load(f)

# Step 2: 设置评估模式参数
env_params['eval'] = True
#env_params['exploration'] = True  # 如果是探索任务需要设置为True
initial_position = [1, 1]  # 固定的初始位置
env = MowerEnv(**env_params, initial_position=initial_position)
# # Step 3: 创建环境
# env = MowerEnv(**env_params)

# Step 4: 设置评估地图
env.eval_maps = [test_map_path]  # 直接设置要评估的地图
# Step 5: 加载训练好的模型
model = SAC.load(model_path)

# Step 6: 评估智能体
episodes = 1
for episode in range(episodes):
    obs = env.reset()
    done = False
    total_reward = 0
    steps = 0
    frames = []  # 用于存储每一帧的图像
    while not done:
        # 获取动作
        action, _ = model.predict(obs, deterministic=True)
        
        # 执行动作
        obs, reward, done, info = env.step(action)
        
       # 渲染环境并获取图像数组
        image_array = env.render(mode='rgb_array')

        # 将图像数组添加到帧列表
        frames.append(image_array)
        
        total_reward += reward
        steps += 1
        
        # 设置最大步数
        if steps > 2000:
            break
        # 保存最后一帧
    # 保存动画为 GIF
    gif_path = os.path.join(results_dir, f'episode_{episode+1}.gif')
    imageio.mimsave(gif_path, frames, fps=30)

    print(f"Episode {episode + 1} finished after {steps} steps with reward {total_reward}")
    print(f"Coverage achieved: {env.coverage_in_percent * 100:.2f}% ")
    print(f"Animation saved to {gif_path}")

# 关闭环境
env.close()