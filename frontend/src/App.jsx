export default function App() {
  return (
    <div className="min-h-screen flex flex-col p-8">
      <nav className="flex justify-between items-center mb-12">
        <h1 className="text-2xl font-bold bg-linear-to-r from-brand-accent to-brand-gradient bg-clip-text text-transparent">
          Trust Bank
        </h1>
        <button className="bg-brand-accent px-4 py-2 rounded-lg font-medium">Dashboard</button>
      </nav>
      
      <main className="flex-1">
        <div className="border border-white/10 bg-white/5 p-6 rounded-2xl">
          <p className="text-gray-400">Your content goes here...</p>
        </div>
      </main>
    </div>
  );
}
