# Exercise 30 – Deploying Flask Applications

## 1. Prepare the app
- `app.py` – Flask app with `/` ("Hello, World!") and `/health`
- `requirements.txt` – Flask + gunicorn
- `Procfile` – tells Heroku how to start the web process
- `.python-version` – Python version for Heroku's Python buildpack

## 2. WSGI server (gunicorn), tested locally
```bash
cd 03_python_web_application/ex30_deployment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
gunicorn app:app --bind 0.0.0.0:8000
curl http://127.0.0.1:8000/          # Hello, World!
```
Flask's built-in server (`python app.py`) is for development only. gunicorn runs multiple worker processes and is what production uses.

## 3. Deploy to Heroku
```bash
brew tap heroku/brew && brew install heroku
heroku login
git init && git add . && git commit -m "Flask app ready for Heroku"   # if deploying this folder on its own
heroku create my-flask-deploy-demo
git push heroku main
heroku open                           # share this live URL
heroku logs --tail                    # debugging
```
> Heroku has no free tier anymore; the Eco dyno is the cheapest option. Render or Railway can deploy this same Procfile/Dockerfile setup on a free plan.

## 4. Deploy with Docker
```bash
docker build -t flask-deploy-demo .
docker run -p 8000:8000 flask-deploy-demo
curl http://127.0.0.1:8000/health     # {"status":"ok"}

# push to Docker Hub
docker login
docker tag flask-deploy-demo <dockerhub-username>/flask-deploy-demo:1.0
docker push <dockerhub-username>/flask-deploy-demo:1.0
```
On an Apple Silicon Mac, build for cloud x86 servers with
`docker buildx build --platform linux/amd64 -t <user>/flask-deploy-demo:1.0 --push .`

## 5. Optional: cloud provider
- **AWS**: App Runner → "Container registry" → select the Docker Hub/ECR image → port 8000.
- **Azure**: `az webapp create --deployment-container-image-name <user>/flask-deploy-demo:1.0 ...` (App Service for Containers), then set `WEBSITES_PORT=8000`.
- **Google Cloud Run**: `gcloud run deploy flask-deploy-demo --image docker.io/<user>/flask-deploy-demo:1.0 --port 8000`.

## Production checklist
- `debug` is off (only on when `FLASK_DEBUG=1`)
- `SECRET_KEY` comes from an environment variable
- the container runs as a non-root user and has a health check
- dependencies are pinned in `requirements.txt`
