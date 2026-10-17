# Website Uptime & Global Edge Latency Monitor

A Python-based website monitoring dashboard built with Streamlit, Docker, GitHub Actions, and Kubernetes. It checks website availability, records response times, and displays monitoring results through a web interface.

## Features

- Check website availability using HTTP requests.
- Display HTTP status codes and response times.
- Record monitoring results in a CSV file.
- Visualize response times using a chart.
- Run automated unit tests using pytest.
- Format and lint Python code using Black and Flake8.
- Build and publish a Docker image through GitHub Actions.
- Deploy the containerized application to Kubernetes.
- Run multiple application replicas with health probes and resource limits.

## Technology Stack

- **Python** — monitoring logic
- **Streamlit** — interactive dashboard
- **Pandas and Plotly** — data handling and visualization
- **Pytest** — automated tests
- **Black and Flake8** — formatting and linting
- **Docker** — containerization
- **GitHub Actions** — CI pipeline and image publishing
- **GitHub Container Registry (GHCR)** — Docker image storage
- **Kubernetes** — deployment, service discovery, health checks, and scaling

## Project Structure

```text
website-uptime-monitor/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s-deployment.yaml
├── k8s-service.yaml
├── monitor.py
├── app.py
├── test_monitor.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Run Locally

Create and activate a virtual environment, then install the dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start the dashboard:

```powershell
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Run Tests

```powershell
python -m pytest -v
```

Check formatting and linting:

```powershell
black --check monitor.py app.py test_monitor.py
flake8 monitor.py app.py test_monitor.py --max-line-length=88
```

## Run with Docker

Build the image:

```powershell
docker build -t website-uptime-monitor .
```

Start the container:

```powershell
docker run --rm -p 8501:8501 website-uptime-monitor
```

Open `http://localhost:8501`.

## CI Pipeline and Container Publishing

The GitHub Actions workflow runs on pushes and pull requests targeting `main`. It installs dependencies, checks formatting and linting, runs tests, and validates the Docker build.

On pushes to `main`, the workflow also publishes the image to GitHub Container Registry:

```text
ghcr.io/chrismariya-1412/website-uptime-monitor:latest
```

## Deploy to Kubernetes

Ensure Docker Desktop Kubernetes is enabled and `kubectl` is connected to the local cluster.

Apply the manifests:

```powershell
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

Check deployment status:

```powershell
kubectl rollout status deployment/website-monitor
kubectl get deployments,pods,services
```

Run the dashboard through port forwarding:

```powershell
kubectl port-forward service/website-monitor 8502:8501
```

Open `http://localhost:8502`. If that local port is already occupied, choose another unused local port.

Scale the application:

```powershell
kubectl scale deployment website-monitor --replicas=2
kubectl get pods
```

## Current Limitations

- The Kubernetes cluster is local to the development machine; the GitHub Actions workflow publishes images but does not directly deploy to that local cluster.
- Monitoring history is stored in a CSV file. Multiple replicas do not share this file, and container restarts may lose container-local history.
- The project demonstrates synthetic website checks, not a globally distributed monitoring network. Actual global edge latency measurement would require monitoring agents or probes in multiple geographic regions.

## Future Improvements

- Persist monitoring history in a database or shared storage.
- Add scheduled checks and alert notifications.
- Monitor multiple websites automatically.
- Deploy to a remote Kubernetes cluster.
- Collect latency measurements from multiple geographic regions.

## Repository

[GitHub: website-uptime-monitor](https://github.com/ChrisMariya-1412/website-uptime-monitor)
