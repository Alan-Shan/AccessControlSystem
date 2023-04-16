from resources.routes.login import *
from resources.routes.pictures import *
from resources.routes.visit_requests import *


def init(app):
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/refresh', 'refresh', refresh, methods=['POST'])
    app.add_url_rule('/who_am_i', 'who_i_am', who_i_am, methods=['GET'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['DELETE'])
    app.add_url_rule('/add_request', 'add_visit_request', add_visit_request, methods=['POST'])
    app.add_url_rule('/get_requests', 'get_visit_requests', get_visit_requests, methods=['GET'])
    app.add_url_rule('/add_picture', 'add_picture', add_picture, methods=['POST'])
    app.add_url_rule('/get_picture_by_id/<id>', 'get_picture_by_id', get_picture_by_id, methods=['GET'])
    app.add_url_rule('/get_picture_by_path/<path>', 'get_picture_by_patch', get_picture_by_patch, methods=['GET'])
    app.add_url_rule('/get_not_approved_requests', 'get_not_approved_visit_requests', get_not_approved_visit_requests, methods=['GET'])
    app.add_url_rule('/get_approved_requests', 'get_approved_visit_request', get_approved_visit_request, methods=['GET'])
    app.add_url_rule('/get_request/<id>', 'get_visit_requests_by_id', get_visit_requests_by_id, methods=['GET'])
    app.add_url_rule('/approve_request/<id>', 'approve_visit_request', approve_visit_request, methods=['POST'])
    app.add_url_rule('/reject_request/<id>', 'reject_visit_request', reject_visit_request, methods=['POST'])
    app.add_url_rule('/delete_request/<id>', 'delete_visit_request', delete_visit_request, methods=['POST'])
    app.add_url_rule('/add_admin', 'add_admin', add_admin, methods=['POST'])
    app.add_url_rule('/get_admins', 'get_admins', get_admins, methods=['GET'])
    app.add_url_rule('/get_admin/<id>', 'get_admin_by_id', get_admin_by_id, methods=['GET'])
    app.add_url_rule('/delete_admin/<id>', 'delete_admin', delete_admin, methods=['DELETE'])
    app.add_url_rule('/change_admin_type', 'change_admin_type', change_admin_type, methods=['POST'])
    app.add_url_rule('/modify_admin', 'modify_admin', modify_admin, methods=['POST'])
    app.add_url_rule('/modify_request', 'modify_visit_request', modify_visit_request, methods=['POST'])
