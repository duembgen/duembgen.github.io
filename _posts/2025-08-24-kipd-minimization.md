---
layout: post
title: "KIPD: From Feasibility to Unconstrained Minimization"
date: 2025-08-24
categories: [research]
---

_Note from November 3rd 2025: The concepts of this blogpost are better described in the [more recent post](/research/2025/10/27/subspaces.html)_

_This is a follow-up to my [previous post](/research/2025/08/18/kernel-image-primal-dual.html) on different formulations (Kernel, Image, Primal, Dual) of Sum-of-Squares (SOS) feasibility problems. This post took significantly less time to write because it is really an evolution of the previous post, which Gemini is amazingly good at. I added a paragraph about this in [other post](/misc/2025/08/18/blog-posts-in-2025.html) about writing blog-posts with the helpf of Gemini_


In the last post, we explored how to determine if a polynomial $p(x)$ can be written as a sum of squares. This is a powerful tool for certifying that a polynomial is non-negative. But what if we want to find the *global minimum* of a polynomial? With only a few changes to the optimization problems, we can use SOS techniques to solve this, or at least find a good lower bound. 

The starting point is the following problem: $\min_x p(x)$. Any problem of this form can be reformulated as follows: 

$$
\begin{aligned}
\max_{\gamma} \quad & \gamma \\
\text{s.t.} \quad & p(x) - \gamma \geq 0 \quad \forall x, \\
\end{aligned}
$$

i.e. we find the largest value $\gamma$ that lower-bounds $p(x)$. This is, in general, just as hard as our original problem. However, we can use the restriction that the shifted polynomial $p(x) - \gamma$ is a sum of squares. Gor univariate polynomials, this is an exact reformulation; for multivariate polynomials, it provides a lower bound to the optimal cost.  Thus we aim to solve:

$$
\begin{aligned}
\textbf{(SOS-opt)}\quad\max_{\gamma, \mathbf{X}} \quad & \gamma \\
\text{s.t.} \quad & p(x) - \gamma = \mathbf{v}(x)^\top \mathbf{X} \mathbf{v}(x) \\
& \mathbf{X} \succeq 0
\end{aligned}
$$

Just like the feasibility problem, this SOS optimization problem, which we will call \textbf{SOS-opt} is a semidefinite program (SDP). And just like before, there are four related ways to formulate it: the Primal-Kernel, Primal-Image, Dual-Kernel, and Dual-Image form.

### A Quick Overview

The problem of maximizing $\gamma$ such that $p(x) - \gamma$ is SOS can be formulated as an SDP in four ways. The key difference from the feasibility problem is that $\gamma$ is now an optimization variable, and the objective is no longer zero. The constant term of the polynomial, $p_0$, is now $p_0 - \gamma$. This small change propagates through all four formulations.

| | **Kernel Form** | **Image Form** |
|:---|:---|:---|
| **Primal** | **(P-K) Primal Kernel Problem** <br> Maximize $\gamma$ subject to linear coefficient-matching constraints on the Gram matrix $\mathbf{X}$. <br><br> $$\begin{aligned} \max_{\mathbf{X}, \gamma} \quad & \gamma \\ \text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_0 \rangle + \gamma = p_0 \\ & \langle \mathbf{X}, \mathbf{A}_i \rangle = p_i, \quad \forall i>0 \\ & \mathbf{X} \succeq 0 \end{aligned}$$ | **(P-I) Primal Image Problem** <br> Maximize $\gamma$ subject to a parameterized Gram matrix being positive semidefinite. <br><br> $$\begin{aligned} \max_{\mathbf{s}, \gamma} \quad & \gamma \\ \text{s.t.} \quad & \mathbf{Y}(\mathbf{p}) - \gamma \mathbf{A}_0 + \sum_{j} s_j \mathbf{B}_j \succeq 0 \end{aligned}$$ |
| **Dual** | **(D-K) Dual Kernel Problem** <br> Minimize a linear function of the polynomial's coefficients. <br><br> $$\begin{aligned} \min_{\boldsymbol{\lambda}} \quad & \sum_i \lambda_i p_i \\ \text{s.t.} \quad & \sum_i \lambda_i \mathbf{A}_i \succeq 0 \\ & \lambda_0 = 1 \end{aligned}$$ | **(D-I) Dual Image Problem** <br> Minimize an inner product subject to normalization and orthogonality constraints. <br><br> $$\begin{aligned} \min_{\mathbf{X}} \quad & \langle \mathbf{X}, \mathbf{Y}(\mathbf{p}) \rangle \\ \text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_0 \rangle = 1 \\ & \langle \mathbf{X}, \mathbf{B}_j \rangle = 0, \quad \forall j \\ & \mathbf{X} \succeq 0 \end{aligned}$$ |

You can see these four optimization formulations at work in this Jupyter notebook:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/duembgen/notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F2025-08-25-sos-optimization-primal-dual.ipynb)

Now, let's look at how each of these is derived.

#### The Primal Kernel Form

The primal formulation starts from $\textbf{(SOS-opt)}$ and simply matches coefficients between the left-hand and right-hand sides of the equality constraints  $p(x) - \gamma = v(x)^\top X v(x)$.

For the running example from the previous blogpost, a univariate polynomial of degree 4 with $v(x) = [1, x, x²]^\top$, the constraints are:
*   $p_0 - \gamma = X_{00}$
*   $p_1 = 2X_{01}$
*   $p_2 = 2X_{02} + X_{11}$
*   $p_3 = 2X_{12}$
*   $p_4 = X_{22}$

Note that these equations are almost identical to the ones in the feasibility problem, only the first element and cost function now contain $\gamma$. 

The most direct approach is to make $\gamma$ and the entries of $X$ our optimization variables. This gives the **primal kernel** formulation.

$$
\textbf{(P-K)}\quad
\begin{align}
\max_{\mathbf{X}, \gamma} \quad & \gamma \\
\text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_0 \rangle + \gamma = p_0 \\
& \langle \mathbf{X}, \mathbf{A}_i \rangle = p_i, \quad i=1, \dots, 4 \\
& \mathbf{X} \succeq 0
\end{align}
$$

The matrices $A_i$ are the same as in the feasibility problem, used to extract the correct combinations of elements from $X$. This is an SDP where we are maximizing $\gamma$ over the set of feasible Gram matrices.

#### The Primal Image Form

The **primal image** form again parameterizes the space of all valid Gram matrices. Any $\mathbf{X}$ satisfying the coefficient-matching equations for $p(x) - \gamma$ can be written as:

$$
\mathbf{X} = \mathbf{Y}(\mathbf{p}) - \gamma \mathbf{A}_0 + \sum_j s_j \mathbf{B}_j
$$

Here, $\mathbf{Y}(\mathbf{p})$ is the same matrix as in the feasibility problem, constructed from the coefficients of the original polynomial $p(x)$. Again, the problem is exactly the same as for the feasibility case, only that the $-\gamma \mathbf{A}_0$ term adjusts the constant coefficient. The $\mathbf{B}_j$ matrices span the null space of the feasible set, as before.

The optimization problem is to find the largest $\gamma$ for which there exist slack variables $s_j$ that make this matrix positive semidefinite.

$$
\textbf{(P-I)}\quad
\begin{align}
\max_{\mathbf{s}, \gamma} \quad & \gamma \\
\text{s.t.} \quad & \mathbf{Y}(\mathbf{p}) - \gamma \mathbf{A}_0 + \sum_j s_j \mathbf{B}_j \succeq 0
\end{align}
$$

> For people familiar with the QCQP + rank-relaxation approach (a.k.a. Shor's relaxation): this problem is exactly the dual of the rank realxation! In particular, $\mathbf{Y}(\mathbf{p})$ is the cost matrix -- in other words, $p(x)=v(x)^\top\mathbf{Y}(\mathbf{p})v(x)$. 

### The Dual Problems

We assume that strong duality duality holds for these SDPs, meaning the optimal value of the dual problem will be equal to the optimal $\gamma$ of the primal problem.

#### Dual of the Kernel Form

Taking the Lagrangian dual of the Primal Kernel problem (P-K) yields the **Dual Kernel** formulation. We introduce dual variables $\lambda_i$ for each of the linear constraints. The derivation (similar to the one in the appendix of the previous post) leads to a remarkably structured problem:

$$
\textbf{(D-K)}\quad
\begin{align}
\min_{\boldsymbol{\lambda}} \quad & \sum_{i=0}^4 \lambda_i p_i \\
\text{s.t.} \quad & \sum_{i=0}^4 \lambda_i \mathbf{A}_i \succeq 0 \\
& \lambda_0 = 1
\end{align}
$$

This problem minimizes a linear combination of the original polynomial's coefficients, subject to an semidefinite constraint and a normalization constraint $\lambda_0 = 1$. 

<!--This dual formulation is particularly elegant because it connects to the theory of moments and positive polynomials. The vector $\lambda$ can be interpreted as a vector of pseudo-moments.-->

#### Dual of the Image Form

Finally, the dual of the Primal Image problem (P-I) gives us the **Dual Image** formulation:

$$
\textbf{(D-I)}\quad
\begin{align}
\min_{\mathbf{X}} \quad & \langle \mathbf{X}, \mathbf{Y}(\mathbf{p}) \rangle \\
\text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_0 \rangle = 1 \\
& \langle \mathbf{X}, \mathbf{B}_j \rangle = 0 \quad \forall j \\
& \mathbf{X} \succeq 0
\end{align}
$$

> Note that this is exactly the same optimization problem as we get through Shor's relaxation (after adding all redundant constraints). Maybe confusingly, it is often referred to as the Primal problem in that context. This is not surprising since we already made the observation that the Primal-Image form looks like the dual in those formulations. 

#### Tangent: Shor's relaxation

As noted above, problem **(D-I)** is identitcal to Shor's relaxation. To see, this we derive Shor's relaxation here. We start by rewriting our original problem as the following QCQP:

$$
\begin{aligned}
\min_x \quad & \mathbf{x}^\top \mathbf{Y}(\mathbf{p}) \mathbf{x} \\
\text{s.t.} \quad & \mathbf{x}^\top \mathbf{A}_0 \mathbf{x} = 1 \\
                  & \mathbf{x}^\top \mathbf{B}_j \mathbf{x} = 0 \quad \forall j
\end{aligned}
$$

where we have introduced $\mathbf{B}_j$ -- all matrices that span the null space of the feasible set. Those can be found by solving a nullspace problem, as formalized in the AutoTight method, or its variant AutoTemplate to scale to larger problem instances {% cite dumbgen_toward_2024 %}.

Shor's relaxation consists of introducing a new variable $\mathbf{X} = \mathbf{x}\mathbf{x}^\top$ and dropping the non-convex rank-1 constraint on $\mathbf{X}$. This gives us exactly **(D-I)**.

### Conclusion

By shifting from a feasibility problem to an optimization problem, we can use SOS methods to find guaranteed lower bounds on the global minimum of a polynomial. The four formulations—Primal-Kernel, Primal-Image, and their respective duals—all solve the same underlying problem but offer different computational and theoretical perspectives. Strong duality ensures that no matter which formulation you choose, you will arrive at the same optimal lower bound, $\gamma*$. The choice of which to implement often depends on the specific structure of the problem, such as the number of variables and the degree of the polynomial, which can affect the size and complexity of the resulting SDP.

### References / further reading

The topic of SOS optimization is a cornerstone of polynomial optimization. The formulations discussed here are detailed in many standard texts and tutorials on the subject. A foundational reference is:
{% cite parrilo_semidefinite_2003 %}

### Bibliography

{% bibliography %}
