import argparse

parser = argparse.ArgumentParser(description="PyTorch implementation of Temporal Segment Networks")
parser.add_argument('--class_file', type=str, default="data/classInd_hmdb_ucf.txt")
parser.add_argument('--modality', type=str, default='RGB', choices=['RGB', 'Flow', 'RGBDiff', 'RGBDiff2', 'RGBDiffplus'])
parser.add_argument('--train_source_list', type=str, default='/data1/cwj/dataset/ucf101/list_ucf101_train_hmdb_ucf-feature.txt')
parser.add_argument('--train_target_list', type=str, default='/data1/cwj/dataset/hmdb51/list_hmdb51_train_hmdb_ucf-feature.txt')
parser.add_argument('--val_list', type=str, default='/data1/cwj/dataset/hmdb51/list_hmdb51_val_hmdb_ucf-feature.txt')
parser.add_argument('--temperature', default=1.8, type=float)

# ========================= Model Configs ==========================
parser.add_argument('--arch', type=str, default="resnet101")
parser.add_argument('--pretrained', type=str, default="none")
parser.add_argument('--num_segments', type=int, default=5)
parser.add_argument('--val_segments', type=int, default=5)
parser.add_argument('--add_fc', default=1, type=int, metavar='M', help='number of additional fc layers (excluding the last fc layer) (e.g. 0, 1, 2, ...)')
parser.add_argument('--fc_dim', type=int, default=2048, help='dimension of added fc')
parser.add_argument('--baseline_type', type=str, default='video', choices=['frame', 'video', 'tsn'])
parser.add_argument('--frame_aggregation', type=str, default='trn-m',
                    choices=['avgpool', 'rnn', 'temconv', 'trn', 'trn-m', 'none'], help='aggregation of frame features (none if baseline_type is not video)')
parser.add_argument('--optimizer', type=str, default='SGD', choices=['SGD', 'Adam'])
parser.add_argument('--use_opencv', default=False, action="store_true",
                    help='whether to use the opencv transformation')
parser.add_argument('--dropout_i', '--doi', default=0.5, type=float,
                    metavar='DOI', help='dropout ratio for frame-level feature (default: 0.5)')
parser.add_argument('--dropout_v', '--dov', default=0.5, type=float,
                    metavar='DOV', help='dropout ratio for video-level feature (default: 0.5)')
parser.add_argument('--loss_type', type=str, default="nll",
                    choices=['nll'])
parser.add_argument('--weighted_class_loss', type=str, default='N', choices=['Y', 'N'])

# ------ RNN ------
parser.add_argument('--n_rnn', default=1, type=int, metavar='M', help='number of RNN layers (e.g. 0, 1, 2, ...)')
parser.add_argument('--rnn_cell', type=str, default='LSTM', choices=['LSTM', 'GRU'])
parser.add_argument('--n_directions', type=int, default=1, choices=[1, 2], help='(bi-) direction RNN')
parser.add_argument('--n_ts', type=int, default=5, help='number of temporal segments')

# ========================= DA Configs ==========================
parser.add_argument('--share_params', type=str, default='Y', choices=['Y', 'N'])
parser.add_argument('--use_target', type=str, default='uSv', choices=['none', 'Sv', 'uSv'],
                    help='the method to use target data (not use | supervised | unsupervised)')
parser.add_argument('--dis_DA', type=str, default='none', choices=['none', 'DAN', 'JAN', 'CORAL'], help='discrepancy method for DA')
parser.add_argument('--adv_DA', type=str, default='RevGrad', choices=['none', 'RevGrad'], help='adversarial method for DA')
parser.add_argument('--use_bn', type=str, default='none', choices=['none', 'AdaBN', 'AutoDIAL'], help='normalization-based methods')
parser.add_argument('--ens_DA', type=str, default='none', choices=['none', 'MCD'], help='ensembling-based methods')
parser.add_argument('--use_attn_frame', type=str, default='none', choices=['none', 'TransAttn', 'general', 'DotProduct'], help='attention-mechanism for frames only')
parser.add_argument('--use_attn', type=str, default='none', choices=['none', 'TransAttn', 'general', 'DotProduct'], help='attention-mechanism')  # 在使用fada后，无法计算(8)式，故将参数设为'none'
parser.add_argument('--n_attn', type=int, default=1, help='number of discriminators for transferable attention')
parser.add_argument('--add_loss_DA', type=str, default='attentive_entropy', choices=['none', 'target_entropy', 'attentive_entropy'],
                    help='add more loss functions for DA')
parser.add_argument('--pred_normalize', type=str, default='N', choices=['Y', 'N'])
parser.add_argument('--alpha', default=0, type=float, metavar='M', help='weighting for the discrepancy loss (use scheduler if < 0)')
parser.add_argument('--beta', default=[0.75, 0.75, 0.5], type=float, nargs="+", metavar='M',
                    help='weighting for the adversarial loss (use scheduler if < 0; [relation-beta, video-beta, frame-beta])')
parser.add_argument('--gamma', default=0.003, type=float, metavar='M', help='weighting for the entropy loss')
parser.add_argument('--mu', default=0, type=float, metavar='M', help='weighting for ensembling loss (e.g. discrepancy)')
parser.add_argument('--weighted_class_loss_DA', type=str, default='N', choices=['Y', 'N'])
parser.add_argument('--place_dis', default=['N', 'Y', 'N'], type=str, nargs="+",
                    metavar='N', help='where to place the discrepancy loss (length = add_fc + 2)')
parser.add_argument('--place_adv', default=['Y', 'Y', 'Y'], type=str, nargs="+",
                    metavar='N', help='[video relation-based adv, video-based adv, frame-based adv]')

# ========================= Learning Configs ==========================
parser.add_argument('--pretrain_source', default=False, action="store_true", help='perform source-only training before DA')
parser.add_argument('--epochs', default=30, type=int, metavar='N',
                    help='number of total epochs to run')
parser.add_argument('-b', '--batch_size', default=[128, 74, 128], type=int, nargs="+",
                    metavar='N', help='mini-batch size ([source, target, testing])')
parser.add_argument('--lr', '--learning_rate', default=3e-2, type=float,
                    metavar='LR', help='initial learning rate')
parser.add_argument('--lr_decay', default=10, type=float, metavar='LRDecay', help='decay factor for learning rate')
parser.add_argument('--lr_adaptive', type=str, default='dann', choices=['none', 'loss', 'dann'])
parser.add_argument('--lr_steps', default=[150, 150], type=float, nargs="+",
                    metavar='LRSteps', help='epochs to decay learning rate')
parser.add_argument('--momentum', default=0.9, type=float, metavar='M',
                    help='momentum')
parser.add_argument('--weight_decay', '--wd', default=1e-4, type=float,
                    metavar='W', help='weight decay (default: 1e-4)')
parser.add_argument('--clip_gradient', '--gd', default=20, type=float,
                    metavar='W', help='gradient norm clipping (default: disabled)')
parser.add_argument('--no_partialbn', '--npb', default=True, action="store_true")
parser.add_argument('--copy_list', default=['N', 'N'], type=str, nargs="+",
                    metavar='N', help='duplicate data in case the dataset is relatively small ([copy source list, copy target list])')

# ========================= Monitor Configs ==========================
parser.add_argument('--print_freq', '-pf', default=50, type=int,
                    metavar='N', help='frequency for printing to text files (default: 10)')
parser.add_argument('--show_freq', '-sf', default=50, type=int,
                    metavar='N', help='frequency for showing on the screen (default: 10)')
parser.add_argument('--eval_freq', '-ef', default=1, type=int,
                    metavar='N', help='evaluation frequency (default: 5)')
parser.add_argument('--verbose', default=False, action="store_true")

# ========================= Runtime Configs ==========================
parser.add_argument('-j', '--workers', default=4, type=int, metavar='N',
                    help='number of data loading workers (default: 4)')
parser.add_argument('--resume', default='', type=str, metavar='PATH',
                    help='path to latest checkpoint (default: none)')
parser.add_argument('--resume_hp', default=False, action="store_true",
                    help='whether to use the saved hyper-parameters')
parser.add_argument('-e', '--evaluate', dest='evaluate', action='store_true',
                    help='evaluate model on validation set')
parser.add_argument('--exp_path', type=str, default="action-experiments/",
                    help='full path of the experiment folder')
parser.add_argument('--gpus', nargs='+', type=int, default=None)
parser.add_argument('--flow_prefix', default="", type=str)
parser.add_argument('--save_model', default=True, action="store_true")
parser.add_argument('--save_best_log', default="best.log", type=str)
parser.add_argument('--save_attention', type=int, default=-1)
parser.add_argument('--tensorboard', dest='tensorboard', action='store_true')
