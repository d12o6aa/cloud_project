export DOCKER_HOST=unix:///run/docker.sock

docker build -t flask-docker-app .
sudo systemctl start docker
sudo systemctl status docker

docker container ls -a
docker image ls
docker run -d -p 5000:5000 --name model flask-docker-app
docker logs model
docker container rm -f model
docker ps
docker stop <container_id>
docker stop <container_name>
docker ps -a

<!-- --privileged بيخلي الكونتينر عنده access كامل للهاردوير (بس استخدميه بحذر). -->
docker run --privileged --device=/dev/video0 -p 5000:5000 your_image_name


docker run -p 5000:5000 freelance-app


http://127.0.0.1:5000/api/auth/register
http://127.0.0.1:5000/api/auth/login
http://127.0.0.1:5000/api/auth/client/dashboard
http://127.0.0.1:5000/api/auth/freelancer/dashboard
http://127.0.0.1:5000/api/auth/client/jobs
http://127.0.0.1:5000/api/auth/freelancer/jobs
http://127.0.0.1:5000/api/auth/create_job
http://127.0.0.1:5000/api/auth/create
http://127.0.0.1:5000/api/auth/list_jobs
http://127.0.0.1:5000/api/auth/offers
http://127.0.0.1:5000/api/auth/client/offers
http://127.0.0.1:5000/api/auth/
http://127.0.0.1:5000/api/auth/
http://127.0.0.1:5000/api/auth/


http://127.0.0.1:5000/client/dashboard
http://127.0.0.1:5000/freelancer/dashboard
http://127.0.0.1:5000/client/jobs
http://127.0.0.1:5000/client/offers
http://127.0.0.1:5000/freelancer/dashboard