## `make_grid` 的 `normalize=True` 对单张图不生效

我在用 jittor 训一个生成模型，每隔若干步把当前生成出来的图存盘看一下效果。生成出来的张量数值范围不是 [0, 1]（大致在 [-1, 1] 左右），所以我用 `make_grid` / `save_image` 时传了 `normalize=True`，希望它在保存前把数值缩放到 [0, 1]。

batch 内有多张图时一切正常，存出来的拼图颜色看上去是对的。

但是当我只想看单张图的时候（比如只生成一个样本，或者 debug 阶段只 forward 一张），保存出来的图整张要么全黑要么全白，完全没有被归一化。我换了几种 shape 试了一下：

```python
import jittor as jt
from jittor.misc import make_grid

# 一个 batch=1 的图像，数值范围不在 [0,1]
x = jt.randn(1, 3, 64, 64) * 5.0

out = make_grid(x, normalize=True)
print(out.min(), out.max())   # 我期望接近 0 和 1，但实际还是原始范围
```

而把 batch 改成 ≥2 之后，`out` 的数值范围就被正常归一到 [0, 1] 了。所以 `normalize=True` 这个参数在单图场景下相当于没生效，结果跟我不传 `normalize` 一样。

希望 `normalize=True` 不论输入是单张还是多张都能生效。
