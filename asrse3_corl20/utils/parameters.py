import numpy as np
import torch
import argparse
import os
from utils.stacking_grammar import count_objects, decompose_objects


def strToBool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')


parser = argparse.ArgumentParser()
env_group = parser.add_argument_group('environment')
env_group.add_argument('--env', type=str, default='block_stacking', help='block_picking, block_stacking, brick_stacking, '
                                                                         'brick_inserting, block_cylinder_stacking')
env_group.add_argument('--reward_type', type=str, default='sparse')
env_group.add_argument('--simulator', type=str, default='pybullet')
env_group.add_argument('--robot', type=str, default='kuka')
env_group.add_argument('--num_objects', type=int, default=3)
env_group.add_argument('--max_episode_steps', type=int, default=10)
env_group.add_argument('--fast_mode', type=strToBool, default=True)
env_group.add_argument('--simulate_grasp', type=strToBool, default=True)
env_group.add_argument('--action_sequence', type=str, default='xyrp')
env_group.add_argument('--random_orientation', type=strToBool, default=True)
env_group.add_argument('--num_processes', type=int, default=5)
env_group.add_argument('--render', type=strToBool, default=False)
env_group.add_argument('--workspace_size', type=float, default=0.3)
env_group.add_argument('--heightmap_size', type=int, default=90)
env_group.add_argument('--perfect_grasp', action='store_true')
env_group.add_argument('--perfect_place', action='store_true')
env_group.add_argument('--in_hand_mode', type=str,
                       default='raw', choices=['raw', 'proj'])
env_group.add_argument('--goal', type=str, default='1b1r')

training_group = parser.add_argument_group('training')
training_group.add_argument('--alg', default='dqn')
training_group.add_argument('--model', type=str, default='resucat')
training_group.add_argument('--num_rotations', type=int, default=8)
training_group.add_argument('--half_rotation', type=strToBool, default=True)
training_group.add_argument('--lr', type=float, default=5e-5)
training_group.add_argument('--gamma', type=float, default=0.9)
training_group.add_argument('--explore', type=int, default=10000)
training_group.add_argument('--fixed_eps', action='store_true')
training_group.add_argument('--init_eps', type=float, default=1.0)
training_group.add_argument('--final_eps', type=float, default=0.)
training_group.add_argument('--training_iters', type=int, default=1)
training_group.add_argument('--training_offset', type=int, default=1000)
training_group.add_argument('--max_episode', type=int, default=50000)
training_group.add_argument('--device_name', type=str, default='cuda')
training_group.add_argument('--target_update_freq', type=int, default=100)
training_group.add_argument('--save_freq', type=int, default=500)
training_group.add_argument('--action_selection', type=str, default='egreedy')
training_group.add_argument('--load_model_pre', type=str, default=None)
training_group.add_argument('--sl', action='store_true')
training_group.add_argument('--planner_episode', type=int, default=0)
training_group.add_argument('--note', type=str, default=None)
training_group.add_argument('--seed', type=int, default=None)
training_group.add_argument('--perlin', type=float, default=0.0)
training_group.add_argument('--fill_buffer', action='store_true')
training_group.add_argument('--fill_buffer_deconstruct', action='store_true')
training_group.add_argument('--load_buffer', type=str, default=None)
training_group.add_argument('--load_n', type=int, default=1000000)
training_group.add_argument('--pre_train_step', type=int, default=0)
training_group.add_argument('--num_zs', type=int, default=16)
training_group.add_argument('--min_z', type=float, default=0.02)
training_group.add_argument('--max_z', type=float, default=0.12)
training_group.add_argument('--ddpg_tau', type=float, default=0.01)
training_group.add_argument('--ddpg_bc', type=strToBool, default=True)
training_group.add_argument(
    '--ddpg_bc_q_filter', type=strToBool, default=False)
training_group.add_argument('--critic_fc', type=str, default='1024*3')
training_group.add_argument('--q3_input', type=str,
                            default='proj', choices=['crop', 'proj'])
training_group.add_argument('--patch_div', type=float, default=1.0)
training_group.add_argument('--patch_mul', type=float, default=1.0)
training_group.add_argument('--q2_model', type=str, default='cnn')

planner_group = parser.add_argument_group('planner')
planner_group.add_argument('--planner_pos_noise', type=float, default=0)
planner_group.add_argument('--planner_rot_noise', type=float, default=0)

margin_group = parser.add_argument_group('margin')
margin_group.add_argument('--margin', default='l',
                          choices=['ce', 'bce', 'bcel', 'l', 'oril'])
margin_group.add_argument('--margin_l', type=float, default=0.1)
margin_group.add_argument('--margin_weight', type=float, default=0.1)
margin_group.add_argument('--margin_beta', type=float, default=100)

buffer_group = parser.add_argument_group('buffer')
buffer_group.add_argument('--buffer', default='normal',
                          choices=['normal', 'per', 'expert', 'per_expert'])
buffer_group.add_argument('--per_eps', type=float,
                          default=1e-6, help='Epsilon parameter for PER')
buffer_group.add_argument('--per_alpha', type=float,
                          default=0.6, help='Alpha parameter for PER')
buffer_group.add_argument('--per_beta', type=float,
                          default=0.4, help='Initial beta parameter for PER')
buffer_group.add_argument('--per_expert_eps', type=float, default=0.1)
buffer_group.add_argument('--batch_size', type=int, default=32)
buffer_group.add_argument('--buffer_size', type=int, default=100000)

logging_group = parser.add_argument_group('logging')
logging_group.add_argument('--log_pre', type=str, default='outputs')
logging_group.add_argument('--log_sub', type=str, default=None)
logging_group.add_argument('--no_bar', action='store_true')
logging_group.add_argument('--time_limit', type=float, default=10000)
logging_group.add_argument('--load_sub', type=str, default=None)

test_group = parser.add_argument_group('test')
test_group.add_argument('--test', action='store_true')

args = parser.parse_args()
# env
random_orientation = args.random_orientation
reward_type = args.reward_type
env = args.env
simulator = args.simulator
max_episode_steps = args.max_episode_steps
fast_mode = args.fast_mode
simulate_grasp = args.simulate_grasp
action_sequence = args.action_sequence
num_processes = args.num_processes
render = args.render
perfect_grasp = args.perfect_grasp
perfect_place = args.perfect_place
scale = 1.
robot = args.robot
goal_string = args.goal
if "house_building_x" in env:
    num_objects = count_objects(goal_string)
else:
    num_objects = args.num_objects

workspace_size = args.workspace_size
workspace = np.asarray([[0.5-workspace_size/2, 0.5+workspace_size/2],
                        [0-workspace_size/2, 0+workspace_size/2],
                        [0, 0+workspace_size]])
heightmap_size = args.heightmap_size

if env in ['block_picking', 'random_picking', 'random_float_picking', 'cube_float_picking', 'drawer_opening']:
    num_primitives = 1
else:
    num_primitives = 2

heightmap_resolution = workspace_size/heightmap_size
action_space = [0, heightmap_size]

num_rotations = args.num_rotations
half_rotation = args.half_rotation
if half_rotation:
    rotations = [np.pi / num_rotations * i for i in range(num_rotations)]
else:
    rotations = [(2 * np.pi) / num_rotations * i for i in range(num_rotations)]
in_hand_mode = args.in_hand_mode

######################################################################################
# training
alg = args.alg
if alg == 'dqn_sl_anneal':
    args.sl = True
model = args.model
lr = args.lr
gamma = args.gamma
explore = args.explore
fixed_eps = args.fixed_eps
init_eps = args.init_eps
final_eps = args.final_eps
training_iters = args.training_iters
training_offset = args.training_offset
max_episode = args.max_episode
device = torch.device(args.device_name)
target_update_freq = args.target_update_freq
patch_size = 24
save_freq = args.save_freq
action_selection = args.action_selection
sl = args.sl
planner_episode = args.planner_episode

ddpg_tau = args.ddpg_tau
ddpg_bc = args.ddpg_bc
ddpg_bc_q_filter = args.ddpg_bc_q_filter
critic_fc = args.critic_fc

load_model_pre = args.load_model_pre
is_test = args.test
note = args.note
seed = args.seed
perlin = args.perlin

q3_input = args.q3_input

patch_div = args.patch_div
patch_mul = args.patch_mul

q2_model = args.q2_model

# pre train
fill_buffer = args.fill_buffer
fill_buffer_deconstruct = args.fill_buffer_deconstruct
load_buffer = args.load_buffer
load_n = args.load_n
pre_train_step = args.pre_train_step

# planner
planner_pos_noise = args.planner_pos_noise
planner_rot_noise = args.planner_rot_noise

# buffer
buffer_type = args.buffer
per_eps = args.per_eps
per_alpha = args.per_alpha
per_beta = args.per_beta
per_expert_eps = args.per_expert_eps
batch_size = args.batch_size
buffer_size = args.buffer_size

# margin
margin = args.margin
margin_l = args.margin_l
margin_weight = args.margin_weight
margin_beta = args.margin_beta

# logging
log_pre = args.log_pre
log_sub = args.log_sub
no_bar = args.no_bar
time_limit = args.time_limit
load_sub = args.load_sub
if load_sub == 'None':
    load_sub = None

# z
num_zs = args.num_zs
min_z = args.min_z
max_z = args.max_z

######################################################################################
env_config = {'workspace': workspace, 'max_steps': max_episode_steps, 'obs_size': heightmap_size,
              'fast_mode': fast_mode,  'action_sequence': action_sequence, 'render': render, 'num_objects': num_objects,
              'random_orientation': random_orientation, 'reward_type': reward_type, 'simulate_grasp': simulate_grasp,
              'perfect_grasp': perfect_grasp, 'perfect_place': perfect_place, 'scale': scale, 'robot': robot,
              'workspace_check': 'point', 'in_hand_mode': in_hand_mode, 'object_scale_range': (0.6, 0.6),
              'hard_reset_freq': 1000, 'physics_mode': 'fast', 'goal_string': goal_string}
if "house_building_x" in env:
    num_blocks, num_bricks, num_triangles, num_roofs = decompose_objects(goal_string)
    env_config['gen_blocks'] = num_blocks
    env_config['gen_bricks'] = num_bricks
    env_config['gen_triangles'] = num_triangles
    env_config['gen_roofs'] = num_roofs
    if log_sub is not None:
      log_sub = os.path.join(log_sub, goal_string)
    elif alg != 'dqn_fcn':
      load_buffer = os.path.join(log_pre, '{}_deconstruct'.format(alg), 'hx_deconstruct', goal_string, 'checkpoint/buffer.pt')

planner_config = {'pos_noise': planner_pos_noise,
                  'rot_noise': planner_rot_noise, 'random_orientation': random_orientation, }
if seed is not None:
    env_config['seed'] = seed
######################################################################################
hyper_parameters = {}
for key in sorted(vars(args)):
    hyper_parameters[key] = vars(args)[key]

for key in hyper_parameters:
    print('{}: {}'.format(key, hyper_parameters[key]))
