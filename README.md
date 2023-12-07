# kl
Shortcut for running `kubectl logs <pod-name> -n <namespace> -f`. The pod
name and namespace are filled in with best guesses given a pattern. For example,
instead of running
```bash
kubectl get pods -A
# NAMESPACE     NAME                           READY   STATUS   ...  AGE
# kube-system   coredns-597584b69b-fzxgt       1/1     Running  ...  13m
kubectl logs coredns-597584b69b-fzxgt -n kube-system -f
# ... the logs ...
```
use
```bash
kl coredns
```

## ⚙️ Install
```bash
pip install git+https://github.com/t-young31/kl
```

## 🚀 Usage
```bash
kl <pod-pattern>
```
Run `kl --help` for options

## 🏗️ Development
Contributions are very welcome! Suggested steps:
- Fork this repository and create a branch
- Run `pip install -e .[dev] && pre-commit install` to install the dev deps and pre-commit
- Modify, commit, push and open a pull request against `main` for review
