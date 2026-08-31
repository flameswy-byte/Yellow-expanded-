Route139_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route139_EventScript_RouteSignVerdanturfTown::
	msgbox Route139_Text_RouteSignVerdanturfTown, MSGBOX_SIGN
	end

Route139_Text_RouteSignVerdanturfTown:
	.string "ROUTE 139\n"
	.string "{UP_ARROW} VERDANTURF TOWN$"

