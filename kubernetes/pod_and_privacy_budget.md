# Pod and Privacy Budget

This article proposes a design on storing privacy budget information of pods in Kubernetes. Also, this design can be applied to other resources like deployment and even custom resources (e.g. user-defined Pipeline).

## Privacy Budget
In Sage, datasets are partitioned into data blocks based on some dimensions (e.g. timestamp, masked user id), if the dimensions do not contain sensitive information. Each data block is identified by the values of these dimensions and has its own privacy budget. These data blocks are consumed by some privacy-digesting applications. Therefore, a scheduler will allocate the data blocks to the applications. Next section will describe how to quantify the privacy need of an application (i.e. pod).

## Request of Privacy Budget

A data-driven application may need the data meeting specific conditions (e.g. time range, user group), so it should specify its dimensional requirements when it requires privacy budget. The requirements look like:

```yaml
startTime: <st>
endTime: <et>
startUserId: <su>
endUserId: <eu>

## other dimensions

privacyBudget: {epsilon: ..., delta: ...}
```

In principle, an application should treat two data blocks identically if they both meet the conditions of the applications. For the scheduler, its task is to assign the qualified data blocks to an applcation, but it cannot guarantee that the same data block will be assigned to an application if the application requests the private data blocks twice. For example, the data block is assigned to an application in the morning and run out of budget at noon. Then, if the application requests again in the afternoon, the scheduler cannot allocate this data block anymore, but other data blocks meeting the requirements of applications.

In addition, an application may only need some amount of data to process. For example, a linear regression model with 10 parameters may just need 10k data to get converged. Thus, it is unnecessary to assign 100 blocks with 10 million data to such a simple model. Thus, it is recommended to include the number of data needed in the requirement.

```yaml
minNumberOfData: 100000
expectedNumberofData: 500000
```

The scheduler first finds out all the data blocks meeting the dimensional conditions. Then the scheduler arbitrarily pick up a data blocks from them, and count the number of data inside this block. If the number of data doesn't meet the minimum number of data required by the application, the scheduler will continue to another data block, so on and so forth. Otherwise, if the minimum number of data is met, allocate the picked data blocks to the application.

The introduction of the number of data does not break the differential privacy semantics. In this scenario, the application acquires enough data meeting its conditions. It is allowed to consume the privacy of the allocated data blocks. For the selected data blocks, they record the privacy loss due to this application. For other data blocks meeting the dimensional conditions of this application but not selected, there is no change on their privacy. These unselected data blocks can be later consumed by other applications.

Using number of data has a few advantages. (1) there is a minimum guarantee that the amount of data an application can use, (2) data blocks are allowed to mature asynchronously, and (3) privacy budget is preserved by avoiding assigning unnecessary amount of data to an application. 

Here is an elaboration of (1) and (2). If data blocks are generated asynchronously: some data blocks may be ready earlier while others may mature later. There is no guarantee that how much data an application can be assigned if the application is scheduled before the arrival of some data blocks. However, the request with minimum number of data guarantees that an application either has enough data to start, or it should wait or be terminated. Also, an application can still start anyway, but the scheduler continues to assign latest qualified data blocks to it until the minimum request is met.

#### Representation of Privacy Budget Request in Kubernetes

Kubernetes allow users to specify extra information in the annotations of a resource. Therefore, I propose to use the annotation to indicate the privacy budget request of a pod (i.e. application). Here is an example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <your_pod>
  namespace: <your_namespace>
  annotations:
    dp-mode: "true"
    dp-dataset: <data-set>
    dp-request: 'true'
    dp-start-time: '0'
    dp-end-time: '1000'
    dp-start-user-id: '0'
    dp-end-user-id: '3000'
    # more dimensional conditions...

    dp-min-number-of-data: "100000"
    dp-expected-number-of-data: "500000"
    
    dp-min-epsilon: '0.1'
    dp-min-delta: '0.001'
    dp-expected-epsilon: '0.5'
    dp-expected-delta: '0.001'

```
This is an example of a pod waiting to be assigned data blocks. `dp-mode` indicates that this pod consumes privacy. `dp-request` indicates that this pod needs to be scheduled data blocks. `dp-dataset` specifies the dataset to consume. `dp-start-time`, `dp-end-time`, `dp-start-user-id`, and `dp-end-user-id` are the dimensional conditions. `dp-min-number-of-data` and `dp-expected-number-of-data` are the min and expected number of data an application needs. `dp-min-epsilon`, `dp-min-delta`, `dp-expected-epsilon`, and `dp-expected-delta` are the min and expected privacy budget an application needs.


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: <your_pod>
  namespace: <your_namespace>
  annotations:
    dp-mode: "true"
    dp-request: 'false'
    dp-dataset: <data-set>
    dp-start-time: '0'
    dp-end-time: '1000'
    dp-start-user-id: '0'
    dp-end-user-id: '3000'
    # more dimensional conditions...

    dp-actual-number-of-data: "130000"
    dp-actual-epsilon: "0.2"
    dp-actual-delta: "0.001"

    dp-acquired-blocks: '{block-1: (0.1, 0.001), block-2: (0.2, 0.002), ...}'
    dp-consumed-blocks: '{block-1: (0.1, 0.001), ...}'
```

This is an example of a pod after being assigned data blocks. `dp-request` becomes `false`. The min and expected fields of number of data and privacy budget are removed. The fields recording the actual assigned values, like `dp-actual-number-of-data`, `dp-actual-epsilon`, and `dp-actual-delta`, are appended. In addition, the field recording the privacy budget of the assigned data blocks (`dp-acquired-blocks` and `dp-used-blocks`) are created. For the detail on acquired and consumed privacy, please refer to the design document of Private Data Block.

## Reschedule

## Acquire more Privacy Budget from assigned Data Blocks


## Checkpoint
A checkpoint is made when the current state of an application persisted to storage. The storage indicates the privacy loss, therefore the application should also send a consume request to Kubernetes API server, notifying the privacy loss by the checkpoint.

### Sampling and Privacy Leakage
What about an application shuffle the dataset? When the application makes a checkpoint after it consumes some fraction of the data, what is the privacy loss of each data blocks? In other words, If an application (query) with $\epsilon$-DP randomly $X$ fraction of data from a Private Data Block, could we consider it to consume $X \epsilon$ of privacy budget of this data block?

Here is an interesting counter example. If a dataset has 1 billion health information (e.g. height, weight, age, and If_diabetes), and the query is to calculate the mean of height, weight, age, and If_diabetes in this dataset. The query can calculate the mean using every data point and add noises to maintain $\epsilon$-DP. However, there are too many data, could the algorithm do a sampling? What about querying half of the dataset with a noise maintaining $2 \epsilon$-DP? It seems that the query still maintains $\epsilon$-DP on the whole dataset given the purpose to calculate the mean. 

Now, Instead of querying the whole or half the dataset, could I only sample one data point from this data set? Then I add a noise maintaining $10^9 \epsilon$-DP, which basically means no noise. Of course, I make a bad estimate on the mean, but it seems that I know every detail of a specific person without breaking the DP constraint. 

Clearly, some step above is wrong, but I cannot find out where.

Another more practical example: even I add a new constraint that the DP-guarantee of a sampling query cannot exceed the privacy budget of a dataset. That is, if the dataset has $\epsilon$ privacy budget, the query on it cannot be weaker than $\epsilon$-DP. Under this constraint, I query the dataset twice and sample half of the data per query. It seems that the $\epsilon$-DP is not violated. However, 1/4 of the dataset will be queried twice and their privacy loss is  $2 \epsilon$. If the query is MAX and the maximum value is in that 1/4, the MAX result should break the $\epsilon$-DP.

### Indivdual Sampling yields (1/n, 1/n)-DP naturally?

It seems to me that randomly sampling an entry from a dataset whose values are distinctive can maintain (1/n, 1/n)-DP. However, the detail of the sampled entry is definitely leaked, because there is no noise adding to it.

Define $M$ is the random sampling process, $x$ is a dataset with $n$ distinctive members, and $y$ is another dataset with one more member than $x$. Also, the new member is different from the other members. Thus $|y-x| = 1$. I also define that $S$ is an query result, whose range is $x \cup y$. $S_x$ represents a member belonging to both $x$ and $y$, and $S_y$ is the new member of $y$.

Given ($\epsilon$, $\delta$)-DP,

$$ Pr(M(x) = S) \leq e^{\epsilon} Pr(M(y) = S) + \delta $$
 
 If $S = S_x$, the probability to get $S_x$ from $x$ and $y$ is $\frac{1}{n}$ and $\frac{1}{n+1}$, respectively. To acquire the minimum of $\epsilon$ and $\delta$, let LHS = RHS, 
 
 $$ Pr(M(x) = S_x) = e^{\epsilon} Pr(M(y) = S_x) + \delta $$
 
  $$ \frac{1}{n} = e^{\epsilon} \frac{1}{n+1} + \delta $$
  
  Let $\delta = 0$ and given $\ln(1+x) \leq x$ if $x \geq 0$, 
  
  $$\epsilon = \ln{\frac{n+1}{n}} = \ln{(1 + \frac{1}{n})} \leq \frac{1}{n}$$

Thus, $\epsilon \leq \frac{1}{n}$ and $\delta = 0$.

If $S = S_y$, the probability to get it from $x$ and $y$ is 0 and $\frac{1}{n+1}$, respectively.

 $$ Pr(M(x) = S_y) \leq e^{\epsilon} Pr(M(y) = S_y) + \delta $$
 
  $$ 0 \leq e^{\epsilon} \frac{1}{n+1} + \delta $$
  
Even $\delta = 0$, the above inequality is always True.


Let's switch the position of $x$ and $y$. The conclusion for $S_x$ still holds. The inequality of $S_y$ becomes


$$ Pr(M(y) = S_y) \leq e^{\epsilon} Pr(M(x) = S_y) + \delta $$

$$ \frac{1}{n+1} \leq e^{\epsilon} * 0 + \delta $$

Apparently, the minimum of $\delta$ is $\frac{1}{n+1}$.

Combining all the situations, a random sampling without noise can achieve ($\frac{1}{n}$, $\frac{1}{n+1}$)-DP. However, the query $M(x)$ leaks the detail of individual entries in the dataset.
