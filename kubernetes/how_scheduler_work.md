This note shows that how scheduler is deployed in `Kubernetes` and how it can listen to pod and node events and process them.


## Deploy kube-scheduler
`kube-scheduler` is the default scheduler in `Kubernetes`. It will automatically deployed by `Kubernetes` and here is the main function of `kube-scheduler`.
```go
// cmd/kube-scheduler/scheduler.go
func main() {
	rand.Seed(time.Now().UnixNano())

	command := app.NewSchedulerCommand()

    // other logics
    if err := command.Execute(); err != nil {
		os.Exit(1)
	}
}
```

`main` functions define the scheduler command as follows and execute (run) it.

```go
// cmd/kube-scheduler/app/server.go
func NewSchedulerCommand(registryOptions ...Option) *cobra.Command {

    // some preparation

    cmd := &cobra.Command{
		Use: "kube-scheduler",
		Long: "..."
		Run: func(cmd *cobra.Command, args []string) {
			if err := runCommand(cmd, args, opts, registryOptions...); err != nil {
				fmt.Fprintf(os.Stderr, "%v\n", err)
				os.Exit(1)
			}
		},
	}
}

Below is the implementation of `Run` command:

func runCommand(cmd *cobra.Command, args []string, opts *options.Options, registryOptions ...Option) error {

    // some logic

    return Run(ctx, cc, registryOptions...)
}


func Run(ctx context.Context, cc schedulerserverconfig.CompletedConfig, outOfTreeRegistryOptions ...Option) error {

    // some logics

    sched, err := scheduler.New(cc.Client,
        // some parameters setting
    )
    
    sched.Run(ctx)
    return fmt.Errorf("finished without leader elect")
}
```

## Make Scheduler listen to Pod and Node Events
When a scheduler is `New`-ed and deployed, it needs to listen to `pod` and `node` events to make sure they are well scheduler. A scheduler uses resource informers to receive events on `pod` and `node`.

`AddAllEventHandlers` injects the handler of scheduler into resource (`pod` and `node` ) listeners.

```go
// pkg/scheduler/scheduler.go
func New(client clientset.Interface,
	informerFactory informers.SharedInformerFactory,
	podInformer coreinformers.PodInformer,
	recorder events.EventRecorder,
	stopCh <-chan struct{},
	opts ...Option) (*Scheduler, error) {

        // some logics

        AddAllEventHandlers(sched, options.schedulerName, informerFactory, podInformer)
    }

// pkg/scheduler/eventhandlers.go
func AddAllEventHandlers(
	sched *Scheduler,
	schedulerName string,
	informerFactory informers.SharedInformerFactory,
	podInformer coreinformers.PodInformer,
) {
    podInformer.Informer().AddEventHandler(
        cache.FilteringResourceEventHandler{
            
            // some logics

            Handler: cache.ResourceEventHandlerFuncs{
                AddFunc:    sched.addPodToSchedulingQueue,
                UpdateFunc: sched.updatePodInSchedulingQueue,
                DeleteFunc: sched.deletePodFromSchedulingQueue,
            },
        },
    )
}

// the action to handle pod create event
func (sched *Scheduler) addPodToSchedulingQueue(obj interface{}) {
	if err := sched.SchedulingQueue.Add(obj.(*v1.Pod)); err != nil {
		utilruntime.HandleError(fmt.Errorf("unable to queue %T: %v", obj, err))
	}
}
```

## Scheduler workflow in Kubernetes

When a scheduler is run, it continually pops the pods from its priority queue. At the same, as shown above, the priority queue will be pushed pods when a pod listener receive pod events regarding `create` and `update`. 

```go
// pkg/scheduler/scheduler.go

// Run begins watching and scheduling. It waits for cache to be synced, then starts scheduling and blocked until the context is done.
func (sched *Scheduler) Run(ctx context.Context) {
	if !cache.WaitForCacheSync(ctx.Done(), sched.scheduledPodsHasSynced) {
		return
	}
	sched.SchedulingQueue.Run()
	wait.UntilWithContext(ctx, sched.scheduleOne, 0)
	sched.SchedulingQueue.Close()
}

func (sched *Scheduler) scheduleOne(ctx context.Context) {

    // pop a pod from its priority queue, where pods are pushed by addPodToSchedulingQueue and updatePodInSchedulingQueue.
    podInfo := sched.NextPod()

    //filter and score

    scheduleResult, err := sched.Algorithm.Schedule(schedulingCycleCtx, state, pod)
    go func() {
        // pre-bind
        err := sched.bind(bindingCycleCtx, assumedPod, scheduleResult.SuggestedHost, state)
        // post-bind
    }()
}

// pkg/scheduler/internal/queue/scheduling_queue.go
// This is the implementation of Scheduler.NextPod()
func MakeNextPodFunc(queue SchedulingQueue) func() *framework.PodInfo {
	return func() *framework.PodInfo {
		podInfo, err := queue.Pop()
		if err == nil {
			klog.V(4).Infof("About to try and schedule pod %v/%v", podInfo.Pod.Namespace, podInfo.Pod.Name)
			return podInfo
		}
		klog.Errorf("Error while retrieving next pod from scheduling queue: %v", err)
		return nil
	}
}


```