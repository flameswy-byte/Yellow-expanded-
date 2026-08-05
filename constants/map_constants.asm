MACRO map_const
	const \1
	DEF \1_WIDTH EQU \2
	DEF \1_HEIGHT EQU \3
ENDM

; "Indoor" maps are grouped sequentially (see data/maps/town_map_entries.asm)
DEF NUM_INDOOR_MAP_GROUPS EQU 0
MACRO end_indoor_group
	DEF INDOORGROUP_\1 EQU const_value
	REDEF NUM_INDOOR_MAP_GROUPS EQU NUM_INDOOR_MAP_GROUPS + 1
ENDM

; map ids
; indexes for:
; - MapHeaderBanks (see data/maps/map_header_banks.asm)
; - MapHeaderPointers (see data/maps/map_header_pointers.asm)
; - MapSongBanks (see data/maps/songs.asm)
; - ToggleableObjectMapPointers (see data/maps/toggleable_objects.asm)
; - MapSpriteSets (see data/maps/sprite_sets.asm)
; - ExternalMapEntries (see data/maps/town_map_entries.asm)
; - WildDataPointers (see data/wild/grass_water.asm)
; Each map also has associated data in maps.asm.
; Order: towns/cities, then routes, then indoor/dungeon maps
	const_def
	map_const PALLET_TOWN,                   10,  9 ; $00
	map_const VIRIDIAN_CITY,                 20, 18 ; $01
	map_const PEWTER_CITY,                   20, 18 ; $02
	map_const CERULEAN_CITY,                 20, 18 ; $03
	map_const LAVENDER_TOWN,                 10,  9 ; $04
	map_const VERMILION_CITY,                20, 18 ; $05
	map_const CELADON_CITY,                  25, 18 ; $06
	map_const FUCHSIA_CITY,                  20, 18 ; $07
	map_const CINNABAR_ISLAND,               10,  9 ; $08
	map_const INDIGO_PLATEAU,                10,  9 ; $09
	map_const SAFFRON_CITY,                  20, 18 ; $0A
DEF NUM_CITY_MAPS EQU const_value

	map_const UNUSED_MAP_0B,                  0,  0 ; $0B

DEF FIRST_ROUTE_MAP EQU const_value
	map_const ROUTE_1,                       10, 18 ; $0C
	map_const ROUTE_2,                       10, 36 ; $0D
	map_const ROUTE_3,                       35,  9 ; $0E
	map_const ROUTE_4,                       45,  9 ; $0F
	map_const ROUTE_5,                       10, 18 ; $10
	map_const ROUTE_6,                       10, 18 ; $11
	map_const ROUTE_7,                       10,  9 ; $12
	map_const ROUTE_8,                       30,  9 ; $13
	map_const ROUTE_9,                       30,  9 ; $14
	map_const ROUTE_10,                      10, 36 ; $15
	map_const ROUTE_11,                      30,  9 ; $16
	map_const ROUTE_12,                      10, 54 ; $17
	map_const ROUTE_13,                      30,  9 ; $18
	map_const ROUTE_14,                      10, 27 ; $19
	map_const ROUTE_15,                      30,  9 ; $1A
	map_const ROUTE_16,                      20,  9 ; $1B
	map_const ROUTE_17,                      10, 72 ; $1C
	map_const ROUTE_18,                      25,  9 ; $1D
	map_const ROUTE_19,                      10, 27 ; $1E
	map_const ROUTE_20,                      50,  9 ; $1F
	map_const ROUTE_21,                      10, 45 ; $20
	map_const ROUTE_22,                      20,  9 ; $21
	map_const ROUTE_23,                      10, 72 ; $22
	map_const ROUTE_24,                      10, 18 ; $23
	map_const ROUTE_25,                      30,  9 ; $24
	map_const CELADON_WOODS,                 22, 24 ; $25
	map_const ROUTE_26,                      22, 39 ; $26
	map_const ROUTE_27,                      20,  9 ; $27
	map_const ROUTE_28,                      20, 18 ; $28

DEF FIRST_INDOOR_MAP EQU const_value
	map_const REDS_HOUSE_1F,                  4,  4 ; $29
	map_const REDS_HOUSE_2F,                  4,  4 ; $2A
	map_const BLUES_HOUSE,                    4,  4 ; $2B
	map_const OAKS_LAB,                       5,  6 ; $2C
	end_indoor_group PALLET_TOWN

	map_const VIRIDIAN_POKECENTER,            7,  4 ; $2D
	map_const VIRIDIAN_MART,                  4,  4 ; $2E
	map_const VIRIDIAN_SCHOOL_HOUSE,          4,  4 ; $2F
	map_const VIRIDIAN_NICKNAME_HOUSE,        4,  4 ; $30
	map_const VIRIDIAN_GYM,                  10,  9 ; $31
	end_indoor_group VIRIDIAN_CITY

	map_const DIGLETTS_CAVE_ROUTE_2,          4,  4 ; $32
	map_const VIRIDIAN_FOREST_NORTH_GATE,     5,  4 ; $33
	map_const ROUTE_2_TRADE_HOUSE,            4,  4 ; $34
	map_const ROUTE_2_GATE,                   5,  4 ; $35
	map_const VIRIDIAN_FOREST_SOUTH_GATE,     5,  4 ; $36
	end_indoor_group ROUTE_2

	map_const VIRIDIAN_FOREST,               17, 24 ; $37
	end_indoor_group VIRIDIAN_FOREST

	map_const MUSEUM_1F,                     10,  4 ; $38
	map_const MUSEUM_2F,                      7,  4 ; $39
	map_const PEWTER_GYM,                     5,  7 ; $3A
	map_const PEWTER_NIDORAN_HOUSE,           4,  4 ; $3B
	map_const PEWTER_MART,                    4,  4 ; $3C
	map_const PEWTER_SPEECH_HOUSE,            4,  4 ; $3D
	map_const PEWTER_POKECENTER,              7,  4 ; $3E
	end_indoor_group PEWTER_CITY

	map_const MT_MOON_1F,                    20, 18 ; $3F
	map_const MT_MOON_B1F,                   14, 14 ; $40
	map_const MT_MOON_B2F,                   20, 18 ; $41
	end_indoor_group MT_MOON

	map_const CERULEAN_TRASHED_HOUSE,         4,  4 ; $42
	map_const CERULEAN_MELANIES_HOUSE,        4,  4 ; $43
	map_const CERULEAN_POKECENTER,            7,  4 ; $44
	map_const CERULEAN_GYM,                   5,  7 ; $45
	map_const BIKE_SHOP,                      4,  4 ; $46
	map_const CERULEAN_MART,                  4,  4 ; $47
	end_indoor_group CERULEAN_CITY

	map_const MT_MOON_POKECENTER,             7,  4 ; $48
	end_indoor_group ROUTE_4

	map_const CERULEAN_TRASHED_HOUSE_COPY,    4,  4 ; $49
	end_indoor_group CERULEAN_CITY_2

	map_const ROUTE_5_GATE,                   4,  3 ; $4A
	map_const UNDERGROUND_PATH_ROUTE_5,       4,  4 ; $4B
	map_const DAYCARE,                        4,  4 ; $4C
	end_indoor_group ROUTE_5

	map_const ROUTE_6_GATE,                   4,  3 ; $4D
	map_const UNDERGROUND_PATH_ROUTE_6,       4,  4 ; $4E
	map_const UNDERGROUND_PATH_ROUTE_6_COPY,  4,  4 ; $4F
	end_indoor_group ROUTE_6

	map_const ROUTE_7_GATE,                   3,  4 ; $50
	map_const UNDERGROUND_PATH_ROUTE_7,       4,  4 ; $51
	map_const UNDERGROUND_PATH_ROUTE_7_COPY,  4,  4 ; $52
	end_indoor_group ROUTE_7

	map_const ROUTE_8_GATE,                   3,  4 ; $53
	map_const UNDERGROUND_PATH_ROUTE_8,       4,  4 ; $54
	end_indoor_group ROUTE_8

	map_const ROCK_TUNNEL_POKECENTER,         7,  4 ; $55
	map_const ROCK_TUNNEL_1F,                20, 18 ; $56
	end_indoor_group ROCK_TUNNEL

	map_const POWER_PLANT,                   20, 18 ; $57
	end_indoor_group POWER_PLANT

	map_const ROUTE_11_GATE_1F,               4,  5 ; $58
	map_const DIGLETTS_CAVE_ROUTE_11,         4,  4 ; $59
	map_const ROUTE_11_GATE_2F,               4,  4 ; $5A
	end_indoor_group ROUTE_11

	map_const ROUTE_12_GATE_1F,               5,  4 ; $5B
	end_indoor_group ROUTE_12

	map_const BILLS_HOUSE,                    4,  4 ; $5C
	end_indoor_group SEA_COTTAGE

	map_const VERMILION_POKECENTER,           7,  4 ; $5D
	map_const POKEMON_FAN_CLUB,               4,  4 ; $5E
	map_const VERMILION_MART,                 4,  4 ; $5F
	map_const VERMILION_GYM,                  5,  9 ; $60
	map_const VERMILION_PIDGEY_HOUSE,         4,  4 ; $61
	map_const VERMILION_DOCK,                14,  6 ; $62
	end_indoor_group VERMILION_CITY

	map_const SS_ANNE_1F,                    20,  9 ; $63
	map_const SS_ANNE_2F,                    20,  9 ; $64
	map_const SS_ANNE_3F,                    10,  3 ; $65
	map_const SS_ANNE_B1F,                   15,  4 ; $66
	map_const SS_ANNE_BOW,                   10,  7 ; $67
	map_const SS_ANNE_KITCHEN,                7,  8 ; $68
	map_const SS_ANNE_CAPTAINS_ROOM,          3,  4 ; $69
	map_const SS_ANNE_1F_ROOMS,              12,  8 ; $6A
	map_const SS_ANNE_2F_ROOMS,              12,  8 ; $6B
	map_const SS_ANNE_B1F_ROOMS,             12,  8 ; $6C
	end_indoor_group SS_ANNE

	map_const VICTORY_ROAD_1F,               10,  9 ; $6D
	end_indoor_group VICTORY_ROAD

	map_const UNUSED_MAP_6F,                  0,  0 ; $6E
	map_const LANCES_ROOM,                   13, 13 ; $6F
	map_const HALL_OF_FAME,                   5,  4 ; $70
	end_indoor_group POKEMON_LEAGUE

	map_const UNDERGROUND_PATH_NORTH_SOUTH,   4, 24 ; $71 ; UndergroundPathNorthSouth.blk is actually 4x23
	end_indoor_group UNDERGROUND_PATH

	map_const CHAMPIONS_ROOM,                 4,  4 ; $72
	end_indoor_group POKEMON_LEAGUE_2

	map_const UNDERGROUND_PATH_WEST_EAST,    25,  4 ; $73
	end_indoor_group UNDERGROUND_PATH_2

	map_const CELADON_MART_1F,               10,  4 ; $74
	map_const CELADON_MART_2F,               10,  4 ; $75
	map_const CELADON_MART_3F,               10,  4 ; $76
	map_const CELADON_MART_4F,               10,  4 ; $77
	map_const CELADON_MART_ROOF,             10,  4 ; $78
	map_const CELADON_MART_ELEVATOR,          2,  2 ; $79
	map_const CELADON_MANSION_1F,             4,  6 ; $7A
	map_const CELADON_MANSION_2F,             4,  6 ; $7B
	map_const CELADON_MANSION_3F,             4,  6 ; $7C
	map_const CELADON_MANSION_ROOF,           4,  6 ; $7D
	map_const CELADON_MANSION_ROOF_HOUSE,     4,  4 ; $7E
	map_const CELADON_POKECENTER,             7,  4 ; $7F
	map_const CELADON_GYM,                    5,  9 ; $80
	map_const GAME_CORNER,                   10,  9 ; $81
	map_const CELADON_MART_5F,               10,  4 ; $82
	map_const GAME_CORNER_PRIZE_ROOM,         5,  4 ; $83
	map_const CELADON_DINER,                  5,  4 ; $84
	map_const CELADON_CHIEF_HOUSE,            4,  4 ; $85
	map_const CELADON_HOTEL,                  7,  4 ; $86
	end_indoor_group CELADON_CITY

	map_const LAVENDER_POKECENTER,            7,  4 ; $87
	end_indoor_group LAVENDER_TOWN

	map_const POKEMON_TOWER_1F,              10,  9 ; $88
	map_const POKEMON_TOWER_2F,              10,  9 ; $89
	map_const POKEMON_TOWER_3F,              10,  9 ; $8A
	map_const POKEMON_TOWER_4F,              10,  9 ; $8B
	map_const POKEMON_TOWER_5F,              10,  9 ; $8C
	map_const POKEMON_TOWER_6F,              10,  9 ; $8D
	map_const POKEMON_TOWER_7F,              10,  9 ; $8E
	end_indoor_group POKEMON_TOWER

	map_const MR_FUJIS_HOUSE,                 4,  4 ; $8F
	map_const LAVENDER_MART,                  4,  4 ; $90
	map_const LAVENDER_CUBONE_HOUSE,          4,  4 ; $91
	end_indoor_group LAVENDER_TOWN_2

	map_const FUCHSIA_MART,                   4,  4 ; $92
	map_const FUCHSIA_BILLS_GRANDPAS_HOUSE,   4,  4 ; $93
	map_const FUCHSIA_POKECENTER,             7,  4 ; $94
	map_const WARDENS_HOUSE,                  5,  4 ; $95
	end_indoor_group FUCHSIA_CITY

	map_const SAFARI_ZONE_GATE,               4,  3 ; $96
	end_indoor_group SAFARI_ZONE

	map_const FUCHSIA_GYM,                    5,  9 ; $97
	map_const FUCHSIA_MEETING_ROOM,           7,  4 ; $98
	end_indoor_group FUCHSIA_CITY_2

	map_const SEAFOAM_ISLANDS_B1F,           15,  9 ; $99
	map_const SEAFOAM_ISLANDS_B2F,           15,  9 ; $9A
	map_const SEAFOAM_ISLANDS_B3F,           15,  9 ; $9B
	map_const SEAFOAM_ISLANDS_B4F,           15,  9 ; $9C
	end_indoor_group SEAFOAM_ISLANDS

	map_const VERMILION_OLD_ROD_HOUSE,        4,  4 ; $9D
	end_indoor_group VERMILION_CITY_2

	map_const FUCHSIA_GOOD_ROD_HOUSE,         4,  4 ; $9E
	end_indoor_group FUCHSIA_CITY_3

	map_const POKEMON_MANSION_1F,            15, 14 ; $9F
	end_indoor_group POKEMON_MANSION

	map_const CINNABAR_GYM,                  10,  9 ; $A0
	map_const CINNABAR_LAB,                   9,  4 ; $A1
	map_const CINNABAR_LAB_TRADE_ROOM,        4,  4 ; $A2
	map_const CINNABAR_LAB_METRONOME_ROOM,    4,  4 ; $A3
	map_const CINNABAR_LAB_FOSSIL_ROOM,       4,  4 ; $A4
	map_const CINNABAR_POKECENTER,            7,  4 ; $A5
	map_const CINNABAR_MART,                  4,  4 ; $A6
	map_const CINNABAR_MART_COPY,             4,  4 ; $A7
	end_indoor_group CINNABAR_ISLAND

	map_const INDIGO_PLATEAU_LOBBY,           8,  6 ; $A8
	end_indoor_group INDIGO_PLATEAU

	map_const COPYCATS_HOUSE_1F,              4,  4 ; $A9
	map_const COPYCATS_HOUSE_2F,              4,  4 ; $AA
	map_const FIGHTING_DOJO,                  5,  6 ; $AB
	map_const SAFFRON_GYM,                   10,  9 ; $AC
	map_const SAFFRON_PIDGEY_HOUSE,           4,  4 ; $AD
	map_const SAFFRON_MART,                   4,  4 ; $AE
	map_const SILPH_CO_1F,                   15,  9 ; $AF
	map_const SAFFRON_POKECENTER,             7,  4 ; $B0
	map_const MR_PSYCHICS_HOUSE,              4,  4 ; $B1
	end_indoor_group SAFFRON_CITY

	map_const ROUTE_15_GATE_1F,               4,  5 ; $B2
	map_const ROUTE_15_GATE_2F,               4,  4 ; $B3
	end_indoor_group ROUTE_15

	map_const ROUTE_16_GATE_1F,               4,  7 ; $B4
	map_const ROUTE_16_GATE_2F,               4,  4 ; $B5
	map_const ROUTE_16_FLY_HOUSE,             4,  4 ; $B6
	end_indoor_group ROUTE_16

	map_const ROUTE_12_SUPER_ROD_HOUSE,       4,  4 ; $B7
	end_indoor_group ROUTE_12_2

	map_const ROUTE_18_GATE_1F,               4,  5 ; $B8
	map_const ROUTE_18_GATE_2F,               4,  4 ; $B9
	end_indoor_group ROUTE_18

	map_const SEAFOAM_ISLANDS_1F,            15,  9 ; $BA
	end_indoor_group SEAFOAM_ISLANDS_2

	map_const ROUTE_22_GATE,                  5,  4 ; $BB
	end_indoor_group ROUTE_22

	map_const VICTORY_ROAD_2F,               15,  9 ; $BC
	end_indoor_group VICTORY_ROAD_2

	map_const ROUTE_12_GATE_2F,               4,  4 ; $BD
	end_indoor_group ROUTE_12_3

	map_const VERMILION_TRADE_HOUSE,          4,  4 ; $BE
	end_indoor_group VERMILION_CITY_3

	map_const DIGLETTS_CAVE,                 20, 18 ; $BF
	end_indoor_group DIGLETTS_CAVE

	map_const VICTORY_ROAD_3F,               15,  9 ; $C0
	end_indoor_group VICTORY_ROAD_3

	map_const ROCKET_HIDEOUT_B1F,            15, 14 ; $C1
	map_const ROCKET_HIDEOUT_B2F,            15, 14 ; $C2
	map_const ROCKET_HIDEOUT_B3F,            15, 14 ; $C3
	map_const ROCKET_HIDEOUT_B4F,            15, 12 ; $C4
	map_const ROCKET_HIDEOUT_ELEVATOR,        3,  4 ; $C5
	end_indoor_group ROCKET_HQ

	map_const SILPH_CO_2F,                   15,  9 ; $C6
	map_const SILPH_CO_3F,                   15,  9 ; $C7
	map_const SILPH_CO_4F,                   15,  9 ; $C8
	map_const SILPH_CO_5F,                   15,  9 ; $C9
	map_const SILPH_CO_6F,                   13,  9 ; $CA
	map_const SILPH_CO_7F,                   13,  9 ; $CB
	map_const SILPH_CO_8F,                   13,  9 ; $CC
	end_indoor_group SILPH_CO

	map_const POKEMON_MANSION_2F,            15, 14 ; $CD
	map_const POKEMON_MANSION_3F,            15,  9 ; $CE
	map_const POKEMON_MANSION_B1F,           15, 14 ; $CF
	end_indoor_group POKEMON_MANSION_2

	map_const SAFARI_ZONE_EAST,              15, 13 ; $D0
	map_const SAFARI_ZONE_NORTH,             20, 18 ; $D1
	map_const SAFARI_ZONE_WEST,              15, 13 ; $D2
	map_const SAFARI_ZONE_CENTER,            15, 13 ; $D3
	map_const SAFARI_ZONE_CENTER_REST_HOUSE,  4,  4 ; $D4
	map_const SAFARI_ZONE_SECRET_HOUSE,       4,  4 ; $D5
	map_const SAFARI_ZONE_WEST_REST_HOUSE,    4,  4 ; $D6
	map_const SAFARI_ZONE_EAST_REST_HOUSE,    4,  4 ; $D7
	map_const SAFARI_ZONE_NORTH_REST_HOUSE,   4,  4 ; $D8
	end_indoor_group SAFARI_ZONE_2

	map_const CERULEAN_CAVE_2F,              15,  9 ; $D9
	map_const CERULEAN_CAVE_B1F,             15,  9 ; $DA
	map_const CERULEAN_CAVE_1F,              15,  9 ; $DB
	end_indoor_group CERULEAN_CAVE

	map_const NAME_RATERS_HOUSE,              4,  4 ; $DC
	end_indoor_group LAVENDER_TOWN_3

	map_const CERULEAN_BADGE_HOUSE,           4,  4 ; $DD
	end_indoor_group CERULEAN_CITY_3

	map_const ROCK_TUNNEL_B1F,               20, 18 ; $DE
	end_indoor_group ROCK_TUNNEL_2

	map_const SILPH_CO_9F,                   13,  9 ; $DF
	map_const SILPH_CO_10F,                   8,  9 ; $E0
	map_const SILPH_CO_11F,                   9,  9 ; $E1
	map_const SILPH_CO_ELEVATOR,              2,  2 ; $E2
	end_indoor_group SILPH_CO_2

	map_const UNUSED_MAP_ED,                  0,  0 ; $E3
	map_const TRADE_CENTER,                   5,  4 ; $E4
	map_const COLOSSEUM,                      5,  4 ; $E5
	map_const UNUSED_MAP_F4,                  0,  0 ; $E6
	map_const LORELEIS_ROOM,                  5,  6 ; $E7
	map_const BRUNOS_ROOM,                    5,  6 ; $E8
	map_const AGATHAS_ROOM,                   5,  6 ; $E9
	end_indoor_group POKEMON_LEAGUE_3

	map_const SUMMER_BEACH_HOUSE,             7,  4 ; $EA
	end_indoor_group ROUTE_19
DEF NUM_MAPS EQU const_value

; Indoor maps, such as houses, use this as the Map ID in their exit warps
; This map ID takes the player back to the last outdoor map they were on, stored in wLastMap
DEF LAST_MAP EQU $ff

ASSERT NUM_MAPS <= LAST_MAP, "map IDs overlap LAST_MAP"
