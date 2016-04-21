'''
    Simple Python module for Cisco UCS Director reporting API
'''

# UCS Director:
UCSD_HOST    = "ucsd.example.com"
UCSD_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# request constructor:
UCSD_API_URL = "http://%s/app/api/rest?" # HTTPS?
UCSD_API_BASE_PARAMS = "formatType=json&opName=%s"
UCSD_API_OPDATA_PREP = "&opData="
HTTP_REQ_HEADERS = {"X-Cloupia-Request-Key":" "}
HTTP_REQ_HEADERS["X-Cloupia-Request-Key"] = UCSD_API_KEY
HTTP_UCSD_COOKIES = dict()
HTTP_UCSD_TIMEOUT = 3 # API call timeout in seconds

import requests
import json

from helper import *
from ucsd_api_contexts import *

#############################################################################################################
## basic API machinery

def ___APIcall___(APIOP, params=""):
	# returns a dictionary or None
	url = UCSD_API_URL % (UCSD_HOST) + UCSD_API_BASE_PARAMS % (APIOP)
	if not (params==""):
	   url = url + UCSD_API_OPDATA_PREP + params
	try:
	    r = requests.get(url, headers=HTTP_REQ_HEADERS, cookies = HTTP_UCSD_COOKIES, timeout=timeout)
	except: raise  # most useful during debugging
	# exceptions to catch later: http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions
	if r.status_code == requests.codes.ok:  
	    HTTP_UCSD_COOKIES = r.cookies # saving cookies 
	    if ('application/json' in r.headers.get('content-type')):
		    return r.json()
	    elif ('xml' in r.headers.get('content-type')):
		    return xml2dict(r.text)
	    else: return None      # to do: add logging
	else: r.raise_for_status() # seems the most useful thing to do, while I'm debugging this; later will need to think of some better logic

def ___APIclearCookies___():
    HTTP_UCSD_COOKIES = dict()

def ___APIpreparse___(jj):
    # Preparses the API reply contained in a dictionary
	# returns a less-raw dictionary (serviceResult only) or None
    # need a more complex preparsing:
	# - error / exception check, like "serviceError":null
    if jj:
        if j['serviceResult']:  
		    return j['serviceResult']
        else: return None
    else: return None # to do: add logging

####################################
# TODO: params expander dict->json
####################################
	
#############################################################################################################	
## Reporting General
## Doesn't work at the moment

def GetReportsList(contextName, contextValue):
    UCSD_API_OPNAME = "userAPIGetAvailableReports"
    u =  "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '"}'
    res = ___APIpreparse___(___APIcall___(APIOP=UCSD_API_OPNAME, params=u))
    return res

def ___PrintGetReportsAvailable___(res):
    for r in res:
	    print "%s\t%s\t%s\n" % (r[u'reportLabel'],r[u'reportType'],r[u'reportId'])

def GetReportTabular(contextName, contextValue, reportId):
    UCSD_API_OPNAME = "userAPIGetTabularReport"
    u = "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '", param2:"' + reportId + '"}'
    res = ___APIpreparse___(___APIcall___(APIOP=UCSD_API_OPNAME, params=u))
    return res

def GetReportHistorical(contextName, contextValue, reportId, durationName):
    UCSD_API_OPNAME = "userAPIGetHistoricalReport"
    u = "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '", param2:"' + reportId + '", param3:"' +durationName + '"}'
    res = ___APIpreparse___(___APIcall___(APIOP=UCSD_API_OPNAME, params=u))
    return res

#############################################################################################################
## Report Templates
def GetReportsReportBuilderTemplates():
    # Gets a list of all report templates in the system
    UCSD_API_OPNAME = "userAPIGetTabularReport"
    u = '{param0:"10",param1:"null",param2:"REPORT-BUILDER-TEMPLATES-T63"}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res	# {"Id":"templateID","Name":"some name","Description":"some description"}

def GetReportsReportBuilder(templateID):
    # Gets a table of reports generated using selected template	
    UCSD_API_OPNAME = "userAPIGetTabularReport"
    u = '{param0:"654",param1:"'+ templateID + '",param2:"REPORT-BUILDER-TEMPLATES-T63"}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res

	
#############################################################################################################
## Policies->Catalogs

def GetCatalogAllUsers():
    UCSD_API_OPNAME = "userAPIGetTabularReport"
    u = '{param0:"10",param1:"",param2:"CATALOG-T40"}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res

#############################################################################################################
## Workflows & Service Requests

def DoWorkflowRun(name="", params = dict()):
    UCSD_API_OPNAME = "userAPISubmitWorkflowServiceRequest"
    u = "{param0:\"" + name + '",' + 'param1:{' + ___APIworkflowParamsConstructor___(params) + '}' + ',param2:-1}'
    res = ___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
    if res["serviceError"] == null: return res
    return Null

def DoWorkflowRollback():
    UCSD_API_OPNAME = "userAPIRollbackWorkflow"
    u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"srId","value":' + ID + '}]}]}}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res	

def GetWorkflowList(folder=""):
    UCSD_API_OPNAME = "userAPIGetWorkflows"
    u = '{param0:{"list":[{"name":"folderName","value":"' + folder + '"}]}}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res
	
def GetWorkflowSteps(ID=0):
    UCSD_API_OPNAME = "userAPIGetWorkflowSteps"
    u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"requestId","value":' + ID + '}]}]}}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res	

def GetWorkflowStatus(ID=0):
    UCSD_API_OPNAME = "userAPIGetWorkflowStatus"
    u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"requestId","value":' + ID + '}]}]}}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res	

WorkflowStatus = {0:"EXECUTION_STATUS_NOT_STARTED", 1:"EXECUTION_STATUS_IN_PROGRESS", 2:"EXECUTION_STATUS_FAILED", 3:"EXECUTION_STATUS_COMPLETED", 4:"EXECUTION_STATUS_COMPLETED_WITH_WARNING", 5:"EXECUTION_STATUS_CANCELLED", 6:"EXECUTION_STATUS_PAUSED", 7:"EXECUTION_STATUS_SKIPPED",}

def GetWorkflowInputs(name=""):
    UCSD_API_OPNAME = "userAPIGetWorkflowInputs"
    u = '{param0:{"list":[{"name":"workflowName","value":"' + name + '"}]}}'
    res = ___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
    if res["serviceError"] == null: return res
    return Null

def GetWorkflowInputLOV(type=""):
    UCSD_API_OPNAME = "userAPIGetLOVValues"
    u = '{param0:{"list":[{"name":"type","value":"' + type + '"}]}}'
    res = ___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
    if res["serviceError"] == null: return res
    return Null
	
def GetWorkflowInputTable(type=""):
    UCSD_API_OPNAME = "userAPIGetLOVValues"
    u = '{param0:{"list":[{"name":"type","value":"' + type + '"}]}}'
    res = ___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
    if res["serviceError"] == null: return res
    return Null

#############################################################################################################
## some VM-related functions

def GetVMList():
    UCSD_API_OPNAME = "userAPIGetAllVMs"
    u = ""
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res

def DoVMaction(action, vmid, comstr=""):
    UCSD_API_OPNAME = "userAPIExecuteVMAction"
    allowed_actions = ["discardSaveState",
                       "pause",
                       "powerOff",
                       "powerOn",
                       "reboot",
                       "rebuildServer",
                       "repairVM",
                       "reset",
                       "resume",
                       "saveState",
                       "shutdownGuest",
                       "standby",
                       "suspend",
                       ]
    if (not any(action == a for a in generic_actions)): return "Action not valid"
    comments = 'API-VM-ACT-%s: "%s"' % (action, comstr)
    u = "{param0:\"" + vmid + '",' + 'param1:"' + action + '"' + ',param2:"' + comments + '"}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res['rows']

def GetVMcompletedActions(vmid):
    UCSD_API_OPNAME = "userAPIGetTabularReport"
    param0 = "3"
    param1 = vmid 
    param2 = "VM-ACTION-REQUESTS-T0"
    u = "{param0:\"" + param0 + '",' + 'param1:"' + param1 + '"' + ',param2:"' + param2 + '"}'
    res = ___APIpreparse___(___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
    return res['rows']

	
#############################################################################################################
## User functions
##
## NOTE: this is important, because many request results are auto-filtered based on user's context, which is
##       determined by the user name; If I understand the docs correctly, this call is used to impersonate a user:

def GetUserApiKey(user=""):
    UCSD_API_OPNAME = "userAPIGetRESTAccessKey"
    u = "{param0:\"" + user + '"}'
    res = ___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
    if res["serviceError"] == null: return res
    return Null
	
	
