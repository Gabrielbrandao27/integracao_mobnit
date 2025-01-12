export interface Report {
  payload: string;
}

export interface dappResponseData {
  status: string;
  exception_payload: null;
  reports: Report[];
  processed_input_count: number;
}

export type TripsCompletedData = TripsCompletedItem[];

export interface TripsCompletedItem {
  id: number;
  consorcium: string;
  expected_trips: number;
  recorded_trips: number;
  conclusion_percentage: number;
  subsidy: number;
  date: string;
}

export type TraveledKmData = TraveledKmItem[];

export interface TraveledKmItem {
  id: number;
  consorcium: string;
  expected_traveled_distance_km: number;
  recorded_travel_distance_km: number;
  conclusion_percentage: number;
  subsidy: number;
  date: string;
}

export type ClimatizationData = ClimatizationItem[];

export interface ClimatizationItem {
  id: number;
  consorcium: string;
  total_busses: number;
  busses_without_climatization: number;
  conclusion_percentage: number;
  subsidy: number;
  date: string;
}

export type AvaiableFleetData = AvaiableFleetItem[];

export interface AvaiableFleetItem {
  id: number;
  consorcium: string;
  expected_bus_amount: number;
  recorded_bus_amount: number;
  conclusion_percentage: number;
  subsidy: number;
  date: string;
}

export type TotalSubsidyData = TotalSubsidyItem[];

export interface TotalSubsidyItem {
  id: number;
  consorcium: string;
  total_subsidy: number;
  date: string;
}
