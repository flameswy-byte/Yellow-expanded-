Route135_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route135_EventScript_RouteSignLittlerootTown::
	msgbox Route135_Text_RouteSignLittlerootTown, MSGBOX_SIGN
	end

Route135_Text_RouteSignLittlerootTown:
	.string "ROUTE 135\n"
	.string "{RIGHT_ARROW} LITTLEROOT TOWN$"

Route135_EventScript_RouteSignPetalburgCity::
	msgbox Route135_Text_RouteSignPetalburgCity, MSGBOX_SIGN
	end

Route135_Text_RouteSignPetalburgCity:
	.string "ROUTE 135\n"
	.string "{UP_ARROW} PETALBURG CITY$"

