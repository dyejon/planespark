/* TODO: make a decent date struct */


typedef string Timestamp

struct SelectionChange {
    1: required i64 session_id,
    2: required i64 aircraft_id,
    3: required string hex_ident,
    4: required i64 flight_id,
    5: required Timestamp generated_timestamp,
    6: required Timestamp logged_timestamp,
    7: required string callsign,
}

union SBSMessage { 
    1: SelectionChange selection_change,
    /** 
      * 2: NewId new_id;
      * 3: NewAircraft new_aircraft;
      * 4: StatusAircraft status_aircraft;
      * 5: Click click;
      * 6: Transmission transmission;
     **/
}


/* vim: set ts=4 sw=4 expandtab: */
