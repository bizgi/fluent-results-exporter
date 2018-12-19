# encoding: utf-8
# @author: bizgi
# Release 18.1

"""
this code exports chart data into a .csv file for all cases in ansys workbench project.
"""

SetScriptVersion(Version="18.1.463")
print "Loading results..."

def exportData(case, caseName, path, cstFile):
	# exports all cases results in project.

	system1 = GetSystem(Name=case)
	results1 = system1.GetContainer(ComponentName="Results")
 
	# reset and update results before sending command
	resultsComponent1 = system1.GetComponent(Name="Results")
	resultsComponent1.Reset()
	resultsComponent1.Clean()
	resultsComponent1.Update(AllDependencies=True)	
	print "updated."
	
	cmdReadState = """
		>readstate filename=""" + cstFile + """, mode=append, load=false, keepexpressions=true
	"""
		
	cmdExport = """
		EXPORT:
		 Export File = """ + path + prjName[:-5] + """_files/user_files/""" + caseName + """.csv
		 Export Chart Name = Chart 1
		 Overwrite = On
		END
		>export chart
	"""
	
	# read state 
	try:
		results1.SendCommand(Command=cmdReadState)
	except:
		print "error! reset..."
		resultsComponent1 = system1.GetComponent(Name="Results")
		resultsComponent1.Reset()
		resultsComponent1.Clean()
		resultsComponent1.Update(AllDependencies=True)
		
	results1.SendCommand(Command=cmdReadState)
	
	# export chart data as csv file
	print "Export started..."

	results1.SendCommand(Command=cmdExport)
	print "Export completed."
	print "-----------------"
	results1.Exit()


#############################################################
# before run the script change path, prjName, cstName variables

# project folder path
path = 'D:/cfd-project/'

# project name
prjName = 'myProject.wbpj'

# cfd-post state file name
cstName = 'chart.cst'

# cst file must be in project folder root
cstFile = path + cstName

# open project
Open(FilePath=path+prjName)

# get all systems in project and export results
for system in GetAllSystems():
	case = system.Name
	caseName = system.DisplayText
	print case
	if "Post" not in case:
		ResultsId = system.Components[4].DataContainer.Name
		print ResultsId
		print caseName
		exportData(case, caseName, path, cstFile)

print "All results are exported."
