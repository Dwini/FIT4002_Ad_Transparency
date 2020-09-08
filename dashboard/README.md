# Dashboard Project for Ad Transparency

## Deployment
1. in the root directory for the dashboard project, create a `.env` file. Copy the environment variable names from `.env.default` and populate their values. for example:
  `AWS_ACCESS_KEY_ID="FOOBAR"
  AWS_SECRET_ACCESS_KEY="FOOBAR"
  AWS_REGION="FOOBAR"`
2. install requirements with `pip install -r requirements.txt`.
3. run flask application with `python app.py`.

## Notes
* gunicorn will be the wsgi server in a Unix production evironment.
