import { useState, useEffect, useMemo } from "react";
import { Grid, Icon, Table, Button } from "semantic-ui-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import {
  useStats,
  useListReadings,
  useGetReadingsforCurrentDay,
} from "../reactHooks";
import { StatCard } from "./StatCard";
import "./dashboard.scss";

const THRESHOLD = 90;
const PAGE_SIZE = 10;

interface TableRow {
  timestamp: string;
  value: number;
  endpoint: string;
  status: "Critical" | "Normal";
  email_sent: boolean;
};


export default function MoniteringDashboard() {
  const { data: stats, isLoading: statsLoading } = useStats()
  const { data: latestReading } = useStats()
  const currentValue = latestReading?.latest_value ?? null
  const currentTimestamp = latestReading?.latest_timestamp ?? null

  const avgValue = stats?.average_value?.toFixed(1) ?? "-"
  const totalCount = stats?.total_count ?? 0
  const maxVal = stats?.max_value ?? "-"
  const minVal = stats?.min_value ?? "-"
  const exceedances = stats?.threshold_exceeded_count ?? 0

  const { data: currentDayReadings } = useGetReadingsforCurrentDay()
  const [currentPage, setCurrentPage] = useState(0);
  const { data: history, refetch } = useListReadings(
    currentPage * PAGE_SIZE,
    PAGE_SIZE,
  );

  const tableData: TableRow[] = useMemo(() => {
    return (
      history?.map((r) => ({
        timestamp: r.timestamp,
        value: r.value,
        endpoint: r.api_endpoint || "-",
        status: r.value > THRESHOLD ? "Critical" : "Normal",
        email_sent: r.email_sent,
      })) ?? []
    );
  }, [history]);

  useEffect(() => {
    refetch();
  }, [currentPage, refetch]);

  const totalPages = Math.ceil((totalCount ?? 1) / PAGE_SIZE);

  const chartData = currentDayReadings
    ?.slice()
    .reverse()
    .map((d) => ({
      ...d,
      timestamp: d.timestamp,
      exceeds: d.value > THRESHOLD,
    }));

  return (
    <div className="monitering-container">
      <header className="dash-header">
        <h1>Full Circle Data Monitoring Dashboard</h1>
        <p>Real-Time System & Data Insights</p>
      </header>
      <Grid columns={4} stackable className="stats-row">
        <Grid.Column>
          <StatCard
            title="Average Data Value"
            value={statsLoading ? "-" : avgValue}
            subText={`${totalCount} Records`}
            icon="line graph"
          />
        </Grid.Column>
        <Grid.Column>
          <StatCard
            title="Max / Min - Data Value"
            value={statsLoading ? "- / -" : `${maxVal} / ${minVal}`}
            subText="High / Low values"
            icon="arrows alternate vertical"
          />
        </Grid.Column>
        <Grid.Column>
          <StatCard
            title="Exceedances"
            value={statsLoading ? "-" : exceedances}
            subText="Above threshold (90)"
            icon="warning circle"
            isAlert={exceedances > 0}
          />
        </Grid.Column>
        <Grid.Column>
          <StatCard
            title="Poll Interval"
            value="2s"
            subText="Frequency"
            icon="wait"
          />
        </Grid.Column>
      </Grid>

      <Grid stackable>
        <Grid.Column width={11}>
          <div className="chart-container card-style">
            <h3>Data Over Time (Today)</h3>
            {chartData?.length === 0 ? (
              <div className="empty-state">
                <p>No readings received today yet</p>
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={(t) => new Date(t).toLocaleTimeString()}
                    hide
                  />
                  <YAxis
                    domain={[
                      0,
                      Math.max(
                        ...(currentDayReadings?.map((d) => d.value) ?? [0]),
                        THRESHOLD + 10,
                      ),
                    ]}
                  />
                  <Tooltip
                    labelFormatter={(t) => new Date(t).toLocaleTimeString()}
                  />
                  <ReferenceLine
                    y={THRESHOLD}
                    label="Threshold"
                    stroke="red"
                    strokeDasharray="3 3"
                  />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="#5c5cff"
                    strokeWidth={2}
                    dot={false}
                  />
                  <Line
                    type="monotone"
                    dataKey="value"
                    stroke="red"
                    strokeWidth={0}
                    dot={(props) => {
                      const { cx, cy, payload } = props;
                      if (payload.exceeds)
                        return <circle cx={cx} cy={cy} r={4} fill="red" />;
                      return null;
                    }}
                    connectNulls={true}
                  />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </Grid.Column>

        <Grid.Column width={5}>
          <div className="current-value-container card-style">
            <div className="flex-between">
              <h3>Current Value</h3>
              <Icon name="pulse" color="green" />
            </div>
            <div className="live-display">
              <span className="latest-value">{currentValue ?? "--"}</span>
              {currentValue !== null &&
                currentValue !== undefined &&
                (currentValue > THRESHOLD ? (
                  <span className="critical-label">Critical</span>
                ) : (
                    <span className="normal-label"> Normal</span>
                ))}
            </div>
            <p className="timestamp">
              {currentTimestamp
                ? new Date(currentTimestamp).toLocaleTimeString()
                : "Connecting..."}
            </p>
          </div>
        </Grid.Column>
      </Grid>

      {/* Table */}
      <div className="table-container card-style">
        <h3>Recent Logs & Readings</h3>
        <Table basic="very" padded>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Timestamp</Table.HeaderCell>
              <Table.HeaderCell>Endpoint</Table.HeaderCell>
              <Table.HeaderCell>Value</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Email Status</Table.HeaderCell>
            </Table.Row>
          </Table.Header>

          <Table.Body>
            {tableData.map((row, i) => (
              <Table.Row
                key={i}
                negative={
                  typeof row.value === "number" && row.value > THRESHOLD
                }
              >
                <Table.Cell>
                  {new Date(row.timestamp).toLocaleString()}
                </Table.Cell>
                <Table.Cell>{row.endpoint}</Table.Cell>
                <Table.Cell>{row.value}</Table.Cell>
                <Table.Cell>
                  <span
                    style={{
                      color: row.status === "Critical" ? "red" : "green",
                      fontWeight: "bold",
                    }}
                  >
                    {row.status}
                  </span>
                </Table.Cell>
                <Table.Cell>
                  {row.email_sent ? (
                    <span style={{ color: "red", fontWeight: "bold" }}>
                      Email Sent
                    </span>
                  ) : (
                    "--"
                  )}
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>

        {/* Pagination */}
        <div className="pagination-controls">
          <Button
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 0))}
            disabled={currentPage === 0}
          >
            Previous
          </Button>
          <span style={{ margin: "0 10px" }}>
            Page {currentPage + 1} of {totalPages}
          </span>
          <Button
            onClick={() =>
              setCurrentPage((p) => Math.min(p + 1, totalPages - 1))
            }
            disabled={currentPage === totalPages - 1}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
