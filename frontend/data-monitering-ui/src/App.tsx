import MoniteringDashboard from "./pages/Dashboard";
import "semantic-ui-css/semantic.min.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./App.css";

// Create a QueryClient instance
const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MoniteringDashboard />
    </QueryClientProvider>
  );
}

export default App;
