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
            'bootstrap/dist/js/bootstrap.min.js',
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
        output='gen/index.min.js'),

    'css_index': Bundle(
        Bundle(
            'bootstrap/dist/css/bootstrap.min.css',
            'iCheck/skins/square/blue.css',
        ),
        Bundle(
            'css/index/colors/blue.css',
            'css/index/typography/typography-1.css',
            'css/index/nemo.css',
            'css/index/index.css',
            'css/index/login.css',
        ),
        output='gen/index.min.css',
        filters='cssmin'),

    # Add other bundles
}

assets.register(bundles)
