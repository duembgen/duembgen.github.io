---
layout: post
title: "KIPD: Navigating Formulations for SOS Feasibility"
date: 2025-08-18
categories: [research]
---

_I finally got around to writing my first blogpost, thanks to LLMs. This blogpost is not just AI-generated, but thanks to the latest and greatest LLM magic, the time to go from handwritten notes to a polished blogpost was greatly reduced. For full transparency, and maybe because others might find this interesting, I am writing [another blogpost](/misc/2025/08/18/blog-posts-in-2025.html) about my process to generated this blogpost (and hopefully a few more in the future) using Gemini._

Checking if a polynomial is non-negative is a fundamental problem that appears in many areas of engineering and mathematics. While checking for non-negativity is computationally hard in general, a powerful sufficient condition is to check if the polynomial can be written as a sum of squares (SOS) of other polynomials. This condition is not only tractable—it can be checked by solving a semidefinite program (SDP)—but it is also a key component in a wide range of optimization methods for polynomial systems.

In this post, we'll explore how to formulate the SOS problem as an SDP. We will see that there isn't just one way to do it. We'll look at two primary approaches, often called the "kernel form" and the "image form," and then explore their dual problems. This will give us four different, but related, optimization problems for tackling the same question.

My motivation to write this blogpost was the misconception I had about this topic. I recently watched a nice [talk](https://www.youtube.com/watch?v=CGPHaHxCG2w&t=815s) that helped me uncover this misconception: one can solve a SOS problem in kernel *or* in image form, *and* in dual *or* primal form -- so there are really 4 options. In my head, the lines between the dual/image and primal/kernel, respectively, were kind of blurred. 

### A Quick Overview

Checking if a polynomial is a sum of squares (SOS) can be formulated as a semidefinite programming (SDP) feasibility problem. There are four common ways to frame this problem, arising from two primal perspectives (Kernel and Image) and their corresponding duals. The table below presents the general form of each of these four formulations.

| | **Kernel Form** | **Image Form** |
|:---|:---|:---|
| **Primal** | **(P-K) Primal Kernel Problem** <br> Find a Gram matrix $\mathbf{X}$ that satisfies linear coefficient-matching constraints. <br><br> $$\begin{aligned} \text{find} \quad & \mathbf{X} \\ \text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_i \rangle = p_i, \quad \forall i \\ & \mathbf{X} \succeq 0 \end{aligned}$$ | **(P-I) Primal Image Problem** <br> Find slack variables $\mathbf{s}$ that make the parameterized Gram matrix positive semidefinite. <br><br> $$\begin{aligned} \text{find} \quad & \mathbf{s} \\ \text{s.t.} \quad & \mathbf{Y}(\mathbf{p}) + \sum_{j} s_j \mathbf{B}_j \succeq 0 \end{aligned}$$ |
| **Dual** | **(D-K) Dual Kernel Problem** <br> Maximize a linear function of the coefficients subject to a linear matrix inequality. <br><br> $$\begin{aligned} \max_{\boldsymbol{\lambda}} \quad & -\sum_i \lambda_i p_i \\ \text{s.t.} \quad & \sum_i \lambda_i \mathbf{A}_i \succeq 0 \end{aligned}$$ | **(D-I) Dual Image Problem** <br> Maximize an inner product subject to orthogonality constraints. <br><br> $$\begin{aligned} \max_{\mathbf{X}} \quad & -\langle \mathbf{X}, \mathbf{Y}(\mathbf{p}) \rangle \\ \text{s.t.} \quad & \langle \mathbf{X}, \mathbf{B}_j \rangle = 0, \quad \forall j \\ & \mathbf{X} \succeq 0 \end{aligned}$$ |

You can see these four formulations at work in this simple Jupyter notebook: 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/duembgen/notebooks/HEAD?urlpath=%2Fdoc%2Ftree%2F2025-08-18-kernel-image-primal-dual.ipynb)

Now, let's dive into the details of where each of these formulations comes from.

### The Primal Problems

A polynomial $p(x)$ is a sum of squares if and only if it can be written in the form
$$ p(x) = \mathbf{v}(x)^\top \mathbf{X} \mathbf{v}(x) $$
for some positive semidefinite matrix $\mathbf{X} \succeq 0$, called the Gram matrix, and where $\mathbf{v}(x)$ is a vector of monomials.

Our goal is to find such a matrix $\mathbf{X}$. Let's consider a simple example to make things concrete: a univariate polynomial of degree 4.
$$ p(x) = p_0 + p_1x + p_2x^2 + p_3x^3 + p_4x^4 $$
The monomial basis vector is $\mathbf{v}(x) = [1, x, x^2]^\top$. The Gram matrix $\mathbf{X}$ will be a $3 \times 3$ symmetric matrix. The condition $p(x) = \mathbf{v}(x)\top \mathbf{X} \mathbf{v}(x)$ can be expanded and written as an inner product:
$$ p(x) = \langle \mathbf{X}, \mathbf{v}(x)\mathbf{v}(x)\top \rangle $$
By matching the coefficients of the powers of $x$ on both sides, we get a system of linear equations that our matrix $\mathbf{X}$ must satisfy.

#### The Primal Kernel Form

The most direct approach is to write these linear equations as constraints in an optimization problem. This is the **kernel form**, as it describes the feasible set as the kernel of a linear operator.

For our example, matching coefficients yields:
*   $p_0 = X_{00}$
*   $p_1 = 2X_{01}$
*   $p_2 = 2X_{02} + X_{11}$
*   $p_3 = 2X_{12}$
*   $p_4 = X_{22}$

This gives us a feasibility problem in the primal kernel form:

$$
\textbf{(P-K)}\quad
\begin{align}
\text{find} \quad & \mathbf{X} \\
\text{s.t.} \quad & \langle \mathbf{X}, \mathbf{A}_i \rangle = p_i, \quad i=0, \dots, 4 \\
& \mathbf{X} \succeq 0
\end{align}
$$

Here, the matrices $\mathbf{A}_i$ are cleverly chosen to pick out the right elements of $\mathbf{X}$ to match the coefficients $p_i$. 
They are given by:

$$
\mathbf{A}_0 = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad
\mathbf{A}_1 = \begin{pmatrix} 0 & 1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}, \quad
\mathbf{A}_2 = \begin{pmatrix} 0 & 0 & 1 \\ 0 & 1 & 0 \\ 1 & 0 & 0 \end{pmatrix}
$$

$$
\mathbf{A}_3 = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 1 & 0 \end{pmatrix}, \quad
\mathbf{A}_4 = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$


#### The Primal Image Form

An alternative is the **image form**. Instead of defining the valid matrices $\mathbf{X}$ by what constraints they must satisfy, we provide a direct parameterization for any valid $\mathbf{X}$.

Notice that our system of 5 linear equations has 6 variables (the unique entries of the symmetric matrix $\mathbf{X}$). This means there is one degree of freedom. We can introduce a "slack" variable, let's call it $s$, to parameterize all possible solutions. A bit of algebra shows that any valid Gram matrix $\mathbf{X}$ can be written as:

$$
\mathbf{X} =
\begin{bmatrix}
p_0 & p_1/2 & -s/2 \\
p_1/2 & p_2+s & p_3/2 \\
-s/2 & p_3/2 & p_4
\end{bmatrix}
$$

This can be expressed as $\mathbf{X} = \mathbf{Y}(\mathbf{p}) + s \mathbf{B}_1$, where $\mathbf{Y}(\mathbf{p})$ is the matrix containing the parameters $\mathbf{p}$, and $\mathbf{B}_1$ is a matrix that adds the slack term. The problem is then to find if there *exists* a slack variable $s$ that makes this matrix positive semidefinite.

$$
\textbf{(P-I)}\quad
\begin{align}
\text{find} \quad & s \\
\text{s.t.} \quad & \mathbf{Y}(\mathbf{p}) + s \mathbf{B}_1 \succeq 0
\end{align}
$$

The matrix $\mathbf{B}_1$ is a matrix from the null space of the linear operator that maps a Gram matrix to its polynomial coefficients, meaning $\langle \mathbf{B}_1, \mathbf{v}(x)\mathbf{v}(x)\top \rangle = 0$. For our example, this matrix is:

$$
\mathbf{B}_1 = \begin{pmatrix} 0 & 0 & -1/2 \\ 0 & 1 & 0 \\ -1/2 & 0 & 0 \end{pmatrix}
$$

You can verify that adding any multiple $s \mathbf{B}_1$ to a valid Gram matrix $\mathbf{X}$ produces another valid Gram matrix that generates the exact same polynomial $p(x)$, as all the new terms cancel out in the coefficient matching equations.

For more complex polynomials, we might have multiple slack variables, leading to a more general constraint:

$$
\mathbf{Y}(\mathbf{p}) + \sum_j s_j \mathbf{B}_j \succeq 0.
$$

> Now here is the main source of confusion, and the reason I wanted to write this blog post. For someone having looked a lot at SDP programs, problem (P-I) looks a lot like the dual of (P-K). Is it just the dual problem? As it turns out, no.

### The Dual Problems

Every optimization problem has a dual, which provides deep insights and often alternative solution methods. Let's find the duals of our two primal forms.

#### Dual of the Kernel Form

Starting with the primal kernel problem (P-K), we can form its Lagrangian and derive the dual problem. The derivation is standard, and provided in the [Appendix](#derivation-of-the-dual-problem). Calling the dual variables of the linear constraints $\lambda_i$, we obtain the dual optimization problem:

$$
\textbf{(D-K)}\quad
\begin{align}
\max_{\boldsymbol{\lambda}} \quad & -\sum_{i=0}^4 \lambda_i p_i \\
\text{s.t.} \quad & \sum_{i=0}^4 \lambda_i \mathbf{A}_i \succeq 0
\end{align}
$$

For our example, the matrix in the constraint, $\sum \lambda_i \mathbf{A}_i$, turns out to be a beautiful and structured matrix—a Hankel matrix:

$$
\sum_{i=0}^4 \lambda_i \mathbf{A}_i =
\begin{bmatrix}
\lambda_0 & \lambda_1 & \lambda_2 \\
\lambda_1 & \lambda_2 & \lambda_3 \\
\lambda_2 & \lambda_3 & \lambda_4
\end{bmatrix} \succeq 0
$$

By strong duality, the primal problem (P-K) is feasible if and only if the optimal value of this dual problem (D-K) is 0. If (P-K) is infeasible, (D-K) will be unbounded. In particular, we can derive a simple feasibility problem to get a certificate of (in)feasibility, as derived next. 

Let's take a closer look at the dual problem (D-K) and its relationship with the primal. The dual problem has two possible outcomes. First, if for every feasible $\boldsymbol{\lambda}$ we have $-\sum_i \lambda_i p_i \le 0$, then the optimal value of the dual is 0. This is because $\boldsymbol{\lambda} = \mathbf{0}$ is always a feasible point (since $ \sum 0 \cdot \mathbf{A}_i = \mathbf{0} \succeq 0$) and yields an objective value of 0. On the other hand, if there exists even one feasible $ \boldsymbol{\lambda}^{\star} $ for which $-\sum_i \lambda_i p_i > 0$, 
then the dual problem is unbounded. This is because the feasible set is a cone, so any positive multiple $\alpha \boldsymbol{\lambda}^\star $ is also feasible, and we can make the objective $\alpha(-\sum_i \lambda_i p_i)$ arbitrarily large.

By strong duality, these two outcomes correspond directly to the feasibility of the primal problem (P-K):

*   If **(P-K) is feasible**, its optimal value is 0, so the dual optimal value must also be 0.
*   If **(P-K) is infeasible**, the dual problem must be unbounded.

This gives us a practical way to check for primal infeasibility. Instead of solving the dual optimization problem, we can check for its unboundedness by solving a related feasibility problem. Specifically, we can ask: "Does there exist a feasible $\boldsymbol{\lambda}$ that achieves any strictly positive objective value, for instance, $\varepsilon > 0$?" This leads to the dual feasibility formulation:

$$
\textbf{(Df-K)}\quad
\begin{align*}
\text{find} \quad & \boldsymbol{\lambda} \\
\text{s.t.} \quad & \sum_{i=0}^4 \lambda_i p_i = -\varepsilon \\
& \sum_{i=0}^4 \lambda_i \mathbf{A}_i \succeq 0
\end{align*}
$$

If this problem is feasible for any $\varepsilon > 0$, it serves as a certificate that the dual (D-K) is unbounded and, therefore, that the original primal problem (P-K) is infeasible.




Now let us compare (D-K) to the [Primal Image Form](#the-primal-image-form) and problem (P-I). The variables seem related, but they are fundamentally different problems. For instance, if we try to set the variables $\lambda_i$ according to the entries of the parameterized Gram matrix from (P-I), such as $\lambda_0=p_0$, $\lambda_1=p_1/2$, etc., we find they do not generally provide a feasible (let alone optimal) solution to (D-K).

> This confirms that (P-K) is not simply the dual of (P-I). 

#### Dual of the Image Form

For completeness, let's find the dual of the primal image problem (P-I). The dual variable here will be a matrix, which we'll call $\mathbf{X}$ (as it lives in the same space as our original primal variable). The derivation leads to the following dual optimization problem:

$$
\textbf{(D-I)}\quad
\begin{align}
\max_{\mathbf{X}} \quad & -\langle \mathbf{Y}(\mathbf{p}), \mathbf{X} \rangle \\
\text{s.t.} \quad & \langle \mathbf{B}_1, \mathbf{X} \rangle = 0  \\
& \mathbf{X} \succeq 0
\end{align}
$$

This dual problem seeks to maximize $-\langle \mathbf{Y}(\mathbf{p}), \mathbf{X} \rangle$ over all positive semidefinite matrices $\mathbf{X}$ that are orthogonal to the basis of the null space, $\mathbf{B}_1$. Again, the primal (P-I) is feasible if and only if the optimal value of this dual is 0.  The same analysis as for the kernel form applies here to derive a simple feasibility problem for any value $\epsilon > 0$: 

$$
\textbf{(Df-I)}\quad
\begin{align}
\text{find} \quad & \mathbf{X} \\
\text{s.t.} \quad & \langle \mathbf{Y}(\mathbf{p}), \mathbf{X} \rangle = -\epsilon\\
& \langle \mathbf{B}_1, \mathbf{X} \rangle = 0  \\
& \mathbf{X} \succeq 0
\end{align}
$$



### Conclusion

The choice between the different forms can have practical consequences. For a polynomial with few variables but high degree (small $n$, large $d$), the kernel form is often more efficient as it avoids parameterizing a potentially high-dimensional affine space. Conversely, for many variables and low degree (large $n$, small $d$), the image form can be simpler as there are fewer, or even no, slack variables. 

### Appendix 

#### Derivation of the Dual Problem

To derive the dual of the kernel formulation, we begin with the primal problem (P-K). Since it's a feasibility problem, we can think of it as minimizing a zero objective function. We introduce a vector of Lagrange multipliers $\boldsymbol{\lambda}$ for the linear equality constraints $\langle \mathbf{A}_i, \mathbf{X} \rangle = p_i$, and a positive semidefinite matrix multiplier $\mathbf{H} \succeq 0$ for the cone constraint $\mathbf{X} \succeq 0$. The Lagrangian $\mathcal{L}(\mathbf{X}, \boldsymbol{\lambda}, \mathbf{H})$ is formed by adding the constraints to the objective:

$$
\mathcal{L}(\mathbf{X}, \boldsymbol{\lambda}, \mathbf{H}) = 0 + \sum_{i} \lambda_i (p_i - \langle \mathbf{A}_i, \mathbf{X} \rangle) - \langle \mathbf{H}, \mathbf{X} \rangle
$$

The dual problem involves maximizing the *Lagrange dual function*, which we find by minimizing the Lagrangian with respect to the primal variable $\mathbf{X}$. Let's group the terms involving $\mathbf{X}$:

$$
\mathcal{L}(\mathbf{X}, \boldsymbol{\lambda}, \mathbf{H}) = -\left\langle \sum_{i} \lambda_i \mathbf{A}_i + \mathbf{H}, \mathbf{X} \right\rangle + \sum_{i} \lambda_i p_i
$$

This expression is linear in $\mathbf{X}$. For its minimum over the cone of positive semidefinite matrices to be bounded (i.e., not $-\infty$), the matrix multiplying $\mathbf{X}$ must be zero, which gives us the condition $\sum_i \lambda_i \mathbf{A}_i + \mathbf{H} = \mathbf{0}$. If this holds, the Lagrangian simplifies to $\sum_i \lambda_i p_i$. The dual problem is to maximize this value subject to the conditions on the dual variables:

$$
\begin{align}
\max_{\boldsymbol{\lambda}, \mathbf{H}} \quad & \sum_i \lambda_i p_i \\
\text{s.t.} \quad & \sum_i \lambda_i \mathbf{A}_i + \mathbf{H} = \mathbf{0} \\
& \mathbf{H} \succeq 0
\end{align}
$$

We can eliminate $\mathbf{H}$ by substituting $\mathbf{H} = -\sum_i \lambda_i \mathbf{A}_i$. The constraint $\mathbf{H} \succeq 0$ then becomes $-\sum_i \lambda_i \mathbf{A}_i \succeq 0$. Multiplying the objective and the constraint by -1 (which turns the maximization into a minimization and flips the inequality) gives an equivalent problem. For consistency with the table, we'll stick to the maximization form:

$$
\begin{align}
\max_{\boldsymbol{\lambda}} \quad & -\sum_i \lambda_i p_i \\
\text{s.t.} \quad & \sum_i \lambda_i \mathbf{A}_i \succeq 0
\end{align}
$$

### References / further reading

The topic of kernel vs. image form and dual vs. primal problems, are discussed, for example, in {% cite parrilo_semidefinite_2003 %}, Section 6. As mentioned earlier, the motivation of this post was actually this [talk](https://www.youtube.com/watch?v=CGPHaHxCG2w&t=815s), where the topic is also discussed briefly. 

### Bibliography

{% bibliography %}
