Route146_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route146_EventScript_RouteSignFortreeCity::
	msgbox Route146_Text_RouteSignFortreeCity, MSGBOX_SIGN
	end

Route146_Text_RouteSignFortreeCity:
	.string "ROUTE 146\n"
	.string "{UP_ARROW} FORTREE CITY$"

