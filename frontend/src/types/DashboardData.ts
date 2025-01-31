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
  trips_scheduled: number;
  trips_completed: number;
  conclusion_percentage: number;
  subsidy: number;
  date: string;
}

export type TraveledKmData = TraveledKmItem[];

export interface TraveledKmItem {
  id: number;
  consorcium: string;
  km_scheduled: number;
  km_completed: number;
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

export type AvailableFleetData = AvailableFleetItem[];

export interface AvailableFleetItem {
  id: number;
  consorcium: string;
  scheduled_fleets: number;
  recorded_fleets: number;
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
