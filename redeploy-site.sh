#tmux kill-server
cd /root/flask_repo || exit 1
git fetch --all
git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
#source python3-virtualenv/bin/activate
#pip install -r requirements.txt
#systemctl restart myportfolio
#tmux new -d -s flaskapp
#tmux send-keys -t flaskapp "source ../python3-virtualenv/bin/activate" C-m
#tmux send-keys -t flaskapp "export FLASK_APP=app" C-m
#tmux send-keys -t flaskapp "flask run --host=0.0.0.0 --port=5000" C-m
