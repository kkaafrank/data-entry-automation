from dotenv import dotenv_values

config = {
    **dotenv_values('.env.example'),
    **dotenv_values('.env')
}
