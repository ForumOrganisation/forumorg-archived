import os
from flask_assets import Bundle, Environment
from forum import app

assets = Environment(app)

assets.append_path(os.path.join(os.path.dirname(__file__), './static'))
assets.append_path(os.path.join(os.path.dirname(__file__), './static/bower_components'))

bundles = {
    'js_common': Bundle(
        Bundle(
            'jquery/dist/jquery.min.js',
        ),
        output='build/common.min.js'),

    'js_index': Bundle(
        Bundle(
            'recaptcha/index.js',
            'typed.js/dist/typed.min.js',
            'jquery.scrollTo/jquery.scrollTo.min.js',
            'jQuery-One-Page-Nav/jquery.nav.js',
        ),
        Bundle(
            'js/index/index.js',
            filters='jsmin',
        ),
        output='build/index.min.js'),

    'js_login': Bundle(
        Bundle(
            'js/index/login.js',
            filters='jsmin',
        ),
        output='build/login.min.js'),

    'css_common': Bundle(
        Bundle(
            'bootstrap/dist/css/bootstrap.min.css',
            'font-awesome/css/font-awesome.min.css',
            filters='cssrewrite'
        ),
        output='build/common.min.css'),

    'css_index': Bundle(
        Bundle(
            'css/index/nemo.css',
            'css/index/colors/blue.css',
            filters='cssmin'
        ),
        output='build/index.min.css'),

    'css_login': Bundle(
        Bundle(
            'css/index/login.css',
            filters='cssmin'
        ),
        output='build/login.min.css'),

}

assets.register(bundles)
