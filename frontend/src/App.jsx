import { useState, useEffect } from "react";

function App() {
  // define satate app memory
  const [jobs, setJobs] = useState([]);

  //zdefine the effect, the trigger
useEffect(() => {
    fetch('http://127.0.0.1:8000/jobs')
      .then(response => response.json())
      .then(data => setJobs(data))
      .catch(err => console.error("Kitchen is closed!", err));
  }, []);
  // 3. The Visual Layout (The Dining Room)
  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">Hustle Tracker</h1>

      {/* If jobs list is empty, show a message */}
      {jobs.length === 0 ? (
        <p className="text-gray-500">No jobs found. Time to start bidding!</p>
      ) : (
        /* If jobs exist, map through them */
        <div className="grid gap-4">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="p-4 bg-white shadow rounded-lg border-l-4 border-blue-500"
            >
              <h2 className="font-bold text-xl">{job.title}</h2>
              <p className="text-gray-600">
                {job.platform} — ${job.budget}
              </p>
              <p className="text-sm text-gray-400">Status: {job.status}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
