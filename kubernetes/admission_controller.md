My current research is focused on how to integrate privacy as a resource in Kubernetes. Kubernetes is a cluster management tool, providing powerful and convenient features, e.g., detecting failure and restarting dead applications. Before doing research on the big picture about privacy, I would like to start with a easy task: rate-limiting requests/access to a service. In Kubernetes, `service` is a built-in resource, which abstracts the connection to applications (`pods`) with a resource entity (API object). The benefit of doing this is that the communication among applications will not break even an application was dead and re-assigned to a new `node`.

(From now on, I will use `pod` rather than application in this article. We can consider a `pod` is a set of applications sharing the same memory.)

After reading the documentation of Kubernetes, Admission Controller comes to my mind. It is a webhook that can intercept any requests to API server. It gives me an intuition that the communication between `pods` should rely on the `api-server`. However, I was proven wrong later after I setup my first Admission Controller. The fact is that only CRUD on resources (including `service`) will refer to `api-server`. There is an operation called `CONNECT` regarding the request to `api-server`, but I don't know what is its usage. I cannot find out any examples and there is no documentation online. My next step should look at DNS service.

Some future reading here:

https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/

Nevertheless, I will still share my experience on setting up an admission controller, and how we can achieve some features included in the default controller, like `EventRateLimit`.
