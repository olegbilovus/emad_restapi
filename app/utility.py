import os


def check_env():
    var_envs = ["JWT_SECRET", "ACCESS_TOKEN_EXPIRE_MINUTES"]
    error_msgs = []
    for var in var_envs:
        if var not in os.environ:
            error_msgs.append(f"ERROR: {var} not found in environment variables")
    if error_msgs:
        exit("\n".join(error_msgs))
