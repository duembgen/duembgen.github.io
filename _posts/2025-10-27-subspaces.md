---
layout: post
title: "SOS & Moments: The Subspace View"
date: 2025-10-27
---

*This writeup has made my [previous post "series" on Kernel-Image-Primal-Dual SOS formulations](/research/2025/08/24/kipd-minimization.html) somewhat obsolete. It provides a more mathematically principled way of deriving things, by embracing the subspace view. I decided to restart from scratch after reading [this](https://francisbach.com/sums-of-squares-for-dummies/) great blog post of Francis Bach.*

In this post, we'll explore a geometric perspective on sum-of-squares (SOS) and moment relaxations for solving polynomial optimization problems. In the literature, we come across very different formulations, and the connections between those formulations are often blurred. I hope that this blogpost clarifies things for the reader the way it did for me! 

You can run the notebook implementing the toy example here: 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/duembgen/notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F2025-10-27-subspaces.ipynb)

### The Original Problem

Let's consider a general non-convex optimization problem of the form:

$$
\min_{\mathbf{x} \in \mathcal{X}} p(\mathbf{x})
$$

where $p(\mathbf{x})$ is a polynomial and $\mathcal{X}$ is a set defined by polynomial equalities, for instance, $\mathcal{X} = \\{ \mathbf{x} \in \mathbb{R}^d \mid q_i(\mathbf{x}) = 0, \,i\in[n] \\}$, where we introduced the shorthand $[n]$ for $\\{1, \ldots, n\\}$. This problem may in general be hard to solve due to the non-convexity of the objective and the feasible set.

A powerful technique to tackle such problems is to solve a series of convex relaxations. To do so, we first rewrite the problem using "lifted" variables. We define a vector of monomials, $\phi(\mathbf{x})$, which in machine learning would be called the feature vector. The objective can then be written as an inner product $p(\mathbf{x}) = \langle \mathbf{C}, \phi(\mathbf{x})\phi(\mathbf{x})^\top \rangle$ for some matrix $\mathbf{C}$, where $\langle, \rangle$ is trace inner product. Our problem becomes:

$$
\min_{\mathbf{x} \in \mathcal{X}} \langle \mathbf{C}, \phi(\mathbf{x})\phi(\mathbf{x})^\top \rangle
$$

The matrix $\mathbf{M}(\mathbf{x}) = \phi(\mathbf{x})\phi(\mathbf{x})^\top$ is sometimes known as a (pseudo) moment matrix. 

### The Subspace View

The core idea is to write everything in terms of the vector space spanned by these moment matrices, and its orthogonal complement. Let's define the subspace $\mathcal{V}$ as:

$$
\mathcal{V} = \text{span} \{ \phi(\mathbf{x})\phi(\mathbf{x})^\top \mid \mathbf{x} \in \mathcal{X} \}
$$

Every feasible point of our lifted problem lies within this subspace $\mathcal{V}$. In other words, we can define a basis $\\{ \mathbf{B}_i \\}\_{i\in[n\_b]}$, so that every element $\mathbf{X}$ of $\mathcal{V}$ can be written as

$$
\mathbf{X} = \sum_i \alpha_i \mathbf{B}_i,
$$

for some choices $\alpha_i$. In particular, there exist some $\alpha$ that allow to characterize each element of the feasible set $\mathcal{X}$. 

If we call $\mathcal{K}$ the space of all admissible moment matrices, i.e., matrices $\mathbf{M}$ for which there exists a positive measure $\mu$ such that $\mathbf{M}=\int \phi(\mathbf{x})\phi(\mathbf{x})^\top d\mu(\mathbf{x})$, that space corresponds to the closure of the convex hull of all $\phi(\mathbf{x})\phi(\mathbf{x})$ for $\mathbf{x}\in\mathcal{X}$ (see [this post](https://francisbach.com/sums-of-squares-for-dummies/) for more details, and below for the visualization of our toy example). 

{% include figure.liquid
  path="/assets/images/blog/2025-10-27/subspaces-export.svg"
  alt="Visualization of subspace $\mathcal{V}$ and $\mathcal{X},\mathcal{K}$ for the running example"
  caption="Visualization of subspace $\mathcal{V}$ and $\mathcal{X},\mathcal{K}$ for the running example"
  zoomable=true
  sizes="(max-width:30px)"
%}


<div class="example-box" markdown="1"> 

#### Running Example

Let's make this concrete with a simple example that we'll follow throughout the post.
- **Feasible Set**: $\mathcal{X} = \\{x \in \mathbb{R} \mid q_0(x)=x^2 - 1 = 0\\}$, which is just the set $\\{-1, 1\\}$.
- **Lifting Map**: We use the monomial vector $\phi(x) = [1, x, x^2, x^3]^\top$. 

For $x=1$, the moment matrix is:

$$
\phi(1)\phi(1)^\top = \begin{pmatrix} 1 \\ 1 \\ 1 \\ 1 \end{pmatrix} \begin{pmatrix} 1 & 1 & 1 & 1 \end{pmatrix} = \begin{pmatrix} 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 \end{pmatrix} =: \mathbf{B}_1
$$

For $x=-1$, the moment matrix is:

$$
\phi(-1)\phi(-1)^\top = \begin{pmatrix} 1 \\ -1 \\ 1 \\ -1 \end{pmatrix} \begin{pmatrix} 1 & -1 & 1 & -1 \end{pmatrix} = \begin{pmatrix} 1 & -1 & 1 & -1 \\ -1 & 1 & -1 & 1 \\ 1 & -1 & 1 & -1 \\ -1 & 1 & -1 & 1 \end{pmatrix} =: \mathbf{B}_2
$$

The subspace $\mathcal{V}$ is the span of these two matrices, $\mathcal{V} = \text{span}(\mathbf{B}_1, \mathbf{B}_2)$. This is a 2-dimensional subspace within the ambient space of $4 \times 4$ symmetric matrices, which has dimension $\frac{4 \times 5}{2} = 10$. For a more compact notation, we use the half-vectorization operator and define $\mathbf{b}_i:=\mathrm{vech}(\mathbf{B}_i)\in\mathbb{R}^{10}$, where we scale off-diagonal elements by $\sqrt{2}$ to ensure $\langle \mathbf{A}, \mathbf{B}\rangle = \mathbf{a}^\top\mathbf{b}$.
</div>

We will also need a basis for $\mathcal{V}^{\perp}$, the nullspace of the set $\\{ \phi(\mathbf{x})\phi(\mathbf{x})^T, \mathbf{x} \in \mathcal{X} \\}$. Let's call the basis vectors $\\{\mathbf{U}_j\\}\_{j\in [n\_u]}$. By definition of the nullspace, for any $\mathbf{x} \in \mathcal{X}$, we must have:

$$
\langle \mathbf{U}_j, \phi(\mathbf{x})\phi(\mathbf{x})^T \rangle = 0
$$

<div class="example-box" markdown="1">
#### Running Example
Our ambient space of symmetric $4 \times 4$ matrices is 10-dimensional, and we found that $\text{dim}(\mathcal{V}) = 2$. Therefore, the nullspace $\mathcal{V}^{\perp}$ has dimension $10 - 2 = 8$. This means we have 8 nullspace basis vectors, and it is less straight forward to write them down. Instead, you can see a plot of the numerically found vectors below. The procedure of finding these, using an SVD, is outlined in [Appendix 2](#appendix2).

{% include figure.liquid
  path="assets/images/blog/2025-10-27/output_7_0.png"
  width=300
  caption="Numerically found nullspace basis vectors"
%}

{% include figure.liquid
  path="assets/images/blog/2025-10-27/output_6_0.png"
  width=300
  caption="Numerically found span basis vectors"
%}


</div>




### The Moment Relaxation

To derive tractable relaxations, we can rewrite the problem as a (linear) problem on the space of measures:

$$
\begin{align*}
\min_{\mu} & \int \langle \mathbf{C}, \phi(\mathbf{x})\phi(\mathbf{x})^\top \rangle d\mu(\mathbf{x}) 
= \langle \mathbf{C}, \int \phi(\mathbf{x})\phi(\mathbf{x})^\top d\mu(\mathbf{x}) \rangle 
\\ 
& \text{s.t.} \quad \phi(\mathbf{x})\phi(\mathbf{x})^\top \in \mathcal{V}.
\end{align*}
$$

Now we want to find a computationally tractable outer approximation of the set 

$$
\mathcal{K} = \{\mathbf{M} \;| \mathbf{M} = \int_\mathcal{X} \phi(\mathbf{x})\phi(\mathbf{x})^\top d\mu(x)\ \text{for some measure $\mu$.}\}
$$

An intuitive choice is to add all characteristics of this set that are computationally easy to handle:

$$
\mathcal{\widehat{K}} = \{\mathbf{M} \;| \begin{cases} 
& \mathbf{M} = \sum_i \alpha_i \mathbf{B}_i & \text{(want to lie in same subspace)} \\ 
& \mathbf{M} \succeq 0 & \text{(because it is an outer product of same vector and $\mu \geq 0$)} \\
& \langle \mathbf{A}_0, \mathbf{M} \rangle = 1 & \text{(we assume normalization and that $\phi(\mathbf{x})_0=1$)} 
\end{cases} \}
$$

Here, $\mathbf{A}_0$ is a matrix with top-left element equal to 1.  With this choice, we obtain our first convex relaxation: 

$$
\begin{align*}
\textbf{(Moment-Image)} \quad \min_{\alpha_i, \gamma} \quad & \sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{C} \rangle \\
\text{s.t.} \quad & \sum_i \alpha_i \mathbf{B}_i \succeq 0 \\
& \sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{A}_0 \rangle = 1
\end{align*}
$$


### The SOS Relaxation

We will see now that we can also derive the classic Sum-of-Squares (SOS) relaxation, using this time the basis $\{\mathbf{U}_j\}$ for the orthogonal complement of the subspace, $\mathcal{V}^{\perp}$. 

The SOS relaxation can be written as:

$$
\begin{align*}
\max_{c, \mathbf{H}} \quad & c \\
\text{s.t.} \quad & \langle \mathbf{C}, \phi(\mathbf{x})\phi(\mathbf{x})^T \rangle - c = \langle \mathbf{H}, \phi(\mathbf{x})\phi(\mathbf{x})^T \rangle, \quad \forall \mathbf{x} \in \mathcal{X} \\
& \mathbf{H} \succeq 0
\end{align*}
$$

We can reuse the homogenization matrix $\mathbf{A}_0$ to write $c = c \cdot \langle \mathbf{A}_0, \phi(\mathbf{x})\phi(\mathbf{x})^T \rangle$. Thus the constraint becomes:

$$
\langle \mathbf{C} - c\mathbf{A}_0 - \mathbf{H}, \phi(\mathbf{x})\phi(\mathbf{x})^T \rangle = 0, \quad \forall \mathbf{x} \in \mathcal{X}
$$

In other words, the matrix $\mathbf{C} - c\mathbf{A}_0 - \mathbf{H}$ is in the nullspace of $\mathcal{V}$! This means we can express it as a linear combination of the nullspace basis vectors $\{\mathbf{U}_i\}$:

$$
\mathbf{C} - c\mathbf{A}_0 - \mathbf{H} = \sum_i \beta_i \mathbf{U}_i
$$

Rearranging this gives the constraint from our **(SOS-Image)** formulation: $\mathbf{C} - c\mathbf{A}_0 - \sum_i \beta_i \mathbf{U}_i = \mathbf{H} \succeq 0$.

Therefore, the SOS relaxation is:

$$
\begin{align*}
\textbf{(SOS-Image)} \quad \max_{c, \beta_j} \quad & c \\
\text{s.t.} \quad & \mathbf{C} - c \mathbf{A}_0 - \sum_j \beta_j \mathbf{U}_j \succeq 0
\end{align*}
$$

<div class="example-box" markdown="1">
#### Running Example

For the running example problem, we now introduce a cost function to minimize, to then check if the convex relaxations are tight. 

We chose $f(x)=1+x$ so that we have the optimum $\hat{x}=-1$ with optimal cost $\hat{c}=0$. With this choice, we obtain: 

```python
import cvxpy as cp
alpha = cp.Variable(len(B_basis))
objective = cp.Minimize(
    cp.sum([alpha[i] * cp.trace(C @ Bi) for i, Bi in enumerate(B_basis)])
)
constraints = [
    cp.sum([alpha[i] * Bi for i, Bi in enumerate(B_basis)]) >> 0,
    cp.sum([alpha[i] * cp.trace(A0 @ Bi) for i, Bi in enumerate(B_basis)]) == 1,
]

problem = cp.Problem(objective, constraints)
problem.solve(solver="SCS")

X = cp.sum([alpha[i].value * Bi for i, Bi in enumerate(B_basis)])

print(f"  optimal value: {problem.value:.4f}")
print(f"  alpha: {alpha.value.round(3)}")
print(f"  X:\n{X.round(3)}")
```



```raw
optimal value: -0.0000
alpha: [ 0. -4.]
X:
[[ 1. -1.  1. -1.]
 [-1.  1. -1.  1.]
 [ 1. -1.  1. -1.]
 [-1.  1. -1.  1.]]
```



```python
c = cp.Variable()
beta = cp.Variable(len(U_basis))
objective = cp.Maximize(c)
constraints = [
    C - c * A0 + cp.sum([beta[i] * Ui for i, Ui in enumerate(U_basis)]) >> 0
]

problem = cp.Problem(objective, constraints)
problem.solve(solver="SCS", verbose=False)

H = C - problem.value * A0 + cp.sum([beta[i].value * Ui for i, Ui in enumerate(U_basis)])

print(f"  optimal value: {problem.value:.4f}")
print(f"  beta: {beta.value.round(3)}")
print(f"  H:\n{H.round(3)}")
```

```raw
optimal value: -0.0000
beta: [0.578 0.161 0.409 0.161 0.578 0.41  0.161 0.409]
H:
[[0.126 0.125 0.124 0.125]
 [0.125 0.125 0.125 0.125]
 [0.124 0.125 0.126 0.125]
 [0.125 0.125 0.125 0.125]]
```

</div>

### Kernel Forms

We have called the problem we derived thus far **(Moment-Image)** and **(SOS-Image)** because of their particular form: the matrix variable is parametrized as the image of some basis functions -- in one case, the basis of the span, in the other case, the nullspace basis. For each problem, we can also derive a so-called **Kernel** form. We introduce the matrix variable first, and then constrain it to lie in the correct subspace, using elements from the orthogonal complement. Thus, in kernel form, the primal moment relaxation is formulated using the basis of the nullspace $\mathcal{V}^\perp$, and the dual SOS program is formulated using the basis of the subspace $\mathcal{V}$.

Here is a summary table:

|<br> | **Image Form** <br><br>| **Kernel Form** <br><br>|
| **Dual (SOS)**$\;\;$  | $$\begin{align} \max\;& c \\ &\text{s.t. }\mathbf{C} - c\mathbf{A}_0- \sum_j \beta_j \mathbf{U}_j \succeq 0\end{align}$$ | $$\begin{align}\max\;&c  \\  \text{s.t.}\; &\langle \mathbf{B}_i, \mathbf{C} - c \mathbf{A}_0  - \mathbf{H} \rangle = 0, \; i\in[n_b]  \\ &\mathbf{H} \succeq 0 \end{align}$$ <br><br><br> |
| **Primal (Moment)**$\;\;$  | $$\begin{align*}\min &\sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{C} \rangle  \\ \text{s.t. } & \sum_i \alpha_i \mathbf{B}_i \succeq 0 \\ & \sum_i \alpha_i \langle \mathbf{A}_0, \mathbf{B}_i \rangle = 1 \end{align*}$$ | $$\begin{align*}\min &\langle \mathbf{C}, \mathbf{X} \rangle \\ \text{s.t. }  \; &\langle \mathbf{X}, \mathbf{U}_j \rangle = 0, \; j \in [n_u] \\ & \langle \mathbf{X}, \mathbf{A}_0 \rangle = 1 \\ & \mathbf{X} \succeq 0, \end{align*}$$ |

Let's see in more detailed how the kernel forms were derived above:

For the dual form, the condition $\mathbf{H} = \mathbf{C} - c\mathbf{A}_0 - \sum_i \beta_j \mathbf{U}_j$ is equivalent to:
- $\mathbf{H} - \mathbf{C} + c\mathbf{A}_0$ lies in the affine subspace $(\mathbf{C} - c\mathbf{A}_0) + \mathcal{V}^{\perp}$.
- This implies $\langle \mathbf{H} - \mathbf{C} + c\mathbf{A}_0, \mathbf{B}_i \rangle = 0$ for all basis vectors $\mathbf{B}_i \in \mathcal{V}$. 

For the primal form, the condition $\mathbf{X} = \sum_i \alpha_i \mathbf{B}_i + \gamma \mathbf{A}_0$ is equivalent to:
- $\mathbf{X}$ lies in the affine subspace $\mathcal{V} + \text{span}(\mathbf{A}_0)$.
- This implies $\langle \mathbf{X} - \gamma \mathbf{A}_0, \mathbf{U}_j \rangle = 0$ for all basis vectors $\mathbf{U}_j \in \mathcal{V}^{\perp}$.


It is interesting to note that the diagonals of the table are duals of each other! The dual of the image SOS form is the kernel moment form, and the dual of the image moment form is the kernel SOS form. For pedagogical purposes, we derive this in [Appendix 1](#appendix1) below.

***

<div class="example-box" markdown="1">
#### Running Example

We solve the example problem using each of the four SDP formulations. Since there are only two basis vectors and 8 nullspace basis vectors, we expect the **Moment Image** form and the **SOS Kernel** form to be the most efficient. 
Below is the output of the provided example script: 

```raw
sos image solution:
  optimal value: -1.0000
  x: -1.0
  time: 28ms

sos kernel solution:
  optimal value: -1.0000
  x: -1.0
  time: 9ms

moment image solution:
  optimal value: -1.0000
  x: -1.0
  time: 8ms

moment kernel solution:
  optimal value: -1.0000
  x: -1.0
  time: 14ms
done
```
Although the timings are very imprecise (they include the time to setup the problem and convert it to standard form) we can see that the sos kernel and the moment image forms take the least time to solve. 

</div>

### Appendix 1: Verification via dual {#appendix1}

We can verify our calculations by checking that the duals as outlined above. 


#### Image SOS
The image SOS formulation is:

$$
\begin{align*}
\max_{c, \beta_i} \quad & c \\
\text{s.t.} \quad & \mathbf{C} - c \mathbf{A}_0 - \sum_i \beta_i \mathbf{U}_i \succeq 0
\end{align*}
$$

This is a "textbook SDP", and its dual is:

$$
\begin{align*}
\min_{\mathbf{X}} \quad & \langle \mathbf{C}, \mathbf{X} \rangle \\
\text{s.t.} \quad & \langle \mathbf{X}, \mathbf{U}_i \rangle = 0, \quad i \in [n_u] \\
& \langle \mathbf{X}, \mathbf{A}_0 \rangle = 1 \\
& \mathbf{X} \succeq 0
\end{align*}
$$

which is precisely the **Primal (Moment) Kernel Form**.

#### Image Moment

The image Moment formulation is:

$$
\begin{align*}
\min_{\alpha_i, \gamma} \quad & \sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{C} \rangle \\
\text{s.t.} \quad & \sum_i \alpha_i \mathbf{B}_i \succeq 0 \\
& \sum_i \alpha_i \langle \mathbf{A}_0, \mathbf{B}_i \rangle = 1
\end{align*}
$$

The Lagrangian is:

$$
L(\alpha, H, c) = \sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{C} \rangle - \langle \sum_i \alpha_i \mathbf{B}_i, \mathbf{H} \rangle - c(\sum_i \alpha_i \langle \mathbf{A}_0, \mathbf{B}_i \rangle - 1).
$$

Rearranging terms gives: 

$$
L = \sum_i \alpha_i \langle \mathbf{B}_i, \mathbf{C} - \mathbf{H} - c\mathbf{A}_0 \rangle + c.
$$

The dual function is $\max_{\alpha} L(\alpha, H, c)$, which is $-\infty$ unless $\langle \mathbf{B}_i, \mathbf{C} - \mathbf{H} - c\mathbf{A}_0 \rangle = 0$ for all $i$. The dual problem is therefore:

$$
\begin{align*}
\max_{c, \mathbf{H}} \quad & c \\
\text{s.t.} \quad & \langle \mathbf{B}_i, \mathbf{C} - \mathbf{H} - c\mathbf{A}_0 \rangle = 0, \quad i \in [n_b] \\
& \mathbf{H} \succeq 0
\end{align*}
$$

This is precisely the **Dual (SOS) Kernel Form**.

### Appendix 2: Numerical Basis Calclation {#appendix2}

A practical question is how to find the bases $\{\mathbf{B}_i\}$ for $\mathcal{V}$ and $\{\mathbf{U}_j\}$ for $\mathcal{V}^\perp$. A simple approach, assuming one can generate feasible samples of $\mathcal{X}$, is to find these bases numerically by sampling. The procedure is as follows:
1. Generate many sample points $\mathbf{x}_k \in \mathcal{X}$.
2. Form the corresponding moment matrices $\mathbf{M}_k = \phi(\mathbf{x}_k)\phi(\mathbf{x}_k)^\top$.
3. Stack the vectorized versions of these matrices into a large matrix $\mathbf{L} = [\text{vec}(\mathbf{M}_1), \text{vec}(\mathbf{M}_2), \dots]$.
4. Compute the Singular Value Decomposition (SVD) or QR decomposition of $\mathbf{L}$. The left singular vectors corresponding to non-zero singular values will form an orthonormal basis for the range space (our $\mathcal{V}$), and the vectors corresponding to zero singular values will form a basis for the nullspace (our $\mathcal{V}^\perp$).

### Conclusion and Discussion

We've seen that by taking a subspace perspective, we can derive alternative but equivalent relaxations for polynomial optimization problems. Depending on the dimensions of the subspace $\mathcal{V}$ and its complement $\mathcal{V}^\perp$, one form might be more computationally efficient than the other. For instance, if the nullspace $\mathcal{V}^\perp$ has a very small dimension, the primal kernel form might have far fewer constraints than the image form.

An obvious limitation of this approach is that it can not easily deal with inequality constraints. However, I would argue that at least the equality-constrained part can handled in a very elegant way through this subspace view. 

For a complete picture, it would be desirable to define the matrix $\mathbf{C}$ from samples directly, and to explore alternative bases as opposed to the monomial basis. I am planning to treat these topics in a follow-up blogpost. 
