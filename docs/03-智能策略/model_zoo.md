# Model Zoo

## Common settings

- We use distributed training.
- For fair comparison with other codebases, we report the GPU memory as the maximum value of `torch.cuda.max_memory_allocated()` for all 8 GPUs. Note that this value is usually less than what `nvidia-smi` shows.
- We report the inference time as the total time of network forwarding and post-processing, excluding the data loading time. Results are obtained with the script [benchmark.py](https://github.com/open-mmlab/mmdetection/blob/master/tools/analysis_tools/benchmark.py) which computes the average time on 2000 images.

## Baselines

### SECOND

Please refer to [SECOND](https://github.com/open-mmlab/mmdetection3d/blob/master/configs/second) for details. We provide SECOND baselines on jifinance datasets.