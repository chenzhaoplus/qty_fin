from . import main


@main.route('/', methods=['GET', 'POST'])
def home():
    return 'Hello Home!'


@main.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'Hello World!'
