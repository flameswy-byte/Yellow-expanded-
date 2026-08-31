Route138_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route138_EventScript_RouteSignLittlerootTown::
	msgbox Route138_Text_RouteSignLittlerootTown, MSGBOX_SIGN
	end

Route138_Text_RouteSignLittlerootTown:
	.string "ROUTE 138\n"
	.string "{LEFT_ARROW} LITTLEROOT TOWN$"

Route138_EventScript_RouteSignOldaleTown::
	msgbox Route138_Text_RouteSignOldaleTown, MSGBOX_SIGN
	end

Route138_Text_RouteSignOldaleTown:
	.string "ROUTE 138\n"
	.string "{LEFT_ARROW} OLDALE TOWN$"

