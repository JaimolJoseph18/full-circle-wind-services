import { useQuery } from "@tanstack/react-query";
import { DataMonitoringAPI } from "./service";
import type { APIModels } from "./types/schema";

const POLLING_INTERVAL = 2000
export const useStats = () => {
  return useQuery<APIModels["LatestStats"], Error>({
    queryKey: ["latestStats"],
    queryFn: DataMonitoringAPI.getStats,
    staleTime: 0,
    refetchInterval: POLLING_INTERVAL, 
  });
};

export const useListReadings = (offset?: number, limit?: number) => {
  return useQuery<APIModels["DataReading"][], Error>({
    queryKey: ["historyReadings", offset, limit],
    queryFn: () => DataMonitoringAPI.getReadings(offset, limit),
    staleTime: 0,
    refetchInterval: POLLING_INTERVAL,
  });
};

export const useGetReadingsforCurrentDay = () => {
  return useQuery<APIModels["currentDayDataReadings"][], Error>({
    queryKey: ["currentDayReadings"],
    queryFn: () => DataMonitoringAPI.getreadingsforCurrentDay(),
    staleTime: 0,
    refetchInterval: POLLING_INTERVAL,
  });
};
