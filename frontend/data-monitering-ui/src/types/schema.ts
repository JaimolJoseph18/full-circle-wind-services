import type { components } from "./api"

export type APIModels = {
	DataReading: components["schemas"]["DataReadingWithApiLog"]
	LatestStats: components["schemas"]["DataReadingStats"]
	currentDayDataReadings: components["schemas"]["DataReading"]
}