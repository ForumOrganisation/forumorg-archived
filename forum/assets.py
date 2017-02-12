import os

from flask_assets import Bundle, Environment
from forum import app

assets = Environment(app)

assets.append_path(os.path.join(os.path.dirname(__file__), './static'))
assets.append_path(os.path.join(os.path.dirname(__file__), './static/bower_components'))

# TODO: Apply hierarchy
bundles = {
    'js_common': Bundle(
        Bundle(
            'jquery/dist/jquery.min.js',
            'bootstrap/dist/js/bootstrap.min.js'
        ),
        output='build/common.min.js'),

    'css_common': Bundle(
        Bundle(
            'bootstrap/dist/css/bootstrap.min.css',
            'font-awesome/css/font-awesome.min.css',
            'css/common.css',
            filters='cssrewrite'
        ),
        output='build/common.min.css'),

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

    'css_index': Bundle(
        Bundle(
            'css/index/nemo.css',
            'css/index/colors/blue.css',
            filters='cssmin'
        ),
        output='build/index.min.css'),

    'css_login': Bundle(
        Bundle(
            'AdminLTE/dist/css/AdminLTE.min.css',
            'css/index/login.css',
            filters='cssmin'
        ),
        output='build/login.min.css'),

    'js_admin': Bundle(
        Bundle(
            'select2/dist/js/select2.min.js',
            'select2/dist/js/i18n/fr.js',
            'PACE/pace.min.js',
            'jquery.inputmask/dist/min/jquery.inputmask.bundle.min.js',
            'intl-tel-input/build/js/intlTelInput.min.js',
            'datatables.net/js/jquery.dataTables.min.js',
            'datatables.net-bs/js/dataTables.bootstrap.min.js',
            'AdminLTE/dist/js/app.min.js',
        ),
        Bundle(
            'bootstrap-editable/src/js/bootstrap-editable.js',
            'notify-js/Notify.js',
            'js/admin/admin.js',
            filters='jsmin',
        ),
        output='build/admin.min.js'),

    'css_admin': Bundle(
        Bundle(
            'AdminLTE/dist/css/AdminLTE.min.css',
            'AdminLTE/dist/css/skins/skin-blue.min.css',
            'select2/dist/css/select2.min.css',
            'datatables.net-bs/css/dataTables.bootstrap.min.css',
        ),
        Bundle(
            'PACE/themes/white/pace-theme-minimal.css',
            'bootstrap-editable/src/css/bootstrap-editable.css',
            'intl-tel-input/build/css/intlTelInput.css',
            'css/admin/admin.css',
            filters='cssmin',
        ),
        output='build/admin.min.css'),

}

assets.register(bundles)
