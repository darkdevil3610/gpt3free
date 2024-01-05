from flask import Flask, request
import g4f
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


app = Flask(__name__)

@app.route('/')
def index():
    return '<html><head><title>GPT-3-free</title></head><body><center><h1>Hello from Gourav \nUse the (/chat?query=your_query_message) to start!</h1></center></body></html>'


@app.route('/chat', methods=['GET'])
def chat():
  query_message = request.args.get('query', '')
  response = g4f.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
          "role": "user",
          "content": query_message
      }],
      stream=True,
  )
  result = ''.join(message for message in response)

  return f'{result}'


# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
  setup_testing_defaults(environ)
  return ""


if __name__ == '__main__':
  httpd = make_server('', 8000, app)
  print("Serving on port 8000...")
  httpd.serve_forever()
