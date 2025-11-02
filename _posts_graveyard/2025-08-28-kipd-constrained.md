---
layout: post
title: "KIPD: From Unconstrained to Constrained Minimization"
date: 2025-08-28
categories: [research]
---

_This is a follow-up to my [previous post](/research/2025/08/24/kipd-minimization.html) on using Sum-of-Squares (SOS) for unconstrained minimization. This post extends the framework to handle polynomial equality constraints, leveraging deeper results from algebraic geometry. The evolution of these posts has been greatly accelerated with the help of Gemini, a process I discuss [here](/misc/2025/08/18/blog-posts-in-2025.html)._

In the last post, we saw how to find a global lower bound for a polynomial $p(x)$ by finding the largest $\gamma$ such that $p(x) - \gamma$ is a sum of squares (SOS). Now, we consider the constrained optimization problem:

$$
\begin{aligned}
\min_{x} \quad & p(x) \\
\text{s.t.} \quad & g_j(x) = 0, \quad j=1, \dots, m \\
\end{aligned}
$$

For simplicity, we will consider a single equality constraint $g(x) = 0$. The core idea remains the same: reformulate the problem as finding the largest scalar $\gamma$ that acts as a lower bound. However, the non-negativity condition no longer needs to hold for all $x$, only for those $x$ that satisfy the constraint.

$$
\begin{aligned}
\max_{\gamma} \quad & \gamma \\
\text{s.t.} \quad & p(x) - \gamma \geq 0 \quad \forall x \text{ s.t. } g(x) = 0 \\
\end{aligned}
$$

This is where we need a more powerful tool than simple SOS decomposition. The algebraic certificate for a polynomial being non-negative over a variety (a set defined by polynomial equalities) is given by the **Positivstellensatz**. A simplified version (Putinar's Positivstellensatz) tells us that a sufficient condition for $p(x) - \gamma \ge 0$ on the set where $g(x)=0$ is the existence of an SOS polynomial $s(x)$ and an arbitrary polynomial "Lagrange multiplier" $t(x)$ such that:

$$
p(x) - \gamma = s(x) + t(x)g(x)
$$

This identity must hold for all $x$. By substituting the coefficients of $t(x)$ as decision variables, we can again formulate a semidefinite program (SDP). This leads to our new fundamental problem:

$$
\begin{aligned}
\textbf{(SOS-opt-C)}\quad\max_{\gamma, \mathbf{X}, \mathbf{t}} \quad & \gamma \\
\text{s.t.} \quad & p(x) - \gamma = \mathbf{v}(x)^\top \mathbf{X} \mathbf{v}(x) + t(x)g(x) \\
& \mathbf{X} \succeq 0
\end{aligned}
$$

Here, $\mathbf{t}$ represents the vector of coefficients of the multiplier polynomial $t(x)$. The degrees of the monomial vector $\mathbf{v}(x)$ and the multiplier $t(x)$ must be chosen high enough for the identity to be possible. This approach is the foundation of the powerful Lasserre hierarchy for polynomial optimization.

Just like before, this problem can be formulated in four ways.

### A Quick Overview

The introduction of the multiplier polynomial $t(x)g(x)$ adds a new linear term to our coefficient-matching equations. This term is linear in the unknown coefficients of $t(x)$, which become new decision variables in our primal forms. In the dual forms, this results in new linear constraints on the dual variables.


GEMINI: correct the table using the new formulation. 

| | **Kernel Form** | **Image Form** |
|:---|:---|:---|
| **Primal** | **(P-K) Primal Kernel Problem** <br> Maximize $\gamma$ by finding a Gram matrix $\mathbf{X}$ and multiplier coefficients $\mathbf{t}$ that satisfy coefficient-matching constraints. <br><br> $$\begin{aligned} \max_{\mathbf{X}, \gamma, \mathbf{t}} \quad & \gamma \\ \text{s.t.} \quad & p_i - \delta_{i0}\gamma = \langle \mathbf{A}_i, \mathbf{X} \rangle + \sum_k t_k g_{i-k} \\ & \mathbf{X} \succeq 0 \end{aligned}$$ | **(P-I) Primal Image Problem** <br> Maximize $\gamma$ subject to a parameterized Gram matrix being positive semidefinite. The parameterization now also depends on $\mathbf{t}$. <br><br> $$\begin{aligned} \max_{\mathbf{s}, \gamma, \mathbf{t}} \quad & \gamma \\ \text{s.t.} \quad & \mathbf{Y}(\mathbf{p}, \mathbf{g}, \mathbf{t}) - \gamma \mathbf{A}_0 + \sum_j s_j \mathbf{B}_j \succeq 0 \end{aligned}$$ |
| **Dual** | **(D-K) Dual Kernel Problem** <br> Minimize a linear function of the polynomial's coefficients, with additional linear constraints on the dual variables. <br><br> $$\begin{aligned} \min_{\boldsymbol{\lambda}} \quad & \boldsymbol{\lambda}^\top \mathbf{p} \\ \text{s.t.} \quad & \sum_i \lambda_i \mathbf{A}_i \succeq 0 \\ & \lambda_0 = 1 \\ & \sum_i \lambda_i g_{i-k} = 0, \quad \forall k \end{aligned}$$ | **(D-I) Dual Image Problem** <br> Minimize an inner product subject to normalization and additional orthogonality constraints related to $g(x)$. <br><br> $$\begin{aligned} \min_{\mathbf{X}} \quad & \langle \mathbf{X}, \mathbf{Y}(\mathbf{p}) \rangle \\ \text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_0 \rangle = 1 \\ & \langle \mathbf{X}, \mathbf{B}_j \rangle = 0, \quad \forall j \\ & \langle \mathbf{X}, \mathbf{M}_{k} \rangle = 0, \quad \forall k \\ & \mathbf{X} \succeq 0 \end{aligned}$$ |

You can see these four optimization formulations at work in this Jupyter notebook:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/duembgen/notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F2025-08-25-sos-constrained-optimization.ipynb)

Now, let's look at how each of these is derived.

#### The Primal Kernel Form

We start with the central identity $p(x) - \gamma = \mathbf{v}(x)^\top \mathbf{X} \mathbf{v}(x) + t(x)g(x)$ and equate the coefficients of each monomial $x^i$ on both sides. The coefficient of $x^i$ in each term is:

*   On the left: $p_\alpha - \delta_{\alpha \mathbf{0}}\gamma$, where $p_\alpha$ is the coefficient of $p(x)$ corresponding to the multi-index $\alpha$ and $\delta_{\alpha\mathbf{0}}$ is 1 if $\alpha=\mathbf{0}$ and 0 otherwise.
*   In the SOS term: $\langle \mathbf{A}_i, \mathbf{X} \rangle$ (matrix $\mathbf{A}_i$ picks all the terms of the moment matrix corresponding to $x^\mathbf{\alpha}$.
*   We formulate matrices $\mathbf{C}_{ik}$ that will incorporate the equality constraints as follows. For each equality constraint $g_i(x)$ we form: $g\_i(x)t\_i(x) = \sum_k  t\_{ik} \langle\mathbf{C}\_{ik}, v(x)v(x)^\top\rangle$, where $t\_{ik}$ are the coefficients of the polynomial $t_i(x)$.

##### Example
We take as example a problem with two equality constraints: $g_1(x) = a^2 + b^2 - 1 = 0$, $g_2(x)=a-1=0$. We write the polynomial dual variables as 

$$
t_0(x) =t_0^{00} + t_0^{10} a + t_0^{01} b + t_0^{11} ab + \ldots
$$

First, we note that the degree of $t_0(x)$ is zero, the degree of $t_1(x)$ is one (since the total degree of each $g_i(x)t_i(x)$ should $\leq 2$. Plugging this in, we get:

$$
\begin{align}
\sum_{i=1}^{2} g_i(x)t_i(x) &= t_0^{00}(a^2 + b^2 - 1) + t_1^{00}(a - 1) + t_1^{10}a(a-1) + t_1^{01}b(a-1)  \\
& = \langle t_0^{00} \mathbf{C}_0^{00} + t_1^{00} \mathbf{C}_1^{00} + \ldots, v(x)v(x)^\top \rangle \\
\end{align}
$$

where the matrices $C_0^{00}$ to $C_{1}^{01}$ are given below:

GEMINI: fill this in.

Equating these gives a system of linear equations. This gives the **primal kernel** formulation:

$$
\textbf{(P-K)}\quad
\begin{align}
\max_{\mathbf{X}, \gamma, \mathbf{t}} \quad & \gamma \\
\text{s.t.} \quad & p_{\alpha} - \delta_{\alpha\mathbf{0}} \gamma = \langle \mathbf{A}_\alpha, \mathbf{X} \rangle + \sum_{k} t_k^{\alpha} \langle \mathbf{C}_k^{\alpha}, \mathbf{X}\rangle \quad \forall \alpha \\
& \mathbf{X} \succeq 0 
\end{align}
$$

#### The Primal Image Form

The **primal image** form finds a parameterization of $\mathbf{X}$ that will always satisfy the constraints. We have the following parameterization: 

$$
\mathbf{X} = \mathbf{Y}(\mathbf{p}) - \gamma \mathbf{A}_0 - \sum_j s_j \mathbf{N}_j
$$

where $\mathbf{N}_j$ are basis vectors of the nullspace of all operators $\mathbf{A}_\alpha$ and $\mathbf{C}_i^\alpha$. 

##### Example

For simplicity, we use the half-vecotrization operator to find the null space basis vectors. This consists of multiplying the off-diagonal elements by $\sqrt{2}$ so that $\mathrm{vech}(A)^top\mathrm{vech}{B}=\langle A, B \rangle$:

$$
\begin{bmatrix}
-1 & 0 & 0 & 1 & 0 & 1 \\
-1 & 1 & 0 & 0 & 0 & 0 \\
 0 &-1 & 0 & 1 & 0 & 0 \\
 0 & 0 &-1 & 0 & 1 & 0 \\
\end{bmatrix}
$$

We can find the nullspace of this constraint matrix to find the basis vectors $\mathbf{N}_j$. This matrix has rank 4, so its nullspace is 2-dimensional. Two basis vectors are:

$$
\mathbf{n}_1 = [1, 1, 0, 1, 0, 0]^\top, \quad \mathbf{n}_2 = [0, 0, 1, 0, 1, 0]^\top
$$

These vectors can be reshaped into symmetric matrices $\mathbf{N}_1, \mathbf{N}_2$ that form the basis for the homogeneous part of the solution.

$$
\textbf{(P-I)}\quad
\begin{align}
\max_{\mathbf{s}, \gamma, \mathbf{t}} \quad & \gamma \\
\text{s.t.} \quad & \mathbf{Y}(\mathbf{p}) - \gamma \mathbf{A}_0 - \sum_j s_j \mathbf{N}_j \succeq 0
\end{align}
$$

Of course. Here is a rewrite of the "Dual Problems" section with a derivation via the Lagrangian, as well as a revised conclusion.

***

### The Dual Problems

Every semidefinite program has a corresponding dual problem, which is derived from the Lagrangian of the primal problem. The dual often provides a different and powerful interpretation. For our constrained SOS problem, the dual reveals a deep connection to the theory of moments and probability distributions.

#### Derivation via the Lagrangian

To derive the dual, we start with the **primal kernel** formulation (P-K). The problem is:

$$
\begin{align}
\max_{\mathbf{X}, \gamma, \mathbf{t}} \quad & \gamma \\
\text{s.t.} \quad & p_{\alpha} - \delta_{\alpha\mathbf{0}} \gamma = \langle \mathbf{A}_\alpha, \mathbf{X} \rangle + \left(\sum_j t_j(x)g_j(x)\right)_\alpha \quad \forall \alpha \\
& \mathbf{X} \succeq 0
\end{align}
$$

where $(\cdot)\_\alpha$ denotes the coefficient of the monomial $x^\alpha$. We can write the linear term more explicitly. Let $t\_j(x) = \sum_\beta (t\_j)\_\beta x^\beta$. Then the coefficient of $x^\alpha$ in $\sum_j t\_j(x)g\_j(x)$ is $\sum_{j,\beta} (t\_j)\_\beta (x^\beta g\_j(x))\_\alpha$.

We introduce a Lagrange multiplier (a dual variable) $y_\alpha$ for each coefficient-matching constraint. The Lagrangian function is:

$$
L(\mathbf{X}, \gamma, \mathbf{t}; \mathbf{y}) = \gamma - \sum_\alpha y_\alpha \left( \langle \mathbf{A}_\alpha, \mathbf{X} \rangle + \sum_{j,\beta} (t_j)_\beta (x^\beta g_j(x))_\alpha + \delta_{\alpha\mathbf{0}}\gamma - p_\alpha \right)
$$

The dual problem is obtained by minimizing the dual function $g(\mathbf{y}) = \sup_{\mathbf{X}\succeq 0, \gamma, \mathbf{t}} L$ over the dual variables $\mathbf{y}$. To find this supremum, we rearrange the Lagrangian by grouping terms for the primal variables:

$$
\begin{align}
L = & \quad \gamma(1 - y_{\mathbf{0}}) \\
& - \sum_{j,\beta} (t_j)_\beta \left( \sum_\alpha y_\alpha (x^\beta g_j(x))_\alpha \right) \\
& - \left\langle \sum_\alpha y_\alpha \mathbf{A}_\alpha, \mathbf{X} \right\rangle \\
& + \sum_\alpha y_\alpha p_\alpha
\end{align}
$$

For the supremum to be finite, the terms multiplying the unconstrained variables $\gamma$ and $(t_j)_\beta$ must be zero. This gives us the first set of constraints for the dual problem:
1.  **From $\gamma$:** $1 - y_{\mathbf{0}} = 0 \implies y_{\mathbf{0}} = 1$.
2.  **From $t_j(x)$:** For each coefficient $(t\_j)\_\beta$, its multiplier must be zero: $\sum_\alpha y_\alpha (x^\beta g_j(x))_\alpha = 0$. This must hold for all $j$ and all basis multi-indices $\beta$ of the multiplier polynomial $t_j(x)$.

The supremum over $\mathbf{X} \succeq 0$ of $-\langle \sum\_\alpha y\_\alpha \mathbf{A}\_\alpha, \mathbf{X} \rangle$ is finite only if the matrix $\sum\_\alpha y\_\alpha \mathbf{A}\_\alpha$ is positive semidefinite. This gives the main constraint:
3.  **From $\mathbf{X}$:** $\mathbf{M}(\mathbf{y}) := \sum\_\alpha y\_\alpha \mathbf{A}\_\alpha \succeq 0$. This is the famous **moment matrix**.

With these conditions met, the Lagrangian simplifies to $\sum\_\alpha y\_\alpha p\_\alpha$. The dual problem is to minimize this value.

#### The Dual Kernel (Moment) Form

The derivation above leads directly to the **dual kernel** or **moment** formulation. The variables $y\_\alpha$ are interpreted as moments of a hypothetical probability distribution.

$$
\textbf{(D-K)}\quad
\begin{align}
\min_{\mathbf{y}} \quad & \sum_\alpha y_\alpha p_\alpha \\
\text{s.t.} \quad & y_\mathbf{0} = 1 \\
& \mathbf{M}(\mathbf{y}) \succeq 0 \\
& \sum_\alpha y_\alpha (x^\beta g_j(x))_\alpha = 0 \quad \forall j, \beta
\end{align}
$$

Let's interpret these constraints in the language of moments. The vector $\mathbf{y}$ defines a linear functional $L\_\mathbf{y}$ that maps a polynomial $q(x) = \sum q\_\alpha x^\alpha$ to its "expected value" $L\_\mathbf{y}(q) = \sum q\_\alpha y\_\alpha$.
1.  The objective is to minimize the expected value of our cost polynomial $p(x)$.
2.  $y\_\mathbf{0} = 1$ is a normalization, meaning the expected value of the polynomial $1$ is $1$.
3.  $\mathbf{M}(\mathbf{y}) \succeq 0$ is the moment matrix condition. Its $(i,k)$-th entry is $y\_{\alpha\_i+\alpha\_k}$, where $x^{\alpha\_i}$ and $x^{\alpha\_k}$ are monomials from the basis $\mathbf{v}(x)$. This condition ensures that the functional is non-negative on any SOS polynomial.
4.  The final constraint, which can be written as $\sum\_\delta (g\_j)\_\delta y\_{\beta+\delta} = 0$, is a "localizing" condition. It means that the expected value of any polynomial multiple of a constraint $g\_j(x)$ is zero (i.e., $L\_\mathbf{y}(h(x)g\_j(x))=0$). This forces the underlying measure to be supported only on the set where $g\_j(x)=0$.

#### The Dual Image Form

By taking the dual of the **primal image** form (P-I), we arrive at the **dual image** formulation. The dual variable is now a positive semidefinite matrix $\mathbf{Z}$ of the same size as $\mathbf{X}$. The constraints of the primal image form, which involve the nullspace vectors $\mathbf{N}\_j$ and the particular solution $\mathbf{Y}(\dots)$, translate directly into constraints on $\mathbf{Z}$.

$$
\textbf{(D-I)}\quad
\begin{align}
\min_{\mathbf{Z}} \quad & \langle \mathbf{Y(p)}, \mathbf{Z} \rangle \\
\text{s.t.} \quad & \langle \mathbf{Y_0}, \mathbf{Z} \rangle = 1 \\
& \langle \mathbf{Z}, \mathbf{N}_j \rangle = 0 \quad \forall j \\
& \langle \mathbf{Y}_{j,\beta}, \mathbf{Z} \rangle = 0 \quad \forall j, \beta \\
& \mathbf{Z} \succeq 0
\end{align}
$$

Here, $\mathbf{Y(p)}$, $\mathbf{Y\_0}$, and $\mathbf{Y}\_{j,\beta}$ are specific symmetric matrices (particular solutions) that represent the polynomials $p(x)$, the constant $1$, and the basis polynomials for the multiplier term $x^\beta g\_j(x)$, respectively. For example, $\mathbf{Y(p)}$ is any matrix satisfying $\langle \mathbf{A}\_\alpha, \mathbf{Y(p)} \rangle = p\_\alpha$ for all $\alpha$.

The constraints have a clear geometric interpretation in the space of symmetric matrices:
1.  The objective minimizes the inner product of $\mathbf{Z}$ with the matrix representing the cost polynomial.
2.  The constraints $\langle \mathbf{Z}, \mathbf{N}\_j \rangle = 0$ force $\mathbf{Z}$ to lie in the subspace orthogonal to the nullspace of the coefficient-matching map (i.e., in its image space).
3.  The constraints $\langle \mathbf{Y}\_{j,\beta}, \mathbf{Z} \rangle = 0$ enforce the same moment-like conditions from the dual kernel form, but now expressed in terms of the matrix $\mathbf{Z}$.

### Conclusion

We have extended the sum-of-squares framework for unconstrained optimization to handle polynomial equality constraints using a result from real algebraic geometry known as the Positivstellensatz. By introducing multiplier polynomials, we can again formulate the search for a global lower bound as a semidefinite program.

This single problem can be viewed from four different perspectives, forming a complete primal-dual picture:
*   **Primal Kernel:** Find an SOS polynomial and multiplier coefficients. The constraints are on the coefficients of the polynomials.
*   **Primal Image:** Find an SOS polynomial by parameterizing the space of all feasible polynomials. The constraint is a single linear matrix inequality.
*   **Dual Kernel (Moment):** As derived via the Lagrangian, this form seeks an optimal "pseudo-measure" or moment sequence $\mathbf{y}$ that is supported on the constraint set.
*   **Dual Image:** Find an optimal positive semidefinite moment matrix $\mathbf{Z}$ that lies within a specific subspace defined by the problem's constraints.

Under mild assumptions (strong duality holds), these four formulations are equivalent. However, one may be more efficient or insightful than another depending on the specific problem structure. This primal-dual framework is the foundation of the powerful Lasserre hierarchy, which provides a sequence of increasingly accurate SDP relaxations that converge to the true global minimum of a polynomial optimization problem.


### Conclusion


### References / further reading

The Moment-SOS hierarchy is a cornerstone of modern polynomial optimization. Foundational references include:
{% cite parrilo_semidefinite_2003 %}
{% cite lasserre_global_2001 %}

### Bibliography

{% bibliography %}
