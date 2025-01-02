import axiosInstance from "./axiosConfig";

export const fetchDashboardData = async () => {
  try {
    const response = await axiosInstance.get("inspect/"); // Replace with your endpoint
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    throw error;
  }
};
