import axios from "axios";
import type { APIModels } from "./types/schema";

const API_BASE = "http://localhost:8000/api/data-monitoring";

export const DataMonitoringAPI = {
  getStats: async (): Promise<APIModels["LatestStats"]> => {
    const res = await axios.get<APIModels["LatestStats"]>(`${API_BASE}/aggregates`);
    return res.data;
  },

  getreadingsforCurrentDay: async(): Promise<APIModels["DataReading"][]> => {
    const res = await axios.get<APIModels["DataReading"][]>(`${API_BASE}/readings/today`, {
    });
    return res.data;
  },

  getReadings: async (offset?: number, limit?: number): Promise<APIModels["DataReading"][]> => {
    const res = await axios.get<APIModels["DataReading"][]>(`${API_BASE}/history`, {
      params: { offset, limit },
    });
    return res.data;
  },
};
