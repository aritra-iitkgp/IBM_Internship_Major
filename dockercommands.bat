docker build -t codechef1/churn-app:v2 .
docker run -p 5000:5000 codechef1/churn-app:v2
docker push codechef1/churn-app:v2