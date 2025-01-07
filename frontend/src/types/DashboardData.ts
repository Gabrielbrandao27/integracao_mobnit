export interface Report {
  payload: string;
}

export interface dappResponseData {
  status: string;
  exception_payload: null;
  reports: Report[];
  processed_input_count: number;
}

export type AvaiableFleetData = AvaiableFleetItem[];

export interface AvaiableFleetItem {
  id: number;
  line_id: string;
  expected_bus_amount: number;
  recorded_bus_amount: number;
}

export type TraveledKmData = TraveledKmItem[];

export interface TraveledKmItem {
  id: number;
  line_id: string;
  expected_traveled_distance_km: number;
  recorded_travel_distance_km: number;
}
