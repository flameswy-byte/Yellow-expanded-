Route144_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route144_EventScript_RouteSignFallarborTown::
	msgbox Route144_Text_RouteSignFallarborTown, MSGBOX_SIGN
	end

Route144_Text_RouteSignFallarborTown:
	.string "ROUTE 144\n"
	.string "{UP_ARROW} FALLARBOR TOWN$"

