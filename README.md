
# DevOps -  K8s and Helm Lab 

## Helm 

### Base tasks

- Create a chart (`helm create <nome-chart>`)
- Create three `values.yml` files:
    1. `values/default.yml` (common values between envs)
    2. `values/dev.yml` (dev config)
    3. `values/staging.yml` (staging config)
- Details of environments:
    - Dev:
        1. Service should be exposed on `8080`
        2. Each resource should have a label `env:dev`
    - Staging 
        1. Service should be exposed on `8090`
        2. Each resource should have a label `env:staging` 
    - Both env (on `values.yml`):
        1. Image should be parametrized (let's start with `public.ecr.aws/prima/bookshelf-remove-after-lab:2.0.0`)
- Prefix each resource name with the name of current Helm release
- Avoid hardcoding secret in `redis-secret.yml` and set it during `helm install` command.
- Deploy chart on both dev and staging environment (see `helm install`)
- Update (just for `web` deployment) the image name to `public.ecr.aws/prima/bookshelf-remove-after-lab:1.0.0` and upgrade the staging relase (see `helm upgrade`)
- Rollback staging release (see `helm rollback`) after checking upgrade differences.

### Advanced tasks:

- Define and use some sample commong labels (ex. `test1: val1`, `test2: val2` ...) into `helpers.tpl`
- Use [autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)  (mix 2 - max 4) on `staging` environment instead of a fixed number of replicas. (Hint: `kubectl autoscale` command with `--dry-run=client -o yaml` flags may be used to generate HPA manifest).