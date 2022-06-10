# asrse3-copy

This is a copy of asrse3 github repo of Dian Wang. Original project website: https://pointw.github.io/asrse3-page/

## Installation

1. Install [anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
1. Clone this repo
   ```
   git clone https://github.com/pointW/asrse3_corl20.git
   cd asrse3_corl20
   ```
1. Create and activate conda environment, install requirement packages
   ```
   conda create --name asrse3 python=3.7
   conda activate asrse3
   pip install -r requirements.txt
   cd ..
   ```
   Note that this project was developed under pybullet version 2.7.1. Newer version of pybullet should also work, but it is not tested.
1. Install [PyTorch](https://pytorch.org/) (Recommended: pytorch==1.7.0, torchvision==0.8.1)
1. Install [CuPy](https://github.com/cupy/cupy)
1. Clone and install the environment repo
   ```
   git clone https://github.com/ColinKohler/helping_hands_rl_envs.git -b dian_corl20
   cd helping_hands_rl_envs
   pip install .
   cd ..
   ```
1. Goto the scripts folder of this repo to run experiments
   ```
   cd asrse3_corl20/scripts
   ```

## 3D (x y theta) Experiments

### Only use "house_building_x" environment

#### Deconstruction Data Collection

```
python fill_buffer_deconstruct.py --num_process=20 --alg=margin_asr --action_sequence=xyrp --buffer_size=50000 --env=house_building_1_deconstruct --num_objects=5 --max_episode_steps=10 --log_sub=h1_deconstruct
```

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
