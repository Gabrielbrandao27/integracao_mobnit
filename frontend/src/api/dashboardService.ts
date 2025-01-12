import axiosInstance from "./axiosConfig";

export const fetchCompletedTripsData = async () => {
  try {
    const response = await axiosInstance.get("/numero_viagens");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};

export const fetchTraveledKmData = async () => {
  try {
    const response = await axiosInstance.get("/quilometragem_percorrida");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};

export const fetchClimatizationData = async () => {
  try {
    const response = await axiosInstance.get("/climatizacao");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};

export const fetchAvaiableFleetData = async () => {
  try {
    const response = await axiosInstance.get("/frota_disponivel");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};

export const fetchTotalSubsidy = async () => {
  try {
    const response = await axiosInstance.get("/subsidio_total");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};
