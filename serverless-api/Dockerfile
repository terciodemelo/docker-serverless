FROM python:3.7.4-slim

RUN pip install requests falcon gunicorn
EXPOSE 3000

VOLUME /api/main.py
WORKDIR /api

CMD gunicorn -b 0.0.0.0:3000 \
    --reload \
    --access-logformat  '{"type":"gunicorn_access_log","scope":"public","client_address":"%(h)s","request_id":"%({X-Request-Id}i)s","domain":"%({Host}i)s","response_code":"%(s)s","http_method":"%(m)s","path":"%(U)s","request_querystring":"%(q)s","duration_response_from_upstream":"%(D)s","response_length":"%(B)s"}' \
    main:api