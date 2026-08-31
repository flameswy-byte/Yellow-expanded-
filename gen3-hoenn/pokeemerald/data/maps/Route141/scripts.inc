Route141_MapScripts::
	.byte 0

// Open Hoenn - tools/populate.py

Route141_EventScript_RouteSignRustboroCity::
	msgbox Route141_Text_RouteSignRustboroCity, MSGBOX_SIGN
	end

Route141_Text_RouteSignRustboroCity:
	.string "ROUTE 141\n"
	.string "{LEFT_ARROW} RUSTBORO CITY$"

Route141_EventScript_RouteSignVerdanturfTown::
	msgbox Route141_Text_RouteSignVerdanturfTown, MSGBOX_SIGN
	end

Route141_Text_RouteSignVerdanturfTown:
	.string "ROUTE 141\n"
	.string "{RIGHT_ARROW} VERDANTURF TOWN$"

