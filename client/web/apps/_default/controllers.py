"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from yatl.helpers import A

from py4web import URL, abort, action, redirect, request

from .common import (T, auth, authenticated, cache, db, flash, logger, session,
                     unauthenticated)


@action("index")
@action.uses("index.html", auth, T, A)
def index():
    user = auth.get_user()
    message = T("Hello {first_name}").format(**user) if user else T("Welcome! ") 
    return dict(message=message) 

@action("system")
@action("system/<infotype>")
@action.uses("system.html", auth, T)
def system(infotype="all") -> dict:
    from libs.getSysInfo import SystemInfo
    if infotype:
        s = SystemInfo(infoTypes=[infotype])
    else:
        s = SystemInfo()
    try:
        s.run()
        sysinfo = s.system_info
    except Exception as e:
        return dict(error="Unable to get system information: %s" % e)
    #return dict(data=systeminfo.system_info)
    match infotype:
        case "all":
            return dict(cpu=sysinfo["cpu_info"], memory=sysinfo["memory_info"], disk=sysinfo["disk_info"], network=sysinfo["network_info"], running_processes=sysinfo["running_processes"], wifi_profiles=sysinfo["wifi_profiles"], current_ssid=sysinfo["current_ssid"])
        case "os":
            return dict(os=sysinfo["os_info"])
        case "cpu":
            return dict(cpu=sysinfo["cpu_info"])
        case "memory":
            return dict(memory=sysinfo["memory_info"])
        case "disk":
            return dict(disk=sysinfo["disk_info"])
        case "process":
            return dict(running_processes=sysinfo["running_processes"])
        case "network":
            return dict(network=sysinfo["network_info"])
        case "wifi":
            return dict(wifi_profiles=sysinfo["wifi_profiles"], current_ssid=sysinfo["current_ssid"])
        case _:
            return dict(error="Invalid system information type")
    
@action("httptrace")
@action("httptrace/<hostname>")
@action.uses("generic.html", auth, T)
def httptrace(hostname = "google.com") -> dict:
    from libs.httptrace import HttpTrace
    htp = HttpTrace("http://%s" % hostname, 1, None)
    try:
        htp.run()
    except Exception as e:
        return dict(error="Unable to get http trace information: %s" % e)
    return dict(httptrace=htp.results)

@action("resolver")
@action("resolver/<domain>")
@action("resolver/<domain>/<record_type>")
@action("resolver/<domain>/<record_type>/<count:int>")
@action.uses("generic.html", auth, T)
def resolver(domain: str = "google.com", record_type: str = "A", count:int = 3) -> dict:
    from libs.resolverTime import resolverTime
    rt = resolverTime()
    rt.domain = domain
    rt.record_type = record_type
    rt.count = count
    try:
        x = rt.run()
    except Exception as e:
        return dict(error="Unable to get resolver time information: %s" % e)
    minTime = rt.results["min_time"] * 1000
    meanTime = rt.results["mean_time"] * 1000
    maxTime = rt.results["max_time"] * 1000
    return dict(domain=rt.domain, count=count, successful_count=rt.results["successful_count"], record_type=record_type, rawTimes=rt.results["times"], min_timeMS=minTime, mean_timeMS=meanTime, max_timeMS=maxTime)
