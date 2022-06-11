# asrse3-copy

This is a copy of asrse3 github repo of Dian Wang. Original project website: https://pointw.github.io/asrse3-page/

## Installation

1. Clone this repo
   ```
   git clone https://github.com/ThanhDuonghcmut/asrse3-copy.git
   cd asrse3_corl20
   ```
1. Install requirement packages
   ```
   pip install -r requirements.txt
   cd ..
   ```
1. Install [PyTorch](https://pytorch.org/) (Recommended: pytorch==1.7.0, torchvision==0.8.1)
1. Install [CuPy](https://github.com/cupy/cupy)
1. Install the helping hands environment:
   ```
   cd helping_hands_rl_envs
   pip install .
   cd ..
   ```
1. Goto the scripts folder of this repo to run experiments
   ```
   cd asrse3_corl20/scripts
   ```

## 3D (x y theta) Experiments --- Only use "house_building_x" environment

### Deconstruction Data Collection

Because the house_building_x_need to specify the goal, so for every goal we will collect into a folder.

#### Example training goal=1l1b1r with algorithm ASRSE3

```
python fill_buffer_deconstruct.py --num_process=20 --alg=margin_asr --action_sequence=xyrp --buffer_size=50000 --env=house_building_x_deconstruct --max_episode_steps=10 --log_sub=hx_deconstruct --goal=1l1b1r
```

#### Running instruction:

- For different goals, we replace `--goal=1l1b1r` with the goal we want.
- For different algorithms, we replace `--alg=margin_asr` with the algorithm we want below

#### Parameter explanation:

- `num_process`: Number of process to run parallel
- `alg`: type of algorithm to choose:

  - `--alg=margin_asr`: ASRSE3 SDQfD algorithm
  - `--alg=dqn_fcn`: Normal DQN
  - `--alg=margin_fcn --margin=oril`: DQfD

- `action_sequence`: type of action sequence that is using
- `buffer_size`: the max size of the buffer, or the amount of data to collect
- `env`: the environment we want to run, here we choose the `house_building_x_deconstruct`
- `log_sub`: the folder contains all the data folders collected. It is the sub folder of `/scripts/output/{alg}_deconstruct/`
- `goal`: the goal we want to achieve

Data of each goal will be stored in a seperate folder, sub folder of `log_sub` , the name of the folder is the goal.

**The data of each goal must be collect one time. If you want to collect data of that goal again, you have to delete the data folder in the `log_sub` folder first.**

### Training

#### Example: training goal=1l1b1r using ASRSE3 SDQfD

```
python main.py --num_process=5 --alg=margin_asr --action_sequence=xyrp --explore=0 --fixed_eps --buffer=expert --max_episode=50000 --pre_train_step=10000 --env=house_building_x --max_episode_steps=10 --goal=1l1b1r
```

#### Running instruction:

- For different goals, we replace `--goal=1l1b1r` with the goal we want.
- For different algorithms, we replace `--alg=margin_asr` with the algorithm we want below

#### Parameter explanation:

- `num_process`: Number of process to run parallel
- `alg`: type of algorithm to choose:

  - `--alg=margin_asr`: ASRSE3 SDQfD algorithm
  - `--alg=dqn_fcn`: Normal DQN
  - `--alg=margin_fcn --margin=oril`: DQfD

- `action_sequence`: type of action sequence that is using
- `explore` and `fix_eps`: these parameters are used for exploration
- `buffer`: type of buffer using, we have 2 types: `expert` and `normal`
- `max_episode`: the number of episodes for trainging process
- `pre_train_step`: the number of step for pretraining. When using `--alg=dqn_fcn`, we don't need this parameter
- `env`: the environment we want to run, here we choose the `house_building_x`
- `goal`: the goal we want to achieve

## Results

The training results will be saved under `scripts/outputs/{alg}/`

## Citation

```
@article{wang2020policy,
  title={Policy learning in SE (3) action spaces},
  author={Wang, Dian and Kohler, Colin and Platt, Robert},
  journal={arXiv preprint arXiv:2010.02798},
  year={2020}
}
```
