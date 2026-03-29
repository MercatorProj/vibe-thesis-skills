# 数学公式模板

## LaTeX公式规范

### 独立公式格式
```
$$
公式内容 
$$
```

### 行内公式格式
```
$公式内容$
```

## 常用公式模板

### 物理量计算

#### 接地压力
$$
\sigma = \frac{mg}{A} \tag{1}
$$

式中 $\sigma$ 表示目标车辆的单位接地压力,单位为 $\text{kN}/\text{m}^{2}$;$m$ 表示目标车辆的质量,单位为 $\text{kg}$;$g = 9.81\ \text{m}/\text{s}^{2}$ 为重力加速度;$A$ 表示目标车辆轮胎或履带的接地面积,单位为 $\text{m}^{2}$。

#### 沉陷行驶阻力(Bekker模型)
$$
F_{\text{sinking}} = b \left( \frac{k_c}{b} + k_\phi \right) \frac{z^{n+1}}{n+1} \tag{2}
$$

#### 沉陷深度
$$
z = \left[ \beta \cdot \left( \frac{\sigma}{k_c/b + k_\phi} \right) \right]^{1/n} \tag{3}
$$

式中 $b$ 表示目标车辆轮胎或履带的宽度,单位为 $\text{m}$;$k_c$ 为土壤的内聚模数,单位为 $\text{kN}/\text{m}^{n+1}$;$k_\phi$ 为土壤的内摩擦系数,单位为 $\text{kN}/\text{m}^{n+2}$;$n$ 为土壤的变形指数;$\beta$ 为考虑土壤含水率影响的修正系数,其取值范围为 $1.0$–$1.2$。

### 圆锥指数法

#### 车辆圆锥指数
$$
VCI = \frac{RCI}{RCF} \tag{4}
$$

式中 $RCI$ (Rating Cone Index)为额定圆锥指数,$RCF$ (Rating Cone Factor)为额定圆锥因子。

#### 通过性判别
$$
\begin{cases}
CI \geq VCI & \text{可通过} \\
CI < VCI & \text{不可通过}
\end{cases} \tag{5}
$$

### 路径规划算法

#### A*算法代价函数
$$
f(n) = g(n) + h(n) \tag{6}
$$

式中 $f(n)$ 为节点 $n$ 的总估计代价,$g(n)$ 为从起点到节点 $n$ 的实际代价,$h(n)$ 为从节点 $n$ 到终点的启发式估计代价。

#### 曼哈顿距离启发函数
$$
h(n) = |x_n - x_{\text{goal}}| + |y_n - y_{\text{goal}}| \tag{7}
$$

式中 $(x_n, y_n)$ 为节点 $n$ 的坐标,$(x_{\text{goal}}, y_{\text{goal}})$ 为目标点的坐标。

#### 欧几里得距离启发函数
$$
h(n) = \sqrt{(x_n - x_{\text{goal}})^2 + (y_n - y_{\text{goal}})^2} \tag{8}
$$

### 坡度计算

#### 坡度公式
$$
\theta = \arctan\left( \sqrt{\left( \frac{\partial z}{\partial x} \right)^2 + \left( \frac{\partial z}{\partial y} \right)^2} \right) \tag{9}
$$

式中 $\theta$ 为坡度,$\frac{\partial z}{\partial x}$ 和 $\frac{\partial z}{\partial y}$ 分别为 $x$ 和 $y$ 方向的高程梯度。

### VRP模型

#### 目标函数
$$
\min Z = \sum_{k=1}^{K} \sum_{i=0}^{N} \sum_{j=0}^{N} c_{ij} x_{ijk} \tag{10}
$$

式中 $Z$ 为总运输成本,$K$ 为车辆数量,$N$ 为需求点数量,$c_{ij}$ 为从点 $i$ 到点 $j$ 的运输成本,$x_{ijk}$ 为决策变量,当车辆 $k$ 从点 $i$ 行驶到点 $j$ 时为 $1$,否则为 $0$。

#### 容量约束
$$
\sum_{i=0}^{N} d_i y_{ik} \leq Q_k \quad \forall k \tag{11}
$$

式中 $d_i$ 为点 $i$ 的需求量,$y_{ik}$ 为决策变量,当点 $i$ 由车辆 $k$ 服务时为 $1$,否则为 $0$,$Q_k$ 为车辆 $k$ 的容量。

### 数值方法

#### 二分查找法迭代公式
$$
c_k = \frac{a_k + b_k}{2} \tag{12}
$$

式中 $c_k$ 表示第 $k$ 次迭代的中点,$a_k$ 与 $b_k$ 分别为当前迭代步的左、右端点。

#### 牛顿迭代法
$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} \tag{13}
$$

### 性能评估指标

#### 平均绝对误差
$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i| \tag{14}
$$

#### 均方根误差
$$
\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2} \tag{15}
$$

#### 准确率
$$
\text{Accuracy} = \frac{\text{TP} + \text{TN}}{\text{TP} + \text{TN} + \text{FP} + \text{FN}} \tag{16}
$$

## LaTeX符号速查

### 矩阵
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$

代码:
```latex
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
```

### 分段函数
$$
f(x) = \begin{cases}
x^2 & x \geq 0 \\
-x^2 & x < 0
\end{cases}
```

代码:
```latex
f(x) = \begin{cases}
x^2 & x \geq 0 \\
-x^2 & x < 0
\end{cases}
```

### 方程组
$$
\begin{cases}
x + y = 1 \\
x - y = 0
\end{cases}
```

代码:
```latex
\begin{cases}
x + y = 1 \\
x - y = 0
\end{cases}
```

## 单位表示规范

### 物理量单位
- 长度: $\text{m}$ (米), $\text{km}$ (千米)
- 质量: $\text{kg}$ (千克), $\text{t}$ (吨)
- 时间: $\text{s}$ (秒), $\text{h}$ (小时)
- 力: $\text{N}$ (牛顿), $\text{kN}$ (千牛)
- 压力: $\text{Pa}$ (帕斯卡), $\text{kPa}$ (千帕), $\text{MPa}$ (兆帕)
- 速度: $\text{m/s}$ (米/秒), $\text{km/h}$ (千米/小时)
- 角度: $\text{°}$ (度), $\text{rad}$ (弧度)

### 单位格式
- 使用 `\text{}` 命令包裹单位
- 单位与数值之间留空格
- 复合单位使用 `/` 或 `·` 连接
- 示例: $9.81\ \text{m}/\text{s}^{2}$
