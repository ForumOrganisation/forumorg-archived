import os
from flask_assets import Bundle, Environment
from forum import app

assets = Environment(app)

assets.append_path(os.path.join(os.path.dirname(__file__), './static'))
assets.append_path(os.path.join(os.path.dirname(__file__), './static/bower_components'))

bundles = {
    'js_index': Bundle(
        Bundle(
            'recaptcha/index.js',
            'jquery/dist/jquery.min.js',
            'typed.js/dist/typed.min.js',
            'jquery.scrollTo/jquery.scrollTo.min.js',
            'jQuery-One-Page-Nav/jquery.nav.js',
            'iCheck/icheck.min.js',
        ),
        Bundle(
            'js/index/index.js',
            'js/index/login.js',
            filters='jsmin',
        ),
        output='build/index.min.js'),

    'css_index': Bundle(
        Bundle(
            'bootstrap/dist/css/bootstrap.min.css',
        ),
        Bundle(
            'css/index/colors/blue.css',
            'iCheck/skins/square/blue.css',
            'css/index/nemo.css',
            filters='cssmin'
        ),
        output='build/index.min.css'),

    # Add other bundles
}

assets.register(bundles)
