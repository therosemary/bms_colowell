from dingtalk_sdk_gmdzy2010.authority_request import AccessTokenRequest
from dingtalk_sdk_gmdzy2010.department_request import DeptsRequest,\
    SubDeptIdsRequest
from dingtalk_sdk_gmdzy2010.user_request import DeptUsersSimpleRequest


def get_token(**credentials):
    request = AccessTokenRequest(params=credentials)
    request.get_json_response()
    access_token = request.get_access_token()
    return access_token


def _recruit_dept_ids(init_ids=None, total_ids=None, access_token=None):
    if init_ids:
        sub_level_ids = []
        for _id in init_ids:
            params = {"access_token": access_token, "id": _id}
            get_new_ids = SubDeptIdsRequest(params=params)
            get_new_ids.get_json_response()
            new_ids = get_new_ids.get_sub_dept_ids()
            sub_level_ids.extend(new_ids)
            if not new_ids:
                continue
        total_ids.extend(sub_level_ids)
        return _recruit_dept_ids(init_ids=sub_level_ids, total_ids=total_ids,
                                 access_token=access_token)
    else:
        return total_ids


def _get_sub_dept_users(dept_ids=None, access_token=None):
    if dept_ids:
        dept_users = []
        for _id in dept_ids:
            params = {"access_token": access_token, "department_id": _id}
            get_users = DeptUsersSimpleRequest(params=params)
            get_users.get_json_response()
            users = get_users.get_dept_users_brief()
            dept_users.extend(users)
        return dept_users


def get_sub_department_users(access_token=None, dept_name=None):
    params = {"access_token": access_token, "id": 1, "fetch_child": False}
    get_level_2_depts = DeptsRequest(params=params)
    get_level_2_depts.get_json_response()
    level_2_depts = get_level_2_depts.get_depts(dept_name=dept_name)
    sub_dept_ids = _recruit_dept_ids(init_ids=[level_2_depts["id"]],
                                     total_ids=[level_2_depts["id"]],
                                     access_token=access_token)
    sub_dept_users = _get_sub_dept_users(dept_ids=sub_dept_ids,
                                         access_token=access_token)
    return sub_dept_users
