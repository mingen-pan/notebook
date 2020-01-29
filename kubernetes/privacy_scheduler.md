This is a proposal regarding how to use Kubernetes to assign privacy resources to data-processing pipelines. 


## Privacy: Entity or Scaler?
Sometimes it is hard to consider to consider privacy as a resource, like CPU and Memory. We can just point to an object and tell people "this is a privacy". However, differential privacy (DP) provides a metric to calculate the privacy leakage. The more you leak, the less privacy you have. Thus, we can use the metric from differential privacy to quantify a privacy resource. In this case, `privacy` looks like a scalar. 

The traditional DP only considers on static databases. Lécuyer et al. (2019) proposes a new framework to deal with the DP of datastream. Instead of considering every data as a whole set, they partition the datastream into blocks. Queries on datastream can choose which block(s) to consume. The framework accounts the DP of each data block instead of the whole datastream. In this scenario, it is intuitive to consider each data block as an entity (with the metric of available privacy) and assign them to queries. In this scenario, it seems privacy can be treated as entities.

Treating privacy as a scaler or entity is not actually conflicted. The scalar view is focused on how much about of privacy a query can request. It should not consider on the details like which datablocks should it be assigned. It asks a privacy manager if there are enough privacy in this time range for me to consume. If yes, It will start its work, otherwise it needs to modify its request. The data can be stored as records, blocks, or whatever. After a query succeeds to request some amount of privacy at some time range, it will start to deal with data acquisition. And now comes to how the privacy data is stored and partitioned. The pipeline may request a data manager and asks for the data in the approved time range.

## Integration of Differential Privacy into Kubernetes
The idea above is to separate the privacy distribution into two processes: privacy request and data acquisition. The privacy request above is related with scheduler (or admission controller) in Kubernetes and the data assignment can be achieved by a lot forms, like a service or controller.

When a pipeline (a `pod` in Kubernetes) is to started, it will send a request (its configuration) with the following form:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pipeline
spec:
  containers:
  - name: training
    image: train-image
    resources:
      requests:
        dpEpsilon: 0.01
        dpIndexStart: 100
        dpIndexEnd: 200
  - name: validation
    image: validate-image
    resources:
      requests:
        dpEpsilon: 0.02
        dpIndexStart: 150
        dpIndexEnd: 200
```

The scheduler or admission controller reviews the above request. They goes into a privacy pool and see if this time range contains enough privacy (the metric here is `epsilon`).If yes, they will subtract this amount of privacy from the privacy pool and approve this request. After a pipeline is approved, it has the access to the data in this time range and it is the responsibility of this pipeline to query the data in a DP way.

Once the pipeline is started, it still has no data because neither scheduler not admission controller have the ability to send anything to this pipeline. It is the pipeline's job to ask for data.
