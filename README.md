# Naruto Bot

Rojitzu Bot is a Discord Bot dedicated to **Naruto Uzumaki**.

## Installation

Get the repository from [github](https://github.com/) to install this bot.
```bash
git clone https://github.com/Canttuchdiz/naruto_bot.git
```

Make a .env file as another project file:
```
token = (your token)
```

Configure the config.py file
```
CHARACTER = (your character)
OPENAI_KEY = (your apikey)
MODEL = (your model)
```

Build and run the bot by running:
```bash
docker compose up -d --build
```

Every once and awhile run:
```bash
docker system prune -a
```

## Usage

Using ``/threac create`` and ``/thread close`` are the commands for controlling
the threads the bot can talk in.

## Notes

In any text channel, the owner must run ``!sync`` the first time you run
your bot.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
