# Implementation of Stochastic Decision

## Introduction

## Definition of Stochastic Decision
Here I will define this decision mathematically: $Q$ is a decision, yielding {0, 1}. $Q$ is a stochastic function of minimum number of data required $m$, DP loss allowed $\epsilon$, $\delta$, and total number of the data qualified for the application $N$. 

$$ Q_{m, \epsilon, \delta}(N) \in \{0, 1\} $$

$Q(N)$ will be used in the following for simplicity, because $m$, $\epsilon$, and $\delta$ are fixed input. Consider two neighbor dataset $x$ and $y$, and their number of data is $N$ and $N+1$, ($\epsilon, \delta$)-DP is defined to be

$$Pr(Q(N+1) = 1) \leq e^{\epsilon} Pr(Q(N) = 1) + \delta$$

$$Pr(Q(N) = 0) \leq e^{\epsilon} Pr(Q(N+1) = 0) + \delta$$

Since $Q(N)$ is a monotonic increasing given $N$, thus I don't have to consider the cases switching LHS and RHS of the above inequalities. Therefore, any stochastic query meeting these two inequalities is a qualified stochastic decision. In addition, to make the decision practically, one more constrain can be added:

$$Pr(Q(m) = 1) \geq \frac{1}{2},$$

which reflects the meaning of $m$. 


\begin{align}
    g &= \int_a^b f(x)dx \tag{1}\\
    a &= b + c 
\end{align}


## Theorems

**Theorem 1.** $x$ is a scalar variable, and $f(x)$ is a monotonically decreasing function. If 

\begin{align}
    f(a) - f(a + 1) \leq f(b) - f(b + 1), \tag{5}
\end{align}


and $a < b$, and that 


\begin{align}
   f(b) \leq m f(b+1) + n, \tag{6}
\end{align}

where $m \geq 1$ and $n \geq 0$, then


\begin{align}
   f(a) \leq m f(a+1) + n \tag{7}
\end{align}

is also guaranteed.


*Proof of Theorem 1.* 

Modify the Ineq. (6) as

\begin{align}
    f(b) - f(b+1) \leq (m - 1) f(b+1) + n. \tag{8}
\end{align}

Since $m - 1 \geq 0$ and $f(b+1) \leq f(a+1)$,

\begin{align}
    (m - 1) f(b+1) + n \leq (m - 1) f(a+1) + n. \tag{9}
\end{align}

Combine Ineq.(5), (8) and (9),

\begin{align}
    f(a) - f(a+1) \leq (m - 1) f(a+1) + n \tag{10} \\
    \Rightarrow f(a) \leq m f(a+1) + n. \tag{11}
\end{align}

**Lemma 1.** If $x$ is a scalar variable and $f(x)$ is a monotonically decreasing and derivable function, and that 

\begin{align}
    f'(a) \geq f'(b), \tag{12}
\end{align}

where $a + 1\leq b$, then Ineq. (7) can be derived from Ineq. (6).


*Proof of Lemma 1.* 

Given the Lagrange's Mean Value Theorem, 

\begin{align}
    f(a) - f(b) = f'(\xi)(a-b), \tag{13}
\end{align}

where $a < \xi < b$, and substitute with (a, a+1) and (b, b+1), respectively, then it becomes

\begin{align}
    f(a) - f(a+1) = -f'(\xi_{a}), \tag{14} \\
    f(b) - f(b+1) = -f'(\xi_{b}). \tag{15}
\end{align}

Given $a < \xi_{a} < a + 1 \leq b < \xi_{b} < b + 1$, Ineq. (12) becomes

\begin{align}
    -f'(\xi_{a}) \leq -f'(\xi_{b}) \tag{16}.
\end{align}

Combining Ineq. (14), (15), and (16) yields (5). Given Theorem 1., the lemma is proved.

## Sigmoid Implmentation


## Cutoff Exponential Implementation


$$ Pr(Q(m) = 1) = 1 $$

$$ Pr(Q(N) = 1) = e^{\epsilon} Pr(Q(N - 1) = 1) $$

Given $N <= m$,

$$ Pr(Q(N) = 1) = e^{\epsilon (N - m)}$$

$$ Pr(Q(N) = 0) = 1 - e^{\epsilon (N - m)}$$

Apparently, 


$$Pr(Q(N+1) = 1) \leq e^{\epsilon} Pr(Q(N) = 1) + 1 - e^{-\epsilon}$$

is always True by the definition. Switching LHS and RHS is also correct, because $Pr(Q(N) = 1)$ is always smaller than $Pr(Q(N + 1) = 1)$.

Now the question becomes proving the correctness of

\begin{align}
    Pr(Q(N) = 0) \leq e^{\epsilon} Pr(Q(N+1) = 0) + 1 - e^{-\epsilon}.
\end{align}

First, let's prove 

\begin{align}
    Pr(Q(m - 1) = 0) \leq e^{\epsilon} Pr(Q(m) = 0) + 1 - e^{-\epsilon}.
\end{align}

LHS = $1 - e^{-\epsilon}$ and RHS = $e^{\epsilon} * 0 + 1 - e^{-\epsilon} = 1 - e^{-\epsilon}$, so LHS = RHS, and (X) is proved.


Given $Pr(Q(N) = 0)$ is a monotonically decreasing, and (X), if we can prove 

\begin{align}
    \frac{d}{dx}Pr(Q(x=a) = 0) \geq \frac{d}{dx}Pr(Q(x=b) = 0),
\end{align}

where $a + 1 \leq b$, then the Lemma 1. could lead to the correctness of Ineq. (X).

For simplicity, define $f(x) = Pr(Q(x) = 0)$, then

\begin{align}
    f'(x) = \frac{d}{dx} (1 - e^{\epsilon (x - m)}),\\
    \Rightarrow f'(x) = - e^{-\epsilon m} \frac{d}{dx}  e^{\epsilon x} = - e^{-\epsilon m} \epsilon e^{\epsilon x}.\\
\end{align}

Since $f'(x)$ is apparently a monotonically decreasing function, Ineq. (X) is proved. Therefore, Ineq (X) and (X) are proved accordingly. Therefore, this implementation provides ($\epsilon, 1 - e^{-\epsilon}$)-DP guarantee.





