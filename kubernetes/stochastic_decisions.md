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


## 5. Cutoff Exponential Implementation

This implementation has the basic idea: if total counting $N$ equals or larger than $m$, then the decision should always yield `True`. That is

\begin{align}
    Pr(Q(N \geq m) = 1) = 1. \tag{5.1} 
\end{align}


Also when $N < m$, the implementation needs to provide a $\epsilon$-DP guarantee, so the probability of yielding `True` should maintain a relationship like

\begin{align}
    Pr(Q(N) = 1) = e^{\epsilon} Pr(Q(N - 1) = 1). \tag{5.2} 
\end{align}


Combine (5.1) and (5.2), we can get for every $N \leq m$,

\begin{align}
    Pr(Q(N) = 1) = e^{\epsilon (N - m)}, \tag{5.3}\\
    Pr(Q(N) = 0) = 1 - e^{\epsilon (N - m)}. \tag{5.4}
\end{align}

When $N = m$, 

\begin{align}
    Pr(Q(m-1) = 0) \leq e^{\epsilon} Pr(Q(m) = 0) + \delta, \tag{5.5}\\ 
    \Rightarrow 1 - e^{-\epsilon} \leq e^{\epsilon} * 0 + \delta. \tag{5.6}
\end{align}

Thus the minimum of $\delta$ is $1 - e^{-\epsilon}$. Given the minimum $\delta$ and (5.2), 

\begin{align}
    Pr(Q(N+1) = 1) \leq e^{\epsilon} Pr(Q(N) = 1) + 1 - e^{-\epsilon}\tag{5.7}
\end{align}

is always correct by the definition. Switching LHS and RHS is also correct, because $Pr(Q(N) = 1)$ is always smaller than $Pr(Q(N + 1) = 1)$.

Now the question becomes proving the correctness of

\begin{align}
    Pr(Q(N) = 0) \leq e^{\epsilon} Pr(Q(N+1) = 0) + 1 - e^{-\epsilon} \tag{5.8}
\end{align}


for every $N < m$. Given $Pr(Q(N) = 0)$ is a monotonically decreasing and the proof of (5.5), if we can prove 

\begin{align}
    \frac{d}{dx}Pr(Q(x=a) = 0) \geq \frac{d}{dx}Pr(Q(x=b) = 0), \tag{5.9}
\end{align}

where $a + 1 \leq b$, then the Lemma 1. could lead to the proof of Ineq. (5.8).

For simplicity, define $f(x) = Pr(Q(x) = 0)$, then

\begin{align}
    f'(x) = \frac{d}{dx} (1 - e^{\epsilon (x - m)}), \tag{5.10}\\
    \Rightarrow f'(x) = - e^{-\epsilon m} \frac{d}{dx}  e^{\epsilon x} = - e^{-\epsilon m} \epsilon e^{\epsilon x}. \tag{5.11}
\end{align}

Since $f'(x)$ is apparently a monotonically decreasing function, Ineq. (5.9) is proved. Ineq (5.8) is proved accordingly. Therefore, this Cutoff Exponential Implementation provides ($\epsilon, 1 - e^{-\epsilon}$)-DP guarantee.

### Cutoff at small N
(under development)

When $N$ is small, $Pr(Q(N)=1)$ could also be set to be zero without breaking the ($\epsilon, 1 - e^{-\epsilon}$)-DP guarantee.





