import torch

# 加载 checkpoint 文件
checkpoint = torch.load('/Users/shuaicongwu/Downloads/checkpoint.pth', map_location=torch.device('cpu'))

# 打印 checkpoint 的键
print("Keys in checkpoint:", checkpoint.keys())

if 'args' in checkpoint:
    print("args found in checkpoint:", checkpoint['args'])
else:
    print("No 'args' key found in checkpoint.")

# 如果是模型的 state_dict，查看具体层级
if 'state_dict' in checkpoint:
    state_dict = checkpoint['state_dict']
    print("\nLayers in state_dict:")
    for layer_name in state_dict:
        print(layer_name)
else:
    print("\nNo 'state_dict' found, displaying keys directly:")
    for key in checkpoint:
        print(key)
