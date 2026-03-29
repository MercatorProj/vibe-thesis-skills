# Formula Rules

本文档提供详细的公式格式规范和LaTeX语法规则，用于指导数学公式的标准化处理。

## Markdown公式格式规范

### 独立显示公式

#### 标准格式

**要求**: 所有独立显示的数学公式（单独成行、居中显示）必须使用双美元符包裹

**格式**:
```markdown
$$
[公式内容]
$$
```

**示例**:
```markdown
牛顿迭代法的迭代公式为：

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$
```

#### 禁止格式

以下格式**禁止**使用，必须转换为标准格式：

1. **LaTeX display math**
   ```markdown
   \[
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   \]
   ```
   **转换为**:
   ```markdown
   $$
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   $$
   ```

2. **无空格的双美元符**
   ```markdown
   $$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$$
   ```
   **转换为**:
   ```markdown
   $$
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   $$
   ```

3. **LaTeX equation环境**
   ```markdown
   \begin{equation}
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   \end{equation}
   ```
   **转换为**:
   ```markdown
   $$
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   $$
   ```

4. **其他非标准LaTeX环境**
   ```markdown
   \begin{align}
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   \end{align}
   ```
   **转换为**:
   ```markdown
   $$
   x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
   $$
   ```

#### 空行要求

**要求**: 独立显示公式前后必须有适当的空行

**正确示例**:
```markdown
牛顿迭代法的迭代公式为：

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$

其中：$x_k$ 为第 $k$ 次迭代的近似解。
```

**错误示例**:
```markdown
牛顿迭代法的迭代公式为：
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$
其中：$x_k$ 为第 $k$ 次迭代的近似解。
```

### 行内公式

#### 标准格式

**要求**: 所有行内数学公式（嵌入在段落文字中）必须使用单美元符包裹

**格式**:
```markdown
$[公式内容]$
```

**示例**:
```markdown
函数 $f(x)$ 在区间 $[a, b]$ 上连续。
当 $|x_{k+1} - x_k| < \varepsilon$ 时，算法收敛。
```

#### 注意事项

- 行内公式**不能**使用双美元符
- 行内公式前后**不需要**空行
- 行内公式应与文字保持适当间距

**正确示例**:
```markdown
对于任意 $x \in \mathbb{R}$，有 $f(x) \geq 0$。
```

**错误示例**:
```markdown
对于任意 $$x \in \mathbb{R}$$，有 $$f(x) \geq 0$$。
```

## LaTeX语法规则

### 上下标

#### 上标

**规则**: 使用 `^` 符号，多字符上标必须用花括号包裹

**示例**:
- 单字符上标: `x^2` → $x^2$
- 多字符上标: `x^{2n}` → $x^{2n}$
- 复杂上标: `e^{-x^2}` → $e^{-x^2}$

**常见错误**:
- `x^2n` → 错误（显示为 $x^2n$）
- `x^{2n}` → 正确（显示为 $x^{2n}$）

#### 下标

**规则**: 使用 `_` 符号，多字符下标必须用花括号包裹

**示例**:
- 单字符下标: `x_i` → $x_i$
- 多字符下标: `x_{max}` → $x_{max}$
- 复杂下标: `a_{i,j}` → $a_{i,j}$

**常见错误**:
- `x_max` → 错误（显示为 $x_max$）
- `x_{max}` → 正确（显示为 $x_{max}$）

#### 上下标组合

**规则**: 上标和下标可以组合使用

**示例**:
- `x_i^2` → $x_i^2$
- `x_{i,j}^{(n)}` → $x_{i,j}^{(n)}$

### 分数

#### 标准分数

**规则**: 使用 `\frac{分子}{分母}` 格式

**示例**:
```markdown
$$
\frac{a}{b}
$$
```

**显示**: $\frac{a}{b}$

#### 嵌套分数

**规则**: 可以嵌套使用 `\frac`

**示例**:
```markdown
$$
\frac{\frac{a}{b}}{c}
$$
```

**显示**: $\frac{\frac{a}{b}}{c}$

#### 简化写法

**在简洁化风格中**，可以使用斜杠表示分数：

```markdown
$$
a/b
$$
```

**显示**: $a/b$

### 希腊字母

#### 常用希腊字母

| LaTeX | 显示 | LaTeX | 显示 |
|-------|------|-------|------|
| `\alpha` | $\alpha$ | `\beta` | $\beta$ |
| `\gamma` | $\gamma$ | `\delta` | $\delta$ |
| `\epsilon` | $\epsilon$ | `\theta` | $\theta$ |
| `\lambda` | $\lambda$ | `\mu` | $\mu$ |
| `\pi` | $\pi$ | `\sigma` | $\sigma$ |
| `\phi` | $\phi$ | `\omega` | $\omega$ |
| `\Gamma` | $\Gamma$ | `\Delta` | $\Delta$ |
| `\Theta` | $\Theta$ | `\Lambda` | $\Lambda$ |
| `\Pi` | $\Pi$ | `\Sigma` | $\Sigma$ |

#### 使用规则

- **必须使用LaTeX命令**，不能直接输入希腊字母
- 大小写敏感：`\alpha` vs `\Alpha`
- 在专业化风格中，所有希腊字母必须使用LaTeX命令

**正确示例**:
```markdown
$$
\alpha + \beta = \gamma
$$
```

**错误示例**:
```markdown
$$
α + β = γ
$$
```

### 运算符

#### 常用运算符

| LaTeX | 显示 | LaTeX | 显示 |
|-------|------|-------|------|
| `\times` | $\times$ | `\div` | $\div$ |
| `\pm` | $\pm$ | `\mp` | $\mp$ |
| `\cdot` | $\cdot$ | `\ast` | $\ast$ |
| `\leq` | $\leq$ | `\geq` | $\geq$ |
| `\neq` | $\neq$ | `\approx` | $\approx$ |
| `\equiv` | $\equiv$ | `\sim` | $\sim$ |
| `\sum` | $\sum$ | `\prod` | $\prod$ |
| `\int` | $\int$ | `\oint` | $\oint$ |

#### 使用规则

- 在专业化风格中，必须使用LaTeX运算符命令
- 在简洁化风格中，可以使用简化符号（如 `*` 代替 `\times`）

**专业化示例**:
```markdown
$$
a \times b = c
$$
```

**简洁化示例**:
```markdown
$$
a * b = c
$$
```

### 括号

#### 自动调整大小的括号

**规则**: 使用 `\left(` 和 `\right)` 等命令自动调整括号大小

**示例**:
```markdown
$$
\left( \frac{a}{b} \right)
$$
```

**显示**: $\left( \frac{a}{b} \right)$

#### 常用括号命令

| 命令 | 显示 | 命令 | 显示 |
|------|------|------|------|
| `\left(` `\right)` | $(\cdot)$ | `\left[` `\right]` | $[\cdot]$ |
| `\left\{` `\right\}` | $\{\cdot\}$ | `\left|` `\right|` | $|\cdot|$ |

#### 使用规则

- 在专业化风格中，建议使用自动调整大小的括号
- 在简洁化风格中，可以使用普通括号

**专业化示例**:
```markdown
$$
\left( \sum_{i=1}^{n} x_i \right)
$$
```

**简洁化示例**:
```markdown
$$
(\sum_{i=1}^{n} x_i)
$$
```

### 矩阵

#### 矩阵环境

**规则**: 使用矩阵环境定义矩阵

**常用矩阵环境**:

1. **无括号矩阵** (`matrix`)
   ```markdown
   $$
   \begin{matrix}
   a & b \\
   c & d
   \end{matrix}
   $$
   ```

2. **圆括号矩阵** (`pmatrix`)
   ```markdown
   $$
   \begin{pmatrix}
   a & b \\
   c & d
   \end{pmatrix}
   $$
   ```

3. **方括号矩阵** (`bmatrix`)
   ```markdown
   $$
   \begin{bmatrix}
   a & b \\
   c & d
   \end{bmatrix}
   $$
   ```

4. **花括号矩阵** (`vmatrix`)
   ```markdown
   $$
   \begin{vmatrix}
   a & b \\
   c & d
   \end{vmatrix}
   $$
   ```

#### 矩阵元素

- 使用 `&` 分隔列元素
- 使用 `\\` 分隔行

**示例**:
```markdown
$$
\begin{pmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{pmatrix}
$$
```

### 求和与积分

#### 求和符号

**格式**:
```markdown
\sum_{下限}^{上限}
```

**示例**:
```markdown
$$
\sum_{i=1}^{n} x_i
$$
```

**显示**: $\sum_{i=1}^{n} x_i$

#### 积分符号

**格式**:
```markdown
\int_{下限}^{上限}
```

**示例**:
```markdown
$$
\int_{a}^{b} f(x) \, dx
$$
**显示**: $\int_{a}^{b} f(x) \, dx$

#### 多重积分

**示例**:
```markdown
$$
\iint_{D} f(x,y) \, dx \, dy
$$
```

**显示**: $\iint_{D} f(x,y) \, dx \, dy$

### 极限

**格式**:
```markdown
\lim_{变量 \to 值}
```

**示例**:
```markdown
$$
\lim_{x \to \infty} f(x)
$$
```

**显示**: $\lim_{x \to \infty} f(x)$

## 公式编号

### 标准编号

**格式**: 使用 `\tag{编号}` 命令

**示例**:
```markdown
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)} \tag{2}
$$
```

### 自动编号

**在LaTeX文档中**，可以使用 `equation` 环境自动编号：

```latex
\begin{equation}
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
\end{equation}
```

**但在Markdown中**，应转换为标准格式并手动编号：

```markdown
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)} \tag{2}
$$
```

## 常见错误与修正

### 错误1: 未正确包裹的数学表达式

**错误示例**:
```markdown
函数 f(x) = x^2 在区间 [a,b] 上连续。
```

**修正**:
```markdown
函数 $f(x) = x^2$ 在区间 $[a,b]$ 上连续。
```

### 错误2: 上下标未用花括号包裹

**错误示例**:
```markdown
$$
x^2n + x_max
$$
```

**修正**:
```markdown
$$
x^{2n} + x_{max}
$$
```

### 错误3: 使用非标准格式

**错误示例**:
```markdown
\[
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
\]
```

**修正**:
```markdown
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$
```

### 错误4: 公式前后缺少空行

**错误示例**:
```markdown
牛顿迭代公式为：
$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$
其中：$x_k$ 为近似解。
```

**修正**:
```markdown
牛顿迭代公式为：

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}
$$

其中：$x_k$ 为近似解。
```

### 错误5: 直接输入希腊字母

**错误示例**:
```markdown
$$
α + β = γ
$$
```

**修正**:
```markdown
$$
\alpha + \beta = \gamma
$$
```

## 风格转换规则

### Professional风格

**特点**:
- 使用完整LaTeX语法
- 包含所有必要的括号和分隔符
- 公式表达严谨、规范

**转换规则**:
1. 所有分数使用 `\frac{a}{b}` 格式
2. 所有括号使用自动调整大小的 `\left(` `\right)`
3. 所有运算符使用LaTeX命令（如 `\times`）
4. 所有希腊字母使用LaTeX命令

**示例**:
```markdown
$$
\left( \sum_{i=1}^{n} x_i \right) \times \left( \sum_{j=1}^{m} y_j \right)
$$
```

### Concise风格

**特点**:
- 简化公式表达
- 移除冗余括号和分隔符
- 公式表达简洁、直观

**转换规则**:
1. 简单分数可以使用 `a/b` 格式
2. 普通括号使用 `()` 而非 `\left(` `\right)`
3. 乘法可以使用 `*` 而非 `\times`
4. 除法可以使用 `/` 而非 `\frac`

**示例**:
```markdown
$$
(\sum_{i=1}^{n} x_i) * (\sum_{j=1}^{m} y_j)
$$
```

### Standard风格

**特点**:
- 保持原文风格
- 仅进行格式规范化
- 不改变公式表达方式

**转换规则**:
1. 仅转换非标准格式为标准格式
2. 不改变原有的表达方式
3. 保持原文的括号、运算符等风格

## 质量检查清单

在完成公式规范化后，应检查以下项目：

### 格式检查
- [ ] 所有独立公式使用 `$$ ... $$` 格式
- [ ] 所有行内公式使用 `$ ... $` 格式
- [ ] 独立公式前后有适当空行
- [ ] 没有使用禁止的格式（如 `\[ ... \]`）

### 语法检查
- [ ] 所有上下标正确使用花括号
- [ ] 所有分数格式正确
- [ ] 所有希腊字母使用LaTeX命令
- [ ] 所有运算符使用正确

### 一致性检查
- [ ] 全文变量命名格式一致
- [ ] 全文运算符格式一致
- [ ] 全文希腊字母格式一致
- [ ] 全文括号格式一致

### 语义检查
- [ ] 公式数学含义保持不变
- [ ] 没有增删文字内容
- [ ] 没有改写句子结构
- [ ] 公式编号正确
