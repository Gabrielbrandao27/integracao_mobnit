import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://172.233.15.239:10000/inspect",
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
