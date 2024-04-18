import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

content = torch.load('data/ReferFormer/r50_refytvos_finetune.pth', map_location=device)
print(content.keys())

with open('args_content.txt', 'w') as f:
    f.write(str(content['args']))

print("Content of 'optimizer' has been saved to 'optimizer_content.txt'")

