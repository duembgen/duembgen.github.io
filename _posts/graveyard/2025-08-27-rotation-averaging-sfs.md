---
layout: post
title: "Solving Rotation Averaging from Samples"
date: 2025-08-27
categories: [research]
---

_This is another blogpost, based on my handwritten notes and completed plus polished [with a little help from Gemini](/misc/2025/08/18/blog-posts-in-2025.html)._

These notes solve a deceivingly simple instance of rotation averaging, inspired from Example 3.2 of {% cite cifuentes_sampling_2017 %}, but using real as opposed to complex rotation matrices, and elaborating more in detail the connections of this approach with the non-sampling versions. 

$$
\textbf{(R-min)} \quad 
\begin{align} \underset{\mathbf{R}}{\min} \quad & p(\mathbf{R}) \\ \text{s.t.} \quad & \mathbf{R}^T\mathbf{R} = \mathbf{I} \\
& \mathrm{det}(\mathbf{R})=1
\end{align}
$$

where $p(\mathbf{R})$ is some polynomial, given below, and the constraints enforce that $\mathbf{R}$ is an orthogonal matrix. A well-known relaxation of this problem is:

$$
\textbf{(R-max)} \quad \begin{align} \underset{\gamma, \mathbf{H}\succeq 0 }{\max} \quad & \gamma \\ \text{s.t.}
\quad & p(\mathbf{R}) - \gamma = v_d(\mathbf{R})^\top \mathbf{H} v_d(\mathbf{R}) \quad \forall \mathbf{R} \in \mathrm{SO}(2)
\end{align}
$$

where we have introduced $v_d(\mathbf{R})$, a polynomial basis vector for polynomials of degree $d$, for example the monomials:

$$
v_2(\mathbf{R})^\top  = \begin{bmatrix} h &  R_{11} & R_{12} & R_{21} & R_{22} & R_{11}^2 & R_{11}R_{12} & \cdots & R_{22}^2\end{bmatrix}.
$$


### First mistery: Dual feasibility

As we have seen in [this other blogpost](research/2025/08/23/kipd-minimization.html), we can formulate the dual of problem $\textbf{(R-max)}$, and then the dual variable $\mathbf{X}$ actually corresponds to the rank relaxation of the original problem. But why will this $\mathbf{X}$ actually obey the original primal constraints? 

### Second mistery: Sampling-based version

The second mistery is very related, and concerns the sample-based formulation of the original problem. As stated in {%cite cifuentes_sampling_2017 %}, we can solve the following problem:

$$
\textbf{(R-max-N)} \quad \begin{align} \underset{\gamma, \mathbf{H}\succeq 0 }{\max} \quad & \gamma \\ \text{s.t.}
\quad & p(\mathbf{R}_i) - \gamma = v_d(\mathbf{R}_i)^\top \mathbf{H} v_d(\mathbf{R}_i) \quad i=1,\ldots, N 
\end{align}
$$

where $\mathbf{R}_i$ are simply some feasible points of the original problem (i.e., valid rotations). How come that the dual matrix $\mathbf{X}$ when using this problem formulation will actually satisfy the original constraints? The problem **{(R-max-N)}** doesn't even know about the constraints! They were just used to create valid samples...

I hope that by the end of this blogpost I will have clear answers to both of these questions. 


*   [1. A non-sampling-based approach](#1-a-non-sampling-based-approach)
*   [2. A sampling-based approach](#2-a-sampling-based-approach)

## 1. A non-sampling-based-approach

In the non-sampling-based approach, we formulate the optimization problem over the continuous space of rotations.

### 1.a Minimal formulation

Let's consider the problem of minimizing a polynomial function $p(\mathbf{R})$ over the special orthogonal group SO(2), which represents rotations in 2D.


The objective function is given by:

$$
p(\mathbf{R}) = 4R_{21} - 2R_{12}R_{21} - 2R_{11}R_{22} + 3
$$

A 2D rotation matrix $\mathbf{R}$ can be parameterized by an angle $\theta$, or more conveniently for polynomial optimization, by two variables $a$ and $b$ such that $a^2+b^2=1$:

$$
\mathbf{R} = \begin{bmatrix} \cos(\theta) & \sin(\theta) \\ -\sin(\theta) & \cos(\theta) \end{bmatrix} = \begin{bmatrix} b & a \\ -a & b \end{bmatrix} = \begin{bmatrix} \sqrt{1-a^2} & a \\ -a & \sqrt{1-a^2} \end{bmatrix}
$$

where we have set $a = \sin(\theta)$ and $b = \cos(\theta)$. Substituting this into the objective function, we get a polynomial in terms of $a$:

$$
p(a) = 4(-a) - 2(a)(-a) - 2(\sqrt{1-a^2})(\sqrt{1-a^2}) + 3 = -4a + 2a^2 - 2(1-a^2) + 3 = 4a^2 - 4a + 1
$$

This is a simple quadratic function. We can find the minimum by taking the derivative with respect to $a$ and setting it to zero:

$$
\frac{\partial p(a)}{\partial a} = 8a - 4 = 0 \quad \implies \quad a^* = \frac{1}{2}
$$

This gives $b^* = \pm \sqrt{1 - (1/2)^2} = \pm \frac{\sqrt{3}}{2}$. The optimal rotation matrices are:

$$
\mathbf{R}_\pm^* = \begin{bmatrix} \pm \frac{\sqrt{3}}{2} & \frac{1}{2} \\ -\frac{1}{2} & \pm \frac{\sqrt{3}}{2} \end{bmatrix}
$$

The optimal value is $p(\mathbf{R}^*) = 4(1/2)^2 - 4(1/2) + 1 = 1 - 2 + 1 = 0$.

Now, let's see how to solve this using Semidefinite Programming.

#### 1.a.i The primal problem

To formulate this as an SDP, we first define a vector of variables $\mathbf{x} = [1, a, b]^T$. The constraints are $x_0 = 1$ and $a^2+b^2 = x_1^2 + x_2^2 = 1$ (Note that this constraint includes both the orthogonal constraints and the determinant constraint). The objective function in terms of $a$ and $b$ is $p(a,b) = -4a + 2a^2 - 2b^2 + 3$.

We can lift this problem into a higher-dimensional space using a matrix variable $\mathbf{X} = \mathbf{x}\mathbf{x}^T$.

$$
\mathbf{X} = \begin{bmatrix} 1 \\ a \\ b \end{bmatrix} \begin{bmatrix} 1 & a & b \end{bmatrix} = \begin{bmatrix} 1 & a & b \\ a & a^2 & ab \\ b & ab & b^2 \end{bmatrix} = \begin{bmatrix} X_{00} & X_{01} & X_{02} \\ X_{10} & X_{11} & X_{12} \\ X_{20} & X_{21} & X_{22} \end{bmatrix}
$$

The objective function can be written as a linear function of the elements of $\mathbf{X}$:

$$
p(\mathbf{X}) = -4X_{01} + 2X_{11} - 2X_{22} + 3X_{00} = \left\langle \begin{bmatrix} 3 & -2 & 0 \\ -2 & 2 & 0 \\ 0 & 0 & -2 \end{bmatrix}, \mathbf{X} \right\rangle
$$

The constraints become:

1.  $X_{00} = 1$: 

$$\left\langle \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}, \mathbf{X} \right\rangle = 1$$

2.  $a^2+b^2 = 1 \implies X_{11}+X_{22}=1$: 

$$\left\langle \begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}, \mathbf{X} \right\rangle = 0$$ 

Now to the SDP formulation.

The constraint $\mathbf{X} = \mathbf{x}\mathbf{x}^T$ is non-convex. We relax this to $\mathbf{X} \succeq \mathbf{x}\mathbf{x}^T$, which, by the Schur complement, is equivalent to:

$$
\begin{bmatrix} \mathbf{X} & \mathbf{x} \\ \mathbf{x}^T & 1 \end{bmatrix} \succeq 0
$$

However, a simpler relaxation that is often used is just $\mathbf{X} \succeq 0$. So we replace the rank-1 constraint $\mathbf{X} = \mathbf{x}\mathbf{x}^T$ with a positive semidefinite constraint $\mathbf{X} \succeq 0$.

The primal SDP is:


$$
\begin{align} \underset{\mathbf{X}}{\min} \quad & \left\langle \begin{bmatrix} 3 & -2 & 0 \\ -2 & 2 & 0 \\ 0 & 0 & -2 \end{bmatrix}, \mathbf{X} \right\rangle \\ \text{s.t.} \quad & \left\langle \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix}, \mathbf{X} \right\rangle = 1 \\ & \left\langle \begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}, \mathbf{X} \right\rangle = 0 \\ & \mathbf{X} \succeq 0 \end{align}
$$

It is not obvious how one would solve this by hand. As it turns out, the dual problem, on the other hand, is super simple to solve! 

#### 1.a.ii The dual problem

The dual problem can be formulated as:

$$
\begin{align} \underset{y_1, y_2}{\max} \quad & y_1 \\ \text{s.t.} \quad & \begin{bmatrix} 3 & -2 & 0 \\ -2 & 2 & 0 \\ 0 & 0 & -2 \end{bmatrix} - y_1 \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix} - y_2 \begin{bmatrix} -1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} \succeq 0 \end{align}
$$

Which simplifies to:

$$
\begin{pmatrix} 3-y_1+y_2 & -2 & 0 \\ -2 & 2-y_2 & 0 \\ 0 & 0 & -2-y_2 \end{pmatrix} \succeq 0
$$

For this matrix to be positive semidefinite, all its principal minors must be non-negative.

- One minor is simply given by: $-2-y_2 \ge 0 \implies y_2 \leq -2$.

- Another one is: $-(2-y_2)(2+y_2)=-(4 - y_2^2)=y_2^2 - 4 \geq 0$, which implies $y_2 \leq -2$ or $y_2 \geq 2$. Combining with the first condition, we still have $y_2 \leq -2$.

- The last one is: 
 
  $$\begin{align}
  0 & \leq (3-y_1+y_2)(2-y_2) - 4   \\
    &= 6-2y_1+2y_2-3y_2+y_1y_2 -y_2^2- 4 \\
    &=2-2y_1-y_2+y_1y_2-y_2^2 \\
    &\text{(using the fact that $y_2\leq -2$)} \\
    & \leq 2-2y_1+2-2y_1-4 \\ 
    & \leq -4y_1
  \end{align}
  $$

  and therefore $y_1\leq 0$

Since we want to maximize $y_1$, we should choose $y_1=0$. We therefore have strong duality! 

### 2. A sampling-based approach

We want to explore if a sampling-based approach can be more practical. The idea is to enforce the optimization constraints only on a set of sample points.

The dual problem is to find the largest $\gamma$ such that $p(\mathbf{x}) - \gamma$ is a sum of squares (SOS) of polynomials.

$$
\begin{align} \underset{\gamma}{\max} \quad & \gamma \\ \text{s.t.} \quad & p(\mathbf{x}_i) - \gamma \ge 0 \quad \forall \mathbf{x}_i \in \mathrm{SO}(2) \end{align}
$$

This can be written as finding a positive semidefinite matrix $\mathbf{H}$ such that for a vector of monomials $\mathbf{v}(\mathbf{x})$, we have $p(\mathbf{x}_i) - \gamma = \mathbf{v}(\mathbf{x}_i)^T \mathbf{H} \mathbf{v}(\mathbf{x}_i)$ for all samples $\mathbf{x}_i$.

Let $p_i = p(\mathbf{x}_i)$ and $\mathbf{v}_i = \mathbf{v}(\mathbf{x}_i)$.

$$
p_i - \gamma = \mathbf{v}_i^T \mathbf{H} \mathbf{v}_i
$$

If we stack the constraints for $N$ samples, we get $\mathbf{p} - \gamma\mathbf{1} = \mathrm{diag}(\mathbf{V}^T\mathbf{H}\mathbf{V})$.
Here $\mathbf{V} = [\mathbf{v}_1, \dots, \mathbf{v}_N]$.

#### 2.a With orthogonalization

To simplify the problem, we can use a basis where the samples are orthogonal. Let $\mathbf{V} = \mathbf{U}\mathbf{S}_r\mathbf{W}_r^T$ be the thin SVD of the matrix $\mathbf{V}$. Then we have:

$$
\mathbf{p} - \gamma\mathbf{1} = \mathrm{diag}(\mathbf{W}_r\mathbf{S}_r\mathbf{U}^T \mathbf{H} \mathbf{U}\mathbf{S}_r\mathbf{W}_r^T)
$$

Let $\mathbf{H}_r = \mathbf{S}_r\mathbf{U}^T \mathbf{H} \mathbf{U}\mathbf{S}_r$. Then we solve for a smaller matrix $\mathbf{H}_r \in \mathbb{R}^{r \times r}$ where $r$ is the rank of $\mathbf{V}$.

The dual variable $\mathbf{X}$ is related to the matrix $\mathbf{H}$. The elements of $\mathbf{X}$ are the dual variables to the constraints that define the moments of the distribution. The dual variable to the constraint $p(\mathbf{x}) - \gamma = \mathbf{v}(\mathbf{x})^T \mathbf{H} \mathbf{v}(\mathbf{x})$ is the moment matrix, which is our primal variable $\mathbf{X}$.

To recover $\mathbf{H}$ from $\mathbf{H}_r$, we can use the pseudoinverse: $\mathbf{U}^T\mathbf{H}\mathbf{U} = \mathbf{S}_r^{-1}\mathbf{H}_r\mathbf{S}_r^{-1}$. This only defines the projection of $\mathbf{H}$ onto the space spanned by the first $r$ left singular vectors of $\mathbf{V}$. The remaining components of $\mathbf{H}$ can be chosen arbitrarily as long as $\mathbf{H} \succeq 0$.

#### 2.b With a kernelized formulation

Instead of using monomials $\mathbf{v}(\mathbf{x})$, we can use a kernel function 

$$k(\mathbf{x}_i, \mathbf{x}) = \phi(\mathbf{x}_i)^T\phi(\mathbf{x}_j)$$. 

But we never have to explicitly use feature map $\phi$; instead, we can form the following formulation of an SOS polynomial:

$$
k(x)^\top K k(x) = \begin{bmatrix}k(x, x_1)
$$

Each column of the matrix $\mathbf{V}$ is then given by the feature map $\\phi(\mathbf{x}_i)$.

The Gram matrix $\mathbf{K}_{ij} = k(\mathbf{x}_i, \mathbf{x}_j)$ can be used directly, and this is known as the kernel trick. This avoids having to explicitly specify the monomial basis, which can be very high-dimensional.

### Conclusion

We have explored different ways to tackle the rotation averaging problem using semidefinite programming. The non-sampling-based approach provides an exact solution to the relaxed problem but can be computationally expensive. The sampling-based methods offer a more scalable alternative, especially when combined with orthogonalization or kernel methods. These techniques transform a non-convex problem over the manifold of rotations into a convex SDP that can be solved efficiently, providing a powerful tool for robust geometric estimation in various applications.

## Sandbox

### 1.b Vectorized formulation

We can also vectorize the entire rotation matrix $\mathbf{R}$. Let $\mathbf{x} = [1, R_{11}, R_{12}, R_{21}, R_{22}]^T$. The objective function is linear in the outer product $\mathbf{X} = \mathbf{x}\mathbf{x}^T$:

$$
p(\mathbf{X}) = 4X_{03} - 2X_{23} - 2X_{14} + 3X_{00}
$$

So the cost matrix $\mathbf{C}$ is:

$$
\mathbf{C} = \begin{bmatrix} 3 & 0 & 0 & 2 & -1 \\ 0 & 0 & 0 & 0 & -1 \\ 0 & 0 & 0 & -1 & 0 \\ 2 & 0 & -1 & 0 & 0 \\ -1 & -1 & 0 & 0 & 0 \end{bmatrix}
$$

The constraints are:
1.  $X_{00}=1$
2.  $\mathbf{R}^T\mathbf{R} = \mathbf{I}$, which gives:
    *   $R_{11}^2 + R_{21}^2 = 1 \implies X_{11}+X_{33}=1$
    *   $R_{12}^2 + R_{22}^2 = 1 \implies X_{22}+X_{44}=1$
    *   $R_{11}R_{12} + R_{21}R_{22} = 0 \implies X_{12}+X_{34}=0$
3.  $\mathbf{R}\mathbf{R}^T = \mathbf{I}$ gives equivalent constraints.
4.  The determinant constraint $\det(\mathbf{R}) = R_{11}R_{22} - R_{12}R_{21} = 1 \implies X_{14}-X_{23}=1$.

#### 1.b.i The primal problem

$$
\begin{align} \underset{\mathbf{X}}{\min} \quad & \langle \mathbf{C}, \mathbf{X} \rangle \\ \text{s.t.} \quad & X_{00} = 1 \\ & X_{11} + X_{33} = 1 \\ & X_{22} + X_{44} = 1 \\ & X_{12} + X_{34} = 0 \\ & X_{14} - X_{23} = 1 \\ & \mathbf{X} \succeq 0 \end{align}
$$

#### 1.b.ii The dual problem

$$
\begin{align} \underset{\mathbf{y}}{\max} \quad & y_0 + y_1 + y_2 + y_4 \\ \text{s.t.} \quad & \mathbf{C} - \mathrm{diag}(y_0, y_1, y_2, y_1, y_2) - y_3(\mathbf{e}_1\mathbf{e}_2^T+\mathbf{e}_2\mathbf{e}_1^T+\mathbf{e}_3\mathbf{e}_4^T+\mathbf{e}_4\mathbf{e}_3^T) \\ & - y_4(\mathbf{e}_1\mathbf{e}_4^T+\mathbf{e}_4\mathbf{e}_1^T-\mathbf{e}_2\mathbf{e}_3^T-\mathbf{e}_3\mathbf{e}_2^T) \succeq 0 \end{align}
$$

where $\mathbf{e}_i$ are the standard basis vectors.

