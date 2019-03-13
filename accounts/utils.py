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


def get_department_users(access_token=None, department_name=None, root=1):
    """
    Method to collect all of the members for specified department are not
    supplied officially, the only way to make it is to the recursion as below.
    """
    if access_token is None or department_name is None:
        raise ValueError("No access_token or department name, return nothing!")
    
    params = {"access_token": access_token, "id": root, "fetch_child": False}
    depts_request = DeptsRequest(params=params)
    depts_request.get_json_response()
    level_2_depts = depts_request.get_depts(dept_name=department_name)
    
    # the recursion function to collect members.
    department_user_ids = _recruit_dept_ids(init_ids=[level_2_depts["id"]],
                                            total_ids=[level_2_depts["id"]],
                                            access_token=access_token)
    department_users = _get_sub_dept_users(dept_ids=department_user_ids,
                                           access_token=access_token)
    return department_users
