
# Here's a guide to setup this userbot on a server

In no means is this guide optimized or the only way for setup, I just run it this way

## Update packages and install needed ones

```sh
sudo apt update && sudo apt upgrade && sudo apt -y install gnupg2 wget vim git gcc python3-dev build-essential python3-venv libpq-dev psycopg2-binary
curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt update && sudo apt upgrade && sudo apt -y install npm nodejs
```

## Install pm2 to manage the app and to run in background

```sh
npm install pm2@latest -g
```

<details>
    <summary>
    If the above commang gives an error
    </summary>

```sh
sudo mkdir /usr/local/lib/node_modules
sudo chown -R $USER /usr/local/lib/node_modules
```

</details>


### Setup pm2 to run at startup

```sh
pm2 startup
```

### then run the line that it says to run

## Setup Postgresql 14

```sh
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y update
sudo apt -y install postgresql-14
```

## Setup postgres user, replace $PGUSER with a username u want for postgres

```sh
sudo su - postgres

createuser -P -s -e $PGUSER
```

Then enter a pass when prompted and remeber it

<br>

<details>
    <summary>
    If it shows that the pass starts with SCRAM then do the following
    </summary>

### Edit the postgresql.conf and switch to md5 password_encryption

Look for Authentication section then password_encryption and set it to md5 (it was scram-sha-256) and uncomment the line if commented

```sh
sudo vim /etc/postgresql/13/master/postgresql.conf
```

### Edit the pg_hba.conf and switch the authentication to md5

Look for the scram and replace them by md5

```sh
sudo vim /etc/postgresql/13/master/pg_hba.conf
```

### Then change the user password

```sh
psql
ALTER USER $PGUSER WITH PASSWORD 'NEW_PASSWORD_HERE';
ctrl + d
```

</details>


## Create a database for the userbot

```sh
createdb -O $PGUSER cosmic
```

database url will be `postgresql://$PGUSER:$PASS@localhost:5432/cosmic`

replace `$PASS` and `$PGUSER` with the ones you chose

### then switch back to your user (press ctrl + d)

## Setup the bot

### Clone the repo and copy the sample config

```sh
cd && git clone https://github.com/ItsLuuke/ProjectcosmiclionFork.git && cd ProjectFizilionFork
cp sample_config.env config.env
```

now edit the config (vim config.env or nano config.env) and add the vars

### Install the requirements

```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
deactivate
```

### Add a start script for ease of use

```sh
cat > run.sh << EOF
#!/bin/bash
source venv/bin/activate
bash bot.sh
EOF
sudo chmod +x run.sh
```

## Test start the bot first and see if everything is fine

```sh
./run.sh
```

### If there is error and the bot didnt start correctly, then fix then before continuing to the next step

#

## If the bot starts fine then finish the pm2 setup

Start the bot with pm2

```sh
pm2 start run.sh --name cosmic
```

### to make the bot start automatically on startup 

```sh
pm2 save
```

### to stop/start or restart or check logs

```sh
pm2 start cosmic
pm2 stop cosmic
pm2 restart cosmic
pm2 logs cosmic --lines 100 #or how many lines to check
```
