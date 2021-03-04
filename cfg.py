jwt_token = "114514"

default_pages = 10

run_cfg = {
    # "app": "main:app",
    "host": "0.0.0.0",
    "port": 5000,
    # "uds": uds,
    # "fd": fd,
    # "loop": loop,
    # "http": http,
    # "ws": ws,
    # "lifespan": lifespan,
    # "env_file": env_file,
    # "log_config": LOGGING_CONFIG if log_config is None else log_config,
    # "log_level": log_level,
    # "access_log": access_log,
    # "interface": interface,
    "debug": True,
    # "reload": True,
    "reload_dirs": ["."],
    "reload_delay": 3,
    # "workers": 8,
    # "proxy_headers": proxy_headers,
    # "forwarded_allow_ips": forwarded_allow_ips,
    # "root_path": root_path,
    # "limit_concurrency": limit_concurrency,
    # "backlog": backlog,
    # "limit_max_requests": limit_max_requests,
    # "timeout_keep_alive": timeout_keep_alive,
    # "ssl_keyfile": ssl_keyfile,
    # "ssl_certfile": ssl_certfile,
    # "ssl_keyfile_password": ssl_keyfile_password,
    # "ssl_version": ssl_version,
    # "ssl_cert_reqs": ssl_cert_reqs,
    # "ssl_ca_certs": ssl_ca_certs,
    # "ssl_ciphers": ssl_ciphers,
    # "headers": [header.split(":", 1) for header in headers],
    "use_colors": True,
    # "factory": factory,
}

database_cfg = {
    'db':'54sh',
    'host':'192.168.1.4',
    'port':27017
}

Admin_mono = {
    'name':"Admin",
    'pw':"19260817"
}