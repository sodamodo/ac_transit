    enum ScheduleRelationship {
      // The vehicle is proceeding in accordance with its static schedule of
      // stops, although not necessarily according to the times of the schedule.
      // At least one of arrival and departure must be provided. If the schedule
      // for this stop contains both arrival and departure times then so must
      // this update. Frequency-based trips (GTFS frequencies.txt with exact_times = 0)
      // should not have a SCHEDULED value and should use UNSCHEDULED instead.
      SCHEDULED = 0;

      // The stop is skipped, i.e., the vehicle will not stop at this stop.
      // Arrival and departure are optional.
      SKIPPED = 1;

      // No data is given for this stop. The main intention for this value is to
      // give the predictions only for part of a trip, i.e., if the last update
      // for a trip has a NO_DATA specifier, then StopTimes for the rest of the
      // stops in the trip are considered to be unspecified as well.
      // Neither arrival nor departure should be supplied.
      NO_DATA = 2;

      // The vehicle is operating a trip defined in GTFS frequencies.txt with exact_times = 0.
      // This value should not be used for trips that are not defined in GTFS frequencies.txt,
      // or trips in GTFS frequencies.txt with exact_times = 1. Trips containing StopTimeUpdates
      // with ScheduleRelationship=UNSCHEDULED must also set TripDescriptor.ScheduleRelationship=UNSCHEDULED.
      // NOTE: This field is still experimental, and subject to change. It may be
      // formally adopted in the future.
      UNSCHEDULED = 3;
    }

    enum VehicleStopStatus {
    // The vehicle is just about to arrive at the stop (on a stop
    // display, the vehicle symbol typically flashes).
    INCOMING_AT = 0;

    // The vehicle is standing at the stop.
    STOPPED_AT = 1;

    // The vehicle has departed and is in transit to the next stop.
    IN_TRANSIT_TO = 2;
  }
  // The exact status of the vehicle with respect to the current stop.
  // Ignored if current_stop_sequence is missing.
  optional VehicleStopStatus current_status = 4 [default = IN_TRANSIT_TO];

  // Moment at which the vehicle's position was measured. In POSIX time
  // (i.e., number of seconds since January 1st 1970 00:00:00 UTC).
  optional uint64 timestamp = 5;


  enum OccupancyStatus {
    // The vehicle or carriage is considered empty by most measures, and has few or no
    // passengers onboard, but is still accepting passengers.
    EMPTY = 0;

    // The vehicle or carriage has a relatively large percentage of seats available.
    // What percentage of free seats out of the total seats available is to be
    // considered large enough to fall into this category is determined at the
    // discretion of the producer.
    MANY_SEATS_AVAILABLE = 1;

    // The vehicle or carriage has a relatively small percentage of seats available.
    // What percentage of free seats out of the total seats available is to be
    // considered small enough to fall into this category is determined at the
    // discretion of the feed producer.
    FEW_SEATS_AVAILABLE = 2;

    // The vehicle or carriage can currently accommodate only standing passengers.
    STANDING_ROOM_ONLY = 3;

    // The vehicle or carriage can currently accommodate only standing passengers
    // and has limited space for them.
    CRUSHED_STANDING_ROOM_ONLY = 4;

    // The vehicle or carriage is considered full by most measures, but may still be
    // allowing passengers to board.
    FULL = 5;

    // The vehicle or carriage is not accepting passengers, but usually accepts passengers for boarding.
    NOT_ACCEPTING_PASSENGERS = 6;

    // The vehicle or carriage doesn't have any occupancy data available at that time.
    NO_DATA_AVAILABLE = 7;

    // The vehicle or carriage is not boardable and never accepts passengers.
    // Useful for special vehicles or carriages (engine, maintenance carriage, etc…).
    NOT_BOARDABLE = 8;

  }
  // If multi_carriage_status is populated with per-carriage OccupancyStatus,
  // then this field should describe the entire vehicle with all carriages accepting passengers considered.
  optional OccupancyStatus occupancy_status = 9;

  // A percentage value representing the degree of passenger occupancy of the vehicle.
  // The values are represented as an integer without decimals. 0 means 0% and 100 means 100%.
  // The value 100 should represent the total maximum occupancy the vehicle was designed for,
  // including both seated and standing capacity, and current operating regulations allow.
  // It is possible that the value goes over 100 if there are currently more passengers than what the vehicle was designed for.
  // The precision of occupancy_percentage should be low enough that you can't track a single person boarding and alighting for privacy reasons.
  // If multi_carriage_status is populated with per-carriage occupancy_percentage, 
  // then this field should describe the entire vehicle with all carriages accepting passengers considered.
  // This field is still experimental, and subject to change. It may be formally adopted in the future.
  optional uint32 occupancy_percentage = 10;

  // Carriage specific details, used for vehicles composed of several carriages
  // This message/field is still experimental, and subject to change. It may be formally adopted in the future.