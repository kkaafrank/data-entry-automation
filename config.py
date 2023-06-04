from dotenv import dotenv_values
import json

config = {
    **dotenv_values('.env.example'),
    **dotenv_values('.env')
}

for key in config.keys():
    if 'mapping' in key:
        config[key] = json.loads(config[key])
