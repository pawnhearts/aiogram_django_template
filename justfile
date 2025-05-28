set dotenv-load

mi:
    docker compose -f compose.yml run web uv run python manage.py migrate

mami:
    docker compose -f compose.yml run web uv run python manage.py makemigrations && git add */migrations/*py

static:
    docker compose -f compose.yml run web uv run python manage.py collectstatic --noinput

messages:
    export LANG=$(echo $LANG | cut -. -f1)
    docker compose -f compose.yml run web uv run python manage.py makemessages -l $LANG  --noinput
    docker compose -f compose.yml run web uv run python manage.py compilemessages -l $LANG  --noinput

shell:
    docker compose -f compose.yml run web uv run python manage.py dbshell

sh:
    docker compose -f compose.yml run web uv run python manage.py shell_plus

re:
    git pull 2>&1 | tee /tmp/git-pull.log
    - grep pyproject.toml /tmp/git-pull.log && dc build web && docker compose run web uv run python manage.py collectstatic --noinput
    - grep migration /tmp/git-pull.log && docker compose run web uv run python manage.py migrate
    - grep static /tmp/git-pull.log && docker compose run web uv run python manage.py collectstatic --noinput
    - grep locale /tmp/git-pull.log && docker compose run web uv run python manage.py compilemessages -l ru_RU --noinput
    docker compose restart bot web
    docker compose up -d

    docker compose logs -n300 -f bot web

pu:
    git command -a -mfix
    git push
    ssh mbtl "cd mbtl && just re"
