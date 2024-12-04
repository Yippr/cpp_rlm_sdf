import numpy as np
from scipy.ndimage import distance_transform_edt

def compute_sdf(binary_map):
    if isinstance(binary_map, list):
        binary_map = np.array(binary_map)
    # 计算内部和外部距离
    dist_outside = distance_transform_edt(1 - binary_map)
    dist_inside = distance_transform_edt(binary_map)
    
    # 将障碍物内部距离设为负值
    sdf = np.where(binary_map, -dist_inside, dist_outside)
    return sdf

# Test code
test_map = [[0,0,0],[0,1,1],[1,1,1]]
result = compute_sdf(test_map)
print("Input array:")
print(np.array(test_map))
print("\nOutput SDF:")
print(result)
