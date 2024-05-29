import matplotlib.pyplot as plt
import os

file_dir_ytvos = "data/ReferFormer/train_results_on_Ref-YT-VOS/log.txt"
with open(file_dir_ytvos, "r") as file_ytvos:
    lines_ytvos = file_ytvos.readlines()

file_dir_mot17 = "data/ReferFormer/train_results_on_MOT17/log.txt"
with open(file_dir_mot17, "r") as file_mot17:
    lines_mot17 = file_mot17.readlines()

# initial the parameters dict
params = {
    "train_lr": [],
    "train_loss": [],
    "train_loss_bbox": [],
    "train_loss_bbox_0": [],
    "train_loss_bbox_1": [],
    "train_loss_bbox_2": [],
    "train_loss_ce": [],
    "train_loss_ce_0": [],
    "train_loss_ce_1": [],
    "train_loss_ce_2": [],
    "train_loss_dice": [],
    "train_loss_dice_0": [],
    "train_loss_dice_1": [],
    "train_loss_dice_2": [],
    "train_loss_giou": [],
    "train_loss_giou_0": [],
    "train_loss_giou_1": [],
    "train_loss_giou_2": [],
    "train_loss_mask": [],
    "train_loss_mask_0": [],
    "train_loss_mask_1": [],
    "train_loss_mask_2": [],
    "train_loss_bbox_unscaled": [],
    "train_loss_bbox_0_unscaled": [],
    "train_loss_bbox_1_unscaled": [],
    "train_loss_bbox_2_unscaled": [],
    "train_loss_ce_unscaled": [],
    "train_loss_ce_0_unscaled": [],
    "train_loss_ce_1_unscaled": [],
    "train_loss_ce_2_unscaled": [],
    "train_loss_dice_unscaled": [],
    "train_loss_dice_0_unscaled": [],
    "train_loss_dice_1_unscaled": [],
    "train_loss_dice_2_unscaled": [],
    "train_loss_giou_unscaled": [],
    "train_loss_giou_0_unscaled": [],
    "train_loss_giou_1_unscaled": [],
    "train_loss_giou_2_unscaled": [],
    "train_loss_mask_unscaled": [],
    "train_loss_mask_0_unscaled": [],
    "train_loss_mask_1_unscaled": [],
    "train_loss_mask_2_unscaled": [],
    "train_grad_norm": [],
    "epoch": [],
    "n_parameters": []
}

params_ytvos = {}
params_mot17 = {}

for line in lines_ytvos:
    data = eval(line)  # transfer string to dict
    for param, value in data.items():
        if param not in params_ytvos:
            params_ytvos[param] = []
        params_ytvos[param].append(value)

for line in lines_mot17:
    data = eval(line)
    for param, value in data.items():
        if param not in params_mot17:
            params_mot17[param] = []
        params_mot17[param].append(value)

output_dir = "data/generated_by_code/plot_referformer_training/"

# For creating plots for one txt file
# for param, values in params.items():
#     fig, ax = plt.subplots(figsize=(12, 10))
#     ax.plot(range(0, len(values)), values, label=param)
#     ax.set_title(param)
#     ax.set_xlabel("Epoch")
#     ax.set_ylabel("Parameter Value")
#     ax.legend()
#
#     for i in range(len(values)):
#         ax.annotate(f'{values[i]:.6f}'.rstrip('0').rstrip('.'), (i, values[i]), textcoords="offset points", xytext=(0,10), ha='center')
#
#     plt.savefig(os.path.join(output_dir, f"{param}_plot.png"))
#     plt.close()

for param in set(params_ytvos.keys()) | set(params_mot17.keys()):
    if param in params_ytvos and param in params_mot17:
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.plot(range(0, len(params_ytvos[param])), params_ytvos[param], label=file_dir_ytvos.split('.')[0])
        ax.plot(range(0, len(params_mot17[param])), params_mot17[param], label=file_dir_mot17.split('.')[0])
        ax.set_title(param)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Parameter Value")
        ax.legend()

        for i, value in enumerate(params_ytvos[param]):
            ax.annotate(f'{value:.6f}'.rstrip('0').rstrip('.'), (i, value), textcoords="offset points", xytext=(0, -10), ha='center')
        for i, value in enumerate(params_mot17[param]):
            ax.annotate(f'{value:.6f}'.rstrip('0').rstrip('.'), (i, value), textcoords="offset points", xytext=(0, 10), ha='center')

        plt.savefig(os.path.join(output_dir, f"{param}_plot.png"))
        plt.close()
