# Build an Application

   ```shell
   $ ansible-galaxy collection install -r requirements.yaml
   ```

   ```shell
   $ ansible-playbook playbook.yaml --extra-vars "deploy_environment={{ environment }}"
   ```

where the optional values of the environment variable are `dev` and `test`

**Dockerfile in the code repo for reference**

* marketplace

   * Dockerfile.j2
   
   ```dockerfile
   FROM openjdk:8-jdk-alpine
   RUN apk add --no-cache ttf-dejavu tzdata
   ARG USER_HOME_DIR="/root"
   WORKDIR {{ docker.working_directory }}
   COPY ./target/{{ jar_file }} {{ docker.working_directory }}/
   ENV TZ="Asia/Shanghai"
   CMD java -jar {{ jar_file }} --spring.profiles.active={{ deploy_environment }} --aws.ak="{{ aws.access_key | jasypt_encrypt('%s'|format(jasypt.password)) }}" --aws.sk="{{ aws.secret_access_key | jasypt_encrypt('%s'|format(jasypt.password)) }}"
   ```

* housekeeping

   * Dockerfile.j2
    
   ```dockerfile
   FROM python:3.8-slim
   RUN apt-get update && apt-get install -y --no-install-recommends cron tzdata wget gnupg lsb-release build-essential
   RUN apt-get update && apt-get install -y --no-install-recommends python3-dev python3-psycopg2 python3-virtualenv
   RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
   RUN echo "deb http://apt.postgresql.org/pub/repos/apt `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
   RUN apt-get update && apt-get install -y --no-install-recommends postgresql-client-12 libpq-dev
   WORKDIR {{ docker.working_directory }}
   ENV VIRTUAL_ENV=/opt/venv
   RUN python3 -m pip install virtualenv
   RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
   ENV PATH="$VIRTUAL_ENV/bin:$PATH"
   COPY ./b2b/requirements.txt requirements.txt
   RUN pip install -r requirements.txt
   COPY ./b2b/*.py ./
   COPY ./b2b/cfg_{{ deploy_environment }}.cfg {{ docker.working_directory }}/cfg.cfg
   ADD ./cron/crontab /etc/cron.d/cron-jobs
   RUN chmod 0644 /etc/cron.d/cron-jobs
   ADD ./cron/cron.sh {{ docker.working_directory }}/cron.sh
   RUN chmod +x {{ docker.working_directory }}/cron.sh
   RUN mkdir -p /var/log/cron && touch /var/log/cron/cron.log
   ENV TZ="Asia/Shanghai"
   ENTRYPOINT ["/bin/sh", "{{ docker.working_directory }}/cron.sh"]
   ```

   * cron.sh

   ```shell
   #!/usr/bin/env bash
   printenv | cat - /etc/cron.d/cron-jobs > ~/crontab.tmp && mv ~/crontab.tmp /etc/cron.d/cron-jobs
   chmod 644 /etc/cron.d/cron-jobs
   crontab /etc/cron.d/cron-jobs
   tail -f /var/log/cron/cron.log &
   cron -f
   ```