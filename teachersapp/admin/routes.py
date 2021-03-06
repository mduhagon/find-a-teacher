# Admin Blueprint. This Blueprint will hold all administration
# routes and functionality, that only the site administrator can access

from flask import Blueprint, current_app

admin = Blueprint('admin', __name__)

@admin.route("/admin/home")
def admin_home():
    return render_template(
        'home.html', 
        map_key=current_app.config['GOOGLE_MAPS_API_KEY']
    )