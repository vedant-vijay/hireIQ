import { useState } from 'react'
import './App.css'

function App() {
  const [currentJob, setCurrentJob] = useState(null)
  const [candidates, setCandidates] = useState([])
  const [rankings, setRankings] = useState([])
  const [langGraphRankings, setLangGraphRankings] = useState([])

  const [jobTitle, setJobTitle] = useState('')
  const [jobDesc, setJobDesc] = useState('')

  const [candName, setCandName] = useState('')
  const [candEmail, setCandEmail] = useState('')
  const [candResume, setCandResume] = useState('')

  const createJob = async () => {
    const res = await fetch('http://localhost:8000/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: jobTitle, description: jobDesc })
    })
    const data = await res.json()
    setCurrentJob(data)
  }

  const addCandidate = async () => {
    const res = await fetch('http://localhost:8000/candidates', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: candName, email: candEmail, resume_text: candResume, job_id: currentJob.id })
    })
    const data = await res.json()
    setCandidates([...candidates, data])
    setCandName('')
    setCandEmail('')
    setCandResume('')
  }

  const screenAll = async () => {
    for (const candidate of candidates) {
      await fetch('http://localhost:8000/screening', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_id: currentJob.id, candidate_id: candidate.id })
      })
    }
    const res = await fetch(`http://localhost:8000/screening/rankings/${currentJob.id}`)
    const data = await res.json()
    setRankings(data)
  }

  const screenWithLangGraph = async () => {
    for (const candidate of candidates) {
      await fetch('http://localhost:8000/screening-graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_id: currentJob.id, candidate_id: candidate.id })
      })
    }
    const res = await fetch(`http://localhost:8000/screening/rankings/${currentJob.id}`)
    const data = await res.json()
    setLangGraphRankings(data)
  }

  const RankingTable = ({ data, title }) => (
    <div style={{ padding: '20px', border: '1px solid #ccc', marginBottom: '20px' }}>
      <h2>{title}</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Rank</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Name</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Score</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Recommendation</th>
            <th style={{ border: '1px solid #ccc', padding: '8px' }}>Reasoning</th>
          </tr>
        </thead>
        <tbody>
          {data.map((r, index) => {
            const candidate = candidates.find(c => c.id === r.candidate_id)
            return (
              <tr key={r.id}>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>#{index + 1}</td>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{candidate?.name}</td>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{r.match_score}</td>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{r.recommendation}</td>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>{r.reasoning}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <h1>HireIQ — AI Resume Screener</h1>

      {/* STEP 1 */}
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc' }}>
        <h2>Step 1 — Create Job</h2>
        <input placeholder="Job Title" value={jobTitle} onChange={e => setJobTitle(e.target.value)} style={{ display: 'block', marginBottom: '10px', width: '100%' }} />
        <textarea placeholder="Job Description" value={jobDesc} onChange={e => setJobDesc(e.target.value)} style={{ display: 'block', marginBottom: '10px', width: '100%', height: '100px' }} />
        <button onClick={createJob}>Create Job</button>
        {currentJob && <p style={{ color: 'green' }}>✅ Job Created: {currentJob.title}</p>}
      </div>

      {/* STEP 2 */}
      {currentJob && (
        <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc' }}>
          <h2>Step 2 — Add Candidates</h2>
          <input placeholder="Name" value={candName} onChange={e => setCandName(e.target.value)} style={{ display: 'block', marginBottom: '10px', width: '100%' }} />
          <input placeholder="Email" value={candEmail} onChange={e => setCandEmail(e.target.value)} style={{ display: 'block', marginBottom: '10px', width: '100%' }} />
          <textarea placeholder="Paste Resume Text" value={candResume} onChange={e => setCandResume(e.target.value)} style={{ display: 'block', marginBottom: '10px', width: '100%', height: '100px' }} />
          <button onClick={addCandidate}>Add Candidate</button>
          <p>{candidates.length} candidate(s) added</p>
        </div>
      )}

      {/* STEP 3 */}
      {candidates.length > 0 && (
        <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc' }}>
          <h2>Step 3 — Screen Candidates</h2>
          <button onClick={screenAll} style={{ marginRight: '10px' }}>
            🚀 Screen All with AI
          </button>
          <button onClick={screenWithLangGraph}>
            🤖 Screen with LangGraph
          </button>
        </div>
      )}

      {/* RESULTS */}
      {rankings.length > 0 && (
        <RankingTable data={rankings} title="📊 Manual AI Pipeline Rankings" />
      )}

      {langGraphRankings.length > 0 && (
        <RankingTable data={langGraphRankings} title="🤖 LangGraph Pipeline Rankings" />
      )}

    </div>
  )
}

export default App