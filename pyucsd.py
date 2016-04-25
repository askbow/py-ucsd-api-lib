'''
    Simple Python module for Cisco UCS Director reporting API
'''
import requests
import json

from helper import *
from ucsd_api_contexts import *

class UCSD:
    def __init__(self, host, adminKey):
	    # UCS Director:
	    self.UCSD_HOST    = host
	    self.UCSD_API_KEY_ADMIN = adminKey
	    self.UCSD_API_KEY = self.UCSD_API_KEY_ADMIN
		# request constructor:
	    self.UCSD_API_URL = "http://%s/app/api/rest?" # HTTPS?
	    self.UCSD_API_BASE_PARAMS = "formatType=json&opName=%s"
	    self.UCSD_API_OPDATA_PREP = "&opData="
	    self.HTTP_REQ_HEADERS = {"X-Cloupia-Request-Key":" "}
	    self.HTTP_REQ_HEADERS["X-Cloupia-Request-Key"] = self.UCSD_API_KEY
	    self.HTTP_UCSD_COOKIES = dict()
	    self.HTTP_UCSD_TIMEOUT = 3 # API call timeout in seconds
	    self.UCSD_API_WorkflowStatus = {0:"EXECUTION_STATUS_NOT_STARTED", 1:"EXECUTION_STATUS_IN_PROGRESS", 2:"EXECUTION_STATUS_FAILED", 3:"EXECUTION_STATUS_COMPLETED", 4:"EXECUTION_STATUS_COMPLETED_WITH_WARNING", 5:"EXECUTION_STATUS_CANCELLED", 6:"EXECUTION_STATUS_PAUSED", 7:"EXECUTION_STATUS_SKIPPED",}
	    self.UCSD_USERDIR = dict()
    def __repr__(self):
	    return "UCSD.API.WRAPPER(%s)" % self.UCSD_HOST
    #############################################################################################################
    ## basic API machinery
    def ___APIcall___(self,APIOP, params=""):
	    # returns a dictionary or None
	    url = self.UCSD_API_URL % (self.UCSD_HOST) + self.UCSD_API_BASE_PARAMS % (APIOP)
	    if not (params==""):
	        url = url + self.UCSD_API_OPDATA_PREP + params
	    try:
	        r = requests.get(url, headers=self.HTTP_REQ_HEADERS, cookies = self.HTTP_UCSD_COOKIES, timeout=self.HTTP_UCSD_TIMEOUT)
	    except: raise  # most useful during debugging
	    # exceptions to catch later: http://docs.python-requests.org/en/master/user/quickstart/#errors-and-exceptions
	    if r.status_code == requests.codes.ok:  
	        self.HTTP_UCSD_COOKIES = r.cookies # saving cookies 
	        #return r.text
	        if ('application/json' in r.headers.get('content-type')):
	            return ucsdJsonParser(r.text)
	        elif ('xml' in r.headers.get('content-type')):
	            return xml2dict(r.text)
	        else: return r.text      # to do: add logging
	    else: r.raise_for_status() # seems the most useful thing to do, while I'm debugging this; later will need to think of some better logic
        # requests.exceptions.HTTPError: 401 Client Error: Unauthorized
    
    def ___APIclearCookies___(self,):
        self.HTTP_UCSD_COOKIES = dict()
    
    def ___APIpreparse___(self,jj):
        return jj
		# Preparses the API reply contained in a dictionary
    	# returns a less-raw dictionary (serviceResult only) or None
        # need a more complex preparsing:
    	# - error / exception check, like "serviceError":null
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
    
    ####################################
    # TODO: params expander dict->json
    ####################################
    	
    #############################################################################################################	
    ## Contexts
        
    def ___GetContextList(self):
        UCSD_API_OPNAME = "userAPIGetAllContexts"
        u = ""
        res = self.___APIcall___(APIOP=UCSD_API_OPNAME, params=u)
        return res
        
    def GetContextList(self,):
        a = self.___GetContextList()
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult']
        except: return None
        return None
        
        
    #############################################################################################################	
    ## vDC
    
    def ___GetVDCList(self):
        UCSD_API_OPNAME = "userAPIGetAllVDCs"
        u = ""
        res = self.___APIcall___(APIOP=UCSD_API_OPNAME, params=u)
        return res
        
    def GetVDCList(self,):
        a = self.___GetVDCList()
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
     
        
    #############################################################################################################	
    ## Reporting General
    ## Doesn't work at the moment
    
    def ___GetReportsList(self,contextName, contextValue):
        UCSD_API_OPNAME = "userAPIGetAvailableReports"
        u =  "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '"}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP=UCSD_API_OPNAME, params=u))
        return res

    def GetReportsList(self,contextName, contextValue):
        a = self.___GetReportsList(contextName, contextValue)
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult']
        except: return None
        return None
		
    def ___PrintGetReportsAvailable___(self,res):
        for r in res:
    	    print "%s\t%s\t%s\n" % (r[u'reportLabel'],r[u'reportType'],r[u'reportId'])
    
    def GetReportTabular(self,contextName, contextValue, reportId):
        UCSD_API_OPNAME = "userAPIGetTabularReport"
        u = "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '", param2:"' + reportId + '"}'
        res = self.___APIcall___(APIOP=UCSD_API_OPNAME, params=u)
        return res
    
    def GetReportHistorical(self,contextName, contextValue, reportId, durationName):
        UCSD_API_OPNAME = "userAPIGetHistoricalReport"
        u = "{param0:\"" + contextName + '",' + 'param1:"' + contextValue + '", param2:"' + reportId + '", param3:"' +durationName + '"}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP=UCSD_API_OPNAME, params=u))
        return res
    
    #############################################################################################################
    ## Report Templates
    def ___GetReportsReportBuilderTemplates(self,):
        # Gets a list of all report templates in the system
        UCSD_API_OPNAME = "userAPIGetTabularReport"
        u = '{param0:"10",param1:"null",param2:"REPORT-BUILDER-TEMPLATES-T63"}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        return res	# {"Id":"templateID","Name":"some name","Description":"some description"}
    
    def GetReportsReportBuilderTemplates(self,):
        a = self.___GetReportsReportBuilderTemplates()
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
    
    
    def ___GetReportsReportBuilder(self,templateID):
        # Gets a table of reports generated using selected template	
        UCSD_API_OPNAME = "userAPIGetTabularReport"
        u = '{param0:"654",param1:"'+ templateID + '",param2:"CUSTOM-REPORTS-T63"}' # you get the same with "CLOUD_SENSE_REPORT_BUILDER_CUSTOM_REPORTS_REPORT"
        # 654 is some sort of "type"
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        return res
    
    def GetReportsReportBuilder(self,templateID):
        a = self.___GetReportsReportBuilder(templateID)
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
    	
    #############################################################################################################
    ## Policies->Catalogs
    
    def ___GetCatalogAllUsers(self,):
        UCSD_API_OPNAME = "userAPIGetTabularReport"
        u = '{param0:"10",param1:"",param2:"CATALOG-T40"}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res
    
    def GetCatalogAllUsers(self,):
        a = self.___GetCatalogAllUsers()
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
    
    
    #############################################################################################################
    ## Workflows & Service Requests
    
    def DoWorkflowRun(self,name="", params = dict()):
        UCSD_API_OPNAME = "userAPISubmitWorkflowServiceRequest"
        u = "{param0:\"" + name + '",' + 'param1:{' + ___APIworkflowParamsConstructor___(params) + '}' + ',param2:-1}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        if res["serviceError"] == null: return res
        return Null
    
    def DoWorkflowRollback(self,):
        UCSD_API_OPNAME = "userAPIRollbackWorkflow"
        u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"srId","value":' + ID + '}]}]}}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res	



    '''
    An example of two UCSD API calls to do the same thing - get the list of available workflows:
    userAPIGetWorkflows - parked in "Legacy tasks" directory in REST API browser:
    {"id":150,"name":"Firewall management","version":0,"description":"Firewall management","isActive":true,"contextType":0,"isSaveAsTasklet":false,"publishCompoundTaskOutputs":false,"startupWorkflow":false,"isNewFolder":false,"newFolderName":null,"existingFolderName":null,"noOfInputFields":0,"isLocked":false,"isHidden":false,"folderName":"HSS","activityName":null,"isActivity":false,"isSendEmailNotification":false,"emailIdList":"","emailPolicy":"No e-mail","emailIdListToNotify":"","lastValidatedTime":1459509586147,"lastValidatedStatus":"OK","isActiveVersion":true,"createdDateTime":0,"versionDescription":null,"userAssignedVersionTag":"0","lastModifiedDateTime":1459507782942}
    
    userAPIGetTabularReport WORKFLOWS-T46:
    {"Workflow_ID":150,"Workflow_Name":"Firewall management","Workflow_Description":"Firewall management","Validation_Status":"OK","Last_Validated":"2 weeks 6 days  ago","Compound_Task":"No","Version_Label":"0","Version":"version 0 (latest)","Workflow_Locked":"No","Workflow_Folder":"HSS"}
    '''         
    def ___GetWorkflowList(self,folder="", type="new"):
        UCSD_API_OPNAME = "userAPIGetWorkflows" # deprecated since UCSD Release 4.1 
		if type="new": UCSD_API_OPNAME = "userAPIGetWorkflowInputs"
        u = '{param0:"%s"}'%folder
        if type=="report":
            UCSD_API_OPNAME = "userAPIGetTabularReport"
            u = '{param0:"10",param1:"null",param2:"WORKFLOWS-T46"}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        return res
    
    def GetWorkflowList(self,folder="", type="report"):
        a = self.___GetWorkflowList()
        try:
            if a:
                if not (folder==""): filter = { u'Workflow_Folder': folder}
                else: filter = dict()
                if not a[u'serviceError']: return list_search(a[u'serviceResult'][u'rows'], filter)
        except: return None
        return None
    
    def GetWorkflowSteps(self,ID=0):
        UCSD_API_OPNAME = "userAPIGetWorkflowSteps"
        u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"requestId","value":' + ID + '}]}]}}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res	
    
    def GetWorkflowStatus(self,ID=0):
        UCSD_API_OPNAME = "userAPIGetWorkflowStatus"
        u = '{param0:{"list":[{"name":"APIServiceRequestParams","value":{"list":[{"name":"requestId","value":' + ID + '}]}]}}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res	
    
    
    
    def ___GetWorkflowInputs(self,name=""):
        UCSD_API_OPNAME = "userAPIGetWorkflowInputs"
        u = '{param0:"' + name + '"}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        return res
    
    def GetWorkflowInputs(self,name=""):
        a = self.___GetWorkflowInputs(name=name)
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'details']
        except: return None
        return None
    
    def GetWorkflowInputLOV(self,type=""):
        UCSD_API_OPNAME = "userAPIGetLOVValues"
        u = '{param0:{"list":[{"name":"type","value":"' + type + '"}]}}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        if res["serviceError"] == null: return res
        return Null
    	
    def GetWorkflowInputTable(self,type=""):
        UCSD_API_OPNAME = "userAPIGetLOVValues"
        u = '{param0:{"list":[{"name":"type","value":"' + type + '"}]}}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        if res["serviceError"] == null: return res
        return Null
    
    #############################################################################################################
    ## some VM-related functions
    
    def ___GetVMList(self,): # only works if called with admin privileges; other users receive HTTP401
        UCSD_API_OPNAME = "userAPIGetAllVMs"
        u = ""
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res

    def GetVMList(self):
        a = self.___GetVMList()
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None

    def DoVMaction(self,action, vmid, comstr=""): # ussue: this API call to my lab UCSD timeouts
        UCSD_API_OPNAME = "userAPIExecuteVMAction"
        generic_actions = ["discardSaveState",
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
        if (not any(action == a for a in generic_actions)): 
            return None
        comments = 'API-VM-ACT-%s: "%s"' % (action, comstr)
        u = "{param0:\"" + vmid + '",' + 'param1:"' + action + '"' + ',param2:"' + comments + '"}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res['rows']
    
    def ___GetVMcompletedActions(self,vmid):
        UCSD_API_OPNAME = "userAPIGetTabularReport"
        param0 = "3"
        param1 = vmid 
        param2 = "VM-ACTION-REQUESTS-T0"
        u = "{param0:\"" + param0 + '",' + 'param1:"' + param1 + '"' + ',param2:"' + param2 + '"}'
        res = self.___APIpreparse___(self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u))
        return res
    def GetVMcompletedActions(self,vmid):
        a = self.___GetVMcompletedActions(vmid)
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult'][u'rows']
        except: return None
        return None
    	
    #############################################################################################################
    ## User functions
    ##
    ## NOTE: this is important, because many request results are auto-filtered based on user's context, which is
    ##       determined by the user name; If I understand the docs correctly, this call may be used to impersonate a user:
    
    def ___GetUserApiKey(self,user=""):
        UCSD_API_OPNAME = "userAPIGetRESTAccessKey"
        u = "{param0:\"" + user + '"}'
        res = self.___APIcall___(APIOP = UCSD_API_OPNAME, params = u)
        return res
        #return Null
    
    def GetUserApiKey(self,user=""):
        a = self.___GetUserApiKey(user=user)
        try:
            if a:
                if not a[u'serviceError']: return a[u'serviceResult']
        except: return None
        return None
	
    def DoUserSave(self, user=""):
	    # this is a wrapper around GetUserApiKey(self,user="") to reuse the call results
		a = self.GetUserApiKey(user=user)
		try:
		    if a: 
			    self.UCSD_USERDIR[user] = dict()
			    self.UCSD_USERDIR[user]["key"] = a
			    #self.UCSD_USERDIR[user]["ucsd"] = UCSD(host = self.UCSD_HOST, adminKey = a)
			    pass
		    pass
		except: pass
	#

#