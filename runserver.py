#!/usr/bin/python
from forum import app
import os

port = int(os.environ.get('PORT', 3000))
app.run(host='127.0.0.1', port=port, debug=True)
