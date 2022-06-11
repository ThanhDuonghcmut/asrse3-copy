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

```
python fill_buffer_deconstruct.py --num_process=20 --alg=margin_asr --action_sequence=xyrp --buffer_size=50000 --env=house_building_x_deconstruct --max_episode_steps=10 --log_sub=hx_deconstruct --goal=1b1r
```

Parameter explanation:

- num_process: Number of process to run parallel
- alg: type of algorithm to choose:

* alg=margin_asr: ASRSE3 algorithm
* alg=dqn_fcn: Normal DQN
* alg=margin_fcn, margin=oril: DQfD

- action_sequence: type of action sequence that is using
- buffer_size: the max size of the buffer, or the amount of data to collect
- env: the environment we want to run, here we choose the "house_building_x_deconstruct"
- log_sub: the folder contains all the data folders collected. It is the sub folder of /scripts/output/{alg}\_deconstruct/
- goal: the goal we want to achieve

Data of each goal will be stored in a seperate folder, sub folder of log_sub , the name of the folder is the goal.

### Training

#### Example: training 5H1 using ASRSE3 SDQfD

```
python main.py --num_process=5 --alg=margin_asr --action_sequence=xyrp --planner_episode=0 --explore=0 --fixed_eps --buffer=expert --max_episode=50000 --pre_train_step=10000 --env=house_building_1 --num_objects=5 --max_episode_steps=10 --load_buffer=outputs/margin_asr_deconstruct/h1_deconstruct/checkpoint/buffer.pt
```

#### Other envs:

Replace the following parameters for `main.py`:
`--env=house_building_1 --num_objects=5 --max_episode_steps=10 --load_buffer=outputs/margin_asr_deconstruct/h1_deconstruct/checkpoint/buffer.pt`
with:

- H4: `--env=house_building_4 --num_objects=6 --max_episode_steps=20 --load_buffer=outputs/margin_asr_deconstruct/h4_deconstruct/checkpoint/buffer.pt`
- ImDis: `--env=improvise_house_building_discrete --num_objects=5 --max_episode_steps=10 --load_buffer=outputs/margin_asr_deconstruct/imdis_deconstruct/checkpoint/buffer.pt`
- ImRan: `--env=improvise_house_building_random --num_objects=5 --max_episode_steps=10 --load_buffer=outputs/margin_asr_deconstruct/imran_deconstruct/checkpoint/buffer.pt`

#### Other algorithms

Replace `--alg=margin_asr` in `main.py` with:

- ASRSE3 DQfD: `--alg=margin_asr --margin=oril`
- ASRSE3 ADET: `--alg=margin_asr --margin=ce`
- ASRSE3 DQN: `--alg=dqn_asr`
- FCN SDQfD: `--alg=margin_fcn`
- FCN DQfD: `--alg=margin_fcn --margin=oril`
- FCN ADET: `--alg=margin_fcn --margin=ce --margin_weight=0.01`
- FCN DQN: `--alg=dqn_fcn`

## Results

The training results will be saved under `scripts/outputs`

## Citation

```
@article{wang2020policy,
  title={Policy learning in SE (3) action spaces},
  author={Wang, Dian and Kohler, Colin and Platt, Robert},
  journal={arXiv preprint arXiv:2010.02798},
  year={2020}
}
```
